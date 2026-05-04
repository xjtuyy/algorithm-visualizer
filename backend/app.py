"""
Flask主服务
整合HTTP接口和WebSocket通信
"""
import os
import json
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS

from config import Config
from utils.validator import DataValidator, ValidationError
from algorithms.runner import AlgorithmRunner

# 创建Flask应用
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)

# 启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# 创建SocketIO实例
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# 用户会话管理
# 存储每个用户的状态: {session_id: {"data": [], "algorithm": "", "steps": [], "step_index": 0, "is_paused": False, "is_running": False}}
user_sessions = {}
# 线程锁，确保会话操作的线程安全
sessions_lock = threading.Lock()


def get_session(sid: str) -> dict:
    """获取或创建用户会话"""
    with sessions_lock:
        if sid not in user_sessions:
            user_sessions[sid] = {
                "data": [],
                "algorithm": "",
                "steps": [],
                "step_index": 0,
                "is_paused": False,
                "is_running": False,
                "speed": Config.DEFAULT_STEP_DELAY
            }
        return user_sessions[sid]


def clear_session(sid: str) -> None:
    """清除用户会话"""
    with sessions_lock:
        if sid in user_sessions:
            del user_sessions[sid]


# ==================== HTTP路由 ====================

@app.route('/')
def index():
    """提供前端页面"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health')
def health():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "算法可视化演示系统运行中"
    })


@app.route('/api/algorithms')
def get_algorithms():
    """获取支持的算法列表"""
    algorithms = AlgorithmRunner.get_supported_algorithms()
    return jsonify({
        "algorithms": [
            {
                "id": algo,
                "description": AlgorithmRunner.get_algorithm_description(algo)
            }
            for algo in algorithms
        ]
    })


@app.route('/api/submit', methods=['POST'])
def submit_data():
    """
    接收前端提交的算法演示请求
    
    请求格式:
    {
        "algorithm": "heap" | "quicksort" | "linkedlist" | "btree",
        "data": [1, 2, 3, ...],
        "traversal_type": "preorder" | "inorder" | "postorder"  # 仅btree需要
    }
    
    返回格式:
    {
        "success": true | false,
        "message": "...",
        "steps_count": 10  # 总步骤数
    }
    """
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                "success": False,
                "message": "请求数据格式错误"
            }), 400
        
        # 校验输入数据
        valid, error, validated_data = DataValidator.validate_input_request(request_data)
        
        if not valid:
            return jsonify({
                "success": False,
                "message": error
            }), 400
        
        # 获取算法和参数
        algorithm = validated_data['algorithm']
        data = validated_data['data']
        traversal_type = request_data.get('traversal_type', 'preorder')
        
        # 生成步骤数据
        if algorithm == 'btree':
            steps = AlgorithmRunner.run(algorithm, data, traversal_type=traversal_type)
        else:
            steps = AlgorithmRunner.run(algorithm, data)
        
        return jsonify({
            "success": True,
            "message": f"{AlgorithmRunner.get_algorithm_description(algorithm)}演示准备就绪",
            "steps_count": len(steps)
        })
        
    except ValidationError as e:
        return jsonify({
            "success": False,
            "message": e.message
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


# ==================== WebSocket事件处理 ====================

@socketio.on('connect')
def handle_connect():
    """处理客户端连接"""
    sid = request.sid
    get_session(sid)  # 创建会话
    print(f"客户端连接: {sid}")
    emit('connected', {
        'sid': sid,
        'message': '连接成功'
    })


@socketio.on('disconnect')
def handle_disconnect():
    """处理客户端断开连接"""
    sid = request.sid
    clear_session(sid)
    print(f"客户端断开: {sid}")


@socketio.on('join')
def handle_join(data):
    """
    处理用户加入事件（可选，用于多房间场景）
    
    data: {"room": "room_id"}
    """
    room = data.get('room')
    if room:
        join_room(room)
        emit('joined', {'room': room})


@socketio.on('leave')
def handle_leave(data):
    """处理用户离开事件"""
    room = data.get('room')
    if room:
        leave_room(room)
        emit('left', {'room': room})


@socketio.on('start_visualization')
def handle_start_visualization(data):
    """
    开始可视化演示
    
    data: {
        "algorithm": "heap",
        "data": [1, 2, 3, ...],
        "traversal_type": "preorder",  # 仅btree需要
        "speed": 1.0  # 播放速度，可选
    }
    """
    sid = request.sid
    session = get_session(sid)
    
    try:
        algorithm = data.get('algorithm')
        input_data = data.get('data')
        traversal_type = data.get('traversal_type', 'preorder')
        speed = data.get('speed', Config.DEFAULT_STEP_DELAY)
        
        # 校验数据
        valid, error, validated_data = DataValidator.validate_input_request({
            "algorithm": algorithm,
            "data": input_data
        })
        
        if not valid:
            emit('error', {'message': error})
            return
        
        # 更新会话状态
        session['algorithm'] = algorithm
        session['data'] = validated_data['data']
        session['speed'] = speed
        session['is_paused'] = False
        session['is_running'] = True
        session['step_index'] = 0
        
        # 生成步骤数据
        if algorithm == 'btree':
            steps = AlgorithmRunner.run(algorithm, validated_data['data'], traversal_type=traversal_type)
        else:
            steps = AlgorithmRunner.run(algorithm, validated_data['data'])
        
        session['steps'] = steps
        
        # 发送准备就绪信号
        emit('visualization_ready', {
            'total_steps': len(steps),
            'algorithm': algorithm,
            'data': validated_data['data']
        })
        
        print(f"用户 {sid} 开始 {algorithm} 演示，共 {len(steps)} 步")
        
    except Exception as e:
        emit('error', {'message': f"启动失败: {str(e)}"})


@socketio.on('get_step')
def handle_get_step(data):
    """
    获取下一步骤数据
    前端通过此事件主动获取下一步
    """
    sid = request.sid
    session = get_session(sid)
    
    if not session['is_running']:
        emit('error', {'message': "没有正在运行的演示"})
        return
    
    if session['is_paused']:
        emit('paused', {'message': "演示已暂停"})
        return
    
    # 获取当前步骤
    if session['step_index'] < len(session['steps']):
        step = session['steps'][session['step_index']]
        session['step_index'] += 1
        
        emit('step', step)
        
        # 如果是最后一步，发送完成信号
        if session['step_index'] >= len(session['steps']):
            session['is_running'] = False
            emit('visualization_complete', {
'message': '演示完成'
            })
    else:
        session['is_running'] = False
        emit('visualization_complete', {
            'message': '演示完成'
        })


@socketio.on('pause')
def handle_pause():
    """暂停演示"""
    sid = request.sid
    session = get_session(sid)
    
    if session['is_running']:
        session['is_paused'] = True
        emit('paused', {'message': '演示已暂停'})


@socketio.on('resume')
def handle_resume():
    """继续演示"""
    sid = request.sid
    session = get_session(sid)
    
    if session['is_running'] and session['is_paused']:
        session['is_paused'] = False
        emit('resumed', {'message': '演示继续'})


@socketio.on('reset')
def handle_reset():
    """重置演示"""
    sid = request.sid
    session = get_session(sid)
    
    session['is_running'] = False
    session['is_paused'] = False
    session['step_index'] = 0
    session['steps'] = []
    
    emit('reset', {'message': '演示已重置'})


@socketio.on('change_speed')
def handle_change_speed(data):
    """改变演示速度"""
    sid = request.sid
    session = get_session(sid)
    
    speed = data.get('speed', Config.DEFAULT_STEP_DELAY)
    # 限制速度范围
    speed = max(Config.MIN_STEP_DELAY, min(Config.MAX_STEP_DELAY, speed))
    
    session['speed'] = speed
    emit('speed_changed', {'speed': speed})


@socketio.on('get_status')
def handle_get_status():
    """获取当前状态"""
    sid = request.sid
    session = get_session(sid)
    
    emit('status', {
        'is_running': session['is_running'],
        'is_paused': session['is_paused'],
        'step_index': session['step_index'],
        'total_steps': len(session['steps']),
        'algorithm': session['algorithm']
    })


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    """404错误处理"""
    return jsonify({
        "error": "Not Found",
        "message": "请求的资源不存在"
    }), 404


@app.errorhandler(500)
def server_error(e):
    """500错误处理"""
    return jsonify({
        "error": "Server Error",
        "message": "服务器内部错误"
    }), 500


# ==================== 启动应用 ====================

if __name__ == '__main__':
    print("=" * 50)
    print("算法可视化演示系统 - 后端服务")
    print("=" * 50)
    print("支持算法:")
    for algo in AlgorithmRunner.get_supported_algorithms():
        print(f"  - {algo}: {AlgorithmRunner.get_algorithm_description(algo)}")
    print("=" * 50)
    print("服务地址: http://127.0.0.1:5000")
    print("WebSocket: ws://127.0.0.1:5000")
    print("=" * 50)
    
    # 生产环境使用 gevent 支持 WebSocket
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True
    )
