"""
数据校验工具模块
负责验证用户输入数据的合法性
"""
from typing import Tuple, List, Optional, Dict, Any
from config import Config


class ValidationError(Exception):
    """自定义校验异常"""
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DataValidator:
    """数据校验器"""
    
    # 支持的算法类型
    SUPPORTED_ALGORITHMS = ['heap', 'quicksort', 'linkedlist', 'btree']
    
    @classmethod
    def validate_algorithm_type(cls, algorithm: str) -> Tuple[bool, Optional[str]]:
        """
        校验算法类型是否合法
        
        Args:
            algorithm: 算法类型标识
            
        Returns:
            (是否合法, 错误信息)
        """
        if algorithm not in cls.SUPPORTED_ALGORITHMS:
            return False, f"不支持的算法类型，请选择: {', '.join(cls.SUPPORTED_ALGORITHMS)}"
        return True, None
    
    @classmethod
    def validate_integer_list(cls, data: Any, algorithm: str) -> Tuple[bool, Optional[str], Optional[List[int]]]:
        """
        校验输入数据是否为整数数组
        
        Args:
            data: 输入数据
            algorithm: 算法类型
            
        Returns:
            (是否合法, 错误信息, 转换后的整数列表)
        """
        # 检查是否为列表
        if not isinstance(data, list):
            return False, "输入数据必须是数组格式", None
        
        # 检查是否为空
        if len(data) == 0:
            return False, "输入数组不能为空", None
        
        # 获取算法配置
        config = Config.ALGORITHM_CONFIG.get(algorithm, {})
        min_len = config.get('min_length', 1)
        max_len = config.get('max_length', 20)
        desc = config.get('description', '算法')
        
        # 检查长度
        if len(data) < min_len:
            return False, f"{desc}至少需要{min_len}个数据", None
        
        if len(data) > max_len:
            return False, f"{desc}最多支持{max_len}个数据", None
        
        # 检查每个元素是否为整数
        int_list = []
        for i, item in enumerate(data):
            if isinstance(item, int):
                int_list.append(item)
            elif isinstance(item, float):
                # 允许浮点数但会转为整数
                int_list.append(int(item))
            elif isinstance(item, str):
                try:
                    int_list.append(int(item))
                except ValueError:
                    return False, f"第{i+1}个元素 '{item}' 不是有效的整数", None
            else:
                return False, f"第{i+1}个元素类型错误，只支持整数", None
        
        return True, None, int_list
    
    @classmethod
    def validate_input_request(cls, request_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        校验完整的请求数据
        
        Args:
            request_data: 请求JSON数据
            
        Returns:
            (是否合法, 错误信息, 校验后的数据)
        """
        # 检查必要字段
        if 'algorithm' not in request_data:
            return False, "缺少algorithm字段", None
        
        if 'data' not in request_data:
            return False, "缺少data字段", None
        
        algorithm = request_data['algorithm']
        data = request_data['data']
        
        # 校验算法类型
        valid, error = cls.validate_algorithm_type(algorithm)
        if not valid:
            return False, error, None
        
        # 校验数据
        valid, error, int_list = cls.validate_integer_list(data, algorithm)
        if not valid:
            return False, error, None
        
        return True, None, {
            'algorithm': algorithm,
            'data': int_list
        }
