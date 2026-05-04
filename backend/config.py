"""
配置文件
"""
import os

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'algorithm-visualizer-secret-key'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # CORS配置，允许前端跨域访问
    CORS_HEADERS = 'Content-Type'
    
    # 算法参数配置
    ALGORITHM_CONFIG = {
        'heap': {
            'min_length': 1,
            'max_length': 20,
            'description': '堆的创建'
        },
        'quicksort': {
            'min_length': 1,
            'max_length': 15,
            'description': '快速排序'
        },
        'linkedlist': {
            'min_length': 1,
            'max_length': 10,
            'description': '链表操作'
        },
        'btree': {
            'min_length': 1,
            'max_length': 15,
            'description': '二叉树遍历'
        }
    }
    
    # WebSocket推送间隔（秒），控制演示速度
    DEFAULT_STEP_DELAY = 1.0
    MIN_STEP_DELAY = 0.2
    MAX_STEP_DELAY = 3.0
