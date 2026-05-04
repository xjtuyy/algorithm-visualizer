# 算法可视化演示系统 - 后端

## 项目概述

基于 Flask + WebSocket 的数据结构与算法可视化演示系统后端服务。支持四种算法的步骤拆解与实时推送：
- 堆的创建（最大堆）
- 快速排序
- 链表创建与遍历
- 二叉树遍历

## 项目结构

```
backend/
├── app.py                 # Flask主服务入口
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── README.md              # 本文档
├── utils/
│   ├── __init__.py
│   └── validator.py      # 数据校验工具
└── algorithms/
    ├── __init__.py
    ├── runner.py          # 算法执行器统一入口
    ├── heap_builder.py   # 堆创建算法
    ├── quick_sort.py     # 快速排序算法
    ├── linked_list.py    # 链表操作算法
    └── binary_tree.py    # 二叉树遍历算法
```

## 环境配置

### 1. 创建虚拟环境（推荐）

```bash
cd backend
python -m venv venv

# Windows激活
venv\Scripts\activate

# Linux/Mac激活
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://127.0.0.1:5000` 启动。

## API接口文档

### HTTP接口

#### 1. 健康检查
```
GET /api/health
```

响应示例：
```json
{
    "status": "ok",
    "message": "算法可视化演示系统运行中"
}
```

#### 2. 获取支持的算法列表
```
GET /api/algorithms
```

响应示例：
```json
{
    "algorithms": [
        {"id": "heap", "description": "堆的创建（最大堆）"},
        {"id": "quicksort", "description": "快速排序"},
        {"id": "linkedlist", "description": "链表创建与遍历"},
        {"id": "btree", "description": "二叉树遍历"}
    ]
}
```

#### 3. 提交算法演示请求
```
POST /api/submit
Content-Type: application/json

{
    "algorithm": "heap",
    "data": [4, 10, 3, 5, 1, 8, 7, 2, 9],
    "traversal_type": "preorder"  // 仅btree需要
}
```

响应示例：
```json
{
    "success": true,
    "message": "堆的创建（最大堆）演示准备就绪",
    "steps_count": 25
}
```

错误响应：
```json
{
    "success": false,
    "message": "堆的创建至少需要1个数据"
}
```

### WebSocket事件

连接地址：`ws://127.0.0.1:5000`

#### 客户端 -> 服务端事件

| 事件名 | 数据格式 | 说明 |
|--------|----------|------|
| `start_visualization` | `{algorithm, data, traversal_type?, speed?}` | 开始可视化演示 |
| `get_step` | `{}` | 获取下一步骤数据 |
| `pause` | `{}` | 暂停演示 |
| `resume` | `{}` | 继续演示 |
| `reset` | `{}` | 重置演示 |
| `change_speed` | `{speed}` | 改变演示速度 |
| `get_status` | `{}` | 获取当前状态 |

#### 服务端 -> 客户端事件

| 事件名 | 数据格式 | 说明 |
|--------|----------|------|
| `connected` | `{sid, message}` | 连接成功 |
| `visualization_ready` | `{total_steps, algorithm, data}` | 演示准备就绪 |
| `step` | 步骤数据对象 | 单步数据 |
| `visualization_complete` | `{message}` | 演示完成 |
| `paused` | `{message}` | 已暂停 |
| `resumed` | `{message}` | 已继续 |
| `reset` | `{message}` | 已重置 |
| `status` | `{is_running, is_paused, step_index, total_steps, algorithm}` | 当前状态 |
| `error` | `{message}` | 错误信息 |

## 步骤数据格式

### 堆创建步骤数据
```json
{
    "step_id": 1,
    "algorithm": "heap",
    "description": "比较节点8与节点20",
    "action": "compare",
    "array_state": [20, 15, 8, 5, 10, ...],
    "current_node": 2,
    "compare_node": 5,
    "compare_with": 20,
    "swapped": false,
    "swapped_with": null,
    "highlight_indices": [2, 5],
    "color_state": "comparing"
}
```

### 快速排序步骤数据
```json
{
    "step_id": 1,
    "algorithm": "quicksort",
    "description": "选择基准元素: 5",
    "action": "select_pivot",
    "array_state": [3, 1, 5, 2, 4],
    "pivot_index": 2,
    "pivot_value": 5,
    "left_pointer": null,
    "right_pointer": null,
    "compare_index": null,
    "compare_value": null,
    "swapped": false,
    "swap_indices": [],
    "partition_range": [0, 4],
    "left_partition": null,
    "right_partition": null,
    "color_state": "comparing"
}
```

### 链表步骤数据
```json
{
    "step_id": 1,
    "algorithm": "linkedlist",
    "description": "创建头节点: 1",
    "action": "create_head",
    "list_state": [1],
    "nodes": [
        {"index": 0, "value": 1, "next_index": 1}
    ],
    "current_index": 0,
    "current_value": 1,
    "visited_indices": [],
    "highlight_indices": [0],
    "color_state": "comparing"
}
```

### 二叉树步骤数据
```json
{
    "step_id": 1,
    "algorithm": "btree",
    "description": "开始构建二叉树，数据: [1, 2, 3, 4, 5]",
    "action": "init",
    "tree_data": [1, 2, 3, 4, 5],
    "tree_structure": {
        "1": {"level": 0, "x": 50, "y": 20, "value": 1, "children": [2, 3]},
        "2": {"level": 1, "x": 25, "y": 100, "value": 2, "children": [4, 5]},
        "3": {"level": 1, "x": 75, "y": 100, "value": 3, "children": []}
    },
    "current_node": null,
    "current_level": null,
    "visited_values": [],
    "visited_order": [],
    "highlight_nodes": [],
    "traversal_type": "preorder",
    "color_state": "normal"
}
```

## 颜色状态说明

| 状态值 | 说明 |
|--------|------|
| `normal` | 普通状态 |
| `comparing` | 正在比较/操作中 |
| `swapping` | 正在交换 |
| `completed` | 已完成 |
| `error` | 错误状态 |

## 使用示例

### Python客户端示例

```python
import socketio

sio = socketio.Client()

@sio.on('connected')
def on_connected(data):
    print('Connected:', data)
    # 开始可视化
    sio.emit('start_visualization', {
        'algorithm': 'heap',
        'data': [4, 10, 3, 5, 1, 8, 7, 2, 9],
        'speed': 1.0
    })

@sio.on('visualization_ready')
def on_ready(data):
    print('Ready:', data)

@sio.on('step')
def on_step(data):
    print('Step:', data)
    # 发送获取下一步
    sio.sleep(1)
    sio.emit('get_step')

@sio.on('visualization_complete')
def on_complete(data):
    print('Complete:', data)

sio.connect('http://127.0.0.1:5000')
sio.wait()
```

## 常见问题

### 1. WebSocket连接失败
- 确保后端服务已启动
- 检查防火墙设置
- 确认端口5000未被占用

### 2. 跨域问题
- 已配置 CORS，允许所有来源
- 如仍有跨域问题，检查浏览器控制台

### 3. 算法数据校验失败
- 堆创建：至少1个数据，最多20个
- 快速排序：至少1个数据，最多15个
- 链表：至少1个数据，最多10个
- 二叉树：至少1个数据，最多15个

## 后续部署

本地开发测试通过后，可按以下步骤部署到云服务器：

1. **选择云服务器**（如阿里云、腾讯云、AWS等）
2. **安装Python环境**
3. **使用Gunicorn + Nginx + Supervisor**（生产环境推荐）
4. **配置域名和SSL证书**

具体部署步骤将在本地测试通过后提供。
