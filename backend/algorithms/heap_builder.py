"""
堆的创建算法执行器
将堆创建过程拆解为标准化的步骤数据
"""
from typing import List, Dict, Any, Generator
from copy import deepcopy


class HeapBuilder:
    """
    堆创建算法执行器
    
    核心思路：将传统"只输出结果"的算法逻辑，重写为"记录每一步操作"的逻辑
    步骤数据包含：当前操作节点、比较节点、数据变化、操作描述等
    """
    
    def __init__(self, data: List[int]):
        """
        初始化堆构建器
        
        Args:
            data: 输入的整数数组
        """
        self.original_data = deepcopy(data)
        self.data = deepcopy(data)
        self.steps = []
        self.step_id = 0
    
    def _add_step(self, 
                  description: str, 
                  action: str,
                  current_node: int = None,
                  compare_node: int = None,
                  compare_with: int = None,
                  swapped: bool = False,
                  swapped_with: int = None,
                  highlight_indices: List[int] = None,
                  color_state: str = "normal") -> None:
        """
        添加一个步骤记录
        
        Args:
            description: 步骤文字描述
            action: 操作类型 (init, compare, swap, adjust, complete)
            current_node: 当前操作节点索引
            compare_node: 比较节点索引
            compare_with: 比较的值
            swapped: 是否发生交换
            swapped_with: 交换的目标节点索引
            highlight_indices: 需要高亮的节点索引列表
            color_state: 颜色状态 (normal, comparing, swapping, completed)
        """
        self.step_id += 1
        
        step = {
            "step_id": self.step_id,
            "algorithm": "heap",
            "description": description,
            "action": action,
            "array_state": deepcopy(self.data),
            "current_node": current_node,
            "compare_node": compare_node,
            "compare_with": compare_with,
            "swapped": swapped,
            "swapped_with": swapped_with,
            "highlight_indices": highlight_indices or [],
            "color_state": color_state
        }
        self.steps.append(step)
    
    def _heapify(self, arr: List[int], n: int, i: int) -> None:
        """
        堆化操作：从节点i开始向下调整
        
        Args:
            arr: 数组
            n: 堆大小
            i: 当前节点索引
        """
        largest = i  # 假设当前节点最大
        left = 2 * i + 1   # 左子节点
        right = 2 * i + 2  # 右子节点
        
        # 记录当前调整的节点
        self._add_step(
            description=f"开始调整索引{i}的节点，值为{arr[i]}",
            action="adjust_start",
            current_node=i,
            color_state="comparing",
            highlight_indices=[i]
        )
        
        # 比较左子节点
        if left < n:
            self._add_step(
                description=f"比较节点{arr[i]}与左子节点{arr[left]}",
                action="compare",
                current_node=i,
                compare_node=left,
                compare_with=arr[left],
                color_state="comparing",
                highlight_indices=[i, left]
            )
            
            if arr[left] > arr[largest]:
                largest = left
        
        # 比较右子节点
        if right < n:
            self._add_step(
                description=f"比较节点{arr[largest]}与右子节点{arr[right]}",
                action="compare",
                current_node=largest,
                compare_node=right,
                compare_with=arr[right],
                color_state="comparing",
                highlight_indices=[largest, right]
            )
            
            if arr[right] > arr[largest]:
                largest = right
        
        # 如果最大值不是当前节点，交换
        if largest != i:
            self._add_step(
                description=f"交换节点{arr[i]}和{arr[largest]}",
                action="swap",
                current_node=i,
                swapped_with=largest,
                swapped=True,
                color_state="swapping",
                highlight_indices=[i, largest]
            )
            
            # 执行交换
            arr[i], arr[largest] = arr[largest], arr[i]
            self.data = deepcopy(arr)
            
            self._add_step(
                description=f"交换完成，数组变为{arr}",
                action="swap_complete",
                swapped=True,
                swapped_with=largest,
                color_state="swapping",
                highlight_indices=[i, largest]
            )
            
            # 递归堆化受影响的子树
            self._heapify(arr, n, largest)
        else:
            self._add_step(
                description=f"节点{arr[i]}无需调整，保持位置",
                action="no_change",
                current_node=i,
                color_state="completed",
                highlight_indices=[i]
            )
    
    def build_max_heap(self) -> List[Dict[str, Any]]:
        """
        构建最大堆，返回所有步骤
        
        Returns:
            步骤数据列表
        """
        self.steps = []
        self.step_id = 0
        n = len(self.data)
        
        # 初始化步骤
        self._add_step(
            description=f"初始数组: {self.data}，开始构建最大堆",
            action="init",
            color_state="normal"
        )
        
        # 从最后一个非叶子节点开始向前调整
        # 最后一个非叶子节点的索引: (n-1) // 2
        start_idx = (n - 1) // 2
        
        self._add_step(
            description=f"最后一个非叶子节点索引: {start_idx}",
            action="info",
            color_state="normal"
        )
        
        # 标记非叶子节点
        non_leaf_indices = list(range(start_idx, -1, -1))
        for idx in non_leaf_indices:
            self._add_step(
                description=f"调整以索引{idx}为根的子树",
                action="subtree_start",
                current_node=idx,
                highlight_indices=[idx],
                color_state="comparing"
            )
            self._heapify(self.data, n, idx)
        
        # 完成步骤
        self._add_step(
            description=f"最大堆构建完成！最终数组: {self.data}",
            action="complete",
            color_state="completed",
            highlight_indices=list(range(n))
        )
        
        return self.steps
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """获取所有步骤"""
        return self.build_max_heap()


def run_heap_algorithm(data: List[int]) -> List[Dict[str, Any]]:
    """
    运行堆创建算法的便捷函数
    
    Args:
        data: 输入的整数数组
        
    Returns:
        步骤数据列表
    """
    builder = HeapBuilder(data)
    return builder.get_steps()
