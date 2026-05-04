"""
算法执行器统一入口
提供统一的接口调用不同算法的步骤拆解
"""
from typing import List, Dict, Any, Optional

from .heap_builder import HeapBuilder, run_heap_algorithm
from .quick_sort import QuickSortRunner, run_quicksort_algorithm
from .linked_list import LinkedListRunner, run_linkedlist_algorithm
from .binary_tree import BinaryTreeRunner, run_btree_algorithm


class AlgorithmRunner:
    """
    算法执行器统一管理类
    
    提供统一的接口，根据算法类型调用对应的算法执行器
    """
    
    # 算法执行器映射
    _ALGORITHM_RUNNERS = {
        'heap': HeapBuilder,
        'quicksort': QuickSortRunner,
        'linkedlist': LinkedListRunner,
        'btree': BinaryTreeRunner
    }
    
    # 算法对应的便捷函数映射
    _ALGORITHM_FUNCTIONS = {
        'heap': run_heap_algorithm,
        'quicksort': run_quicksort_algorithm,
        'linkedlist': run_linkedlist_algorithm,
        'btree': run_btree_algorithm
    }
    
    @classmethod
    def run(cls, algorithm: str, data: List[int], **kwargs) -> List[Dict[str, Any]]:
        """
        运行指定算法的步骤拆解
        
        Args:
            algorithm: 算法类型 ('heap', 'quicksort', 'linkedlist', 'btree')
            data: 输入数据
            **kwargs: 算法的额外参数（如btree需要traversal_type）
            
        Returns:
            步骤数据列表
            
        Raises:
            ValueError: 不支持的算法类型
        """
        if algorithm not in cls._ALGORITHM_FUNCTIONS:
            raise ValueError(f"不支持的算法类型: {algorithm}")
        
        func = cls._ALGORITHM_FUNCTIONS[algorithm]
        
        # btree需要额外的traversal_type参数
        if algorithm == 'btree':
            traversal_type = kwargs.get('traversal_type', 'preorder')
            return func(data, traversal_type)
        
        return func(data)
    
    @classmethod
    def get_supported_algorithms(cls) -> List[str]:
        """
        获取支持的算法列表
        
        Returns:
            算法类型列表
        """
        return list(cls._ALGORITHM_RUNNERS.keys())
    
    @classmethod
    def get_algorithm_description(cls, algorithm: str) -> str:
        """
        获取算法的描述信息
        
        Args:
            algorithm: 算法类型
            
        Returns:
            算法描述
        """
        descriptions = {
            'heap': '堆的创建（最大堆）',
            'quicksort': '快速排序',
            'linkedlist': '链表创建与遍历',
            'btree': '二叉树遍历'
        }
        return descriptions.get(algorithm, '未知算法')


def run_algorithm(algorithm: str, data: List[int], **kwargs) -> List[Dict[str, Any]]:
    """
    运行算法的便捷函数
    
    Args:
        algorithm: 算法类型
        data: 输入数据
        **kwargs: 额外参数
        
    Returns:
        步骤数据列表
    """
    return AlgorithmRunner.run(algorithm, data, **kwargs)
