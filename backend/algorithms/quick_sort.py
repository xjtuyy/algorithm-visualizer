"""
快速排序算法执行器
将快速排序过程拆解为标准化的步骤数据
"""
from typing import List, Dict, Any
from copy import deepcopy


class QuickSortRunner:
    """
    快速排序算法执行器
    
    快速排序核心思想：
    1. 选择基准元素(pivot)
    2. 分区：将数组分为小于基准和大于基准的两部分
    3. 递归排序两部分
    """
    
    def __init__(self, data: List[int]):
        """
        初始化快速排序执行器
        
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
                  array_state: List[int] = None,
                  pivot_index: int = None,
                  pivot_value: int = None,
                  left_pointer: int = None,
                  right_pointer: int = None,
                  compare_index: int = None,
                  compare_value: int = None,
                  swapped: bool = False,
                  swap_indices: List[int] = None,
                  partition_range: List[int] = None,
                  left_partition: List[int] = None,
                  right_partition: List[int] = None,
                  color_state: str = "normal") -> None:
        """
        添加一个步骤记录
        
        Args:
            description: 步骤文字描述
            action: 操作类型
            array_state: 当前数组状态
            pivot_index: 基准元素索引
            pivot_value: 基准元素值
            left指针: 左指针位置
            right指针: 右指针位置
            compare_index: 比较的元素索引
            compare_value: 比较的元素值
            swapped: 是否发生交换
            swap_indices: 交换的索引对
            partition_range: 当前分区范围
            left_partition: 左分区元素
            right_partition: 右分区元素
            color_state: 颜色状态
        """
        self.step_id += 1
        
        step = {
            "step_id": self.step_id,
            "algorithm": "quicksort",
            "description": description,
            "action": action,
            "array_state": array_state if array_state is not None else deepcopy(self.data),
            "pivot_index": pivot_index,
            "pivot_value": pivot_value,
            "left_pointer": left_pointer,
            "right_pointer": right_pointer,
            "compare_index": compare_index,
            "compare_value": compare_value,
            "swapped": swapped,
            "swap_indices": swap_indices or [],
            "partition_range": partition_range,
            "left_partition": left_partition,
            "right_partition": right_partition,
            "color_state": color_state
        }
        self.steps.append(step)
    
    def _partition(self, arr: List[int], low: int, high: int) -> int:
        """
        分区操作
        
        Args:
            arr: 数组
            low: 起始索引
            high: 结束索引
            
        Returns:
            基准元素的最终位置
        """
        pivot = arr[high]  # 选择最后一个元素作为基准
        pivot_index = high
        
        self._add_step(
            description=f"选择基准元素: {pivot} (索引{high})",
            action="select_pivot",
            array_state=deepcopy(arr),
            pivot_index=pivot_index,
            pivot_value=pivot,
            partition_range=[low, high],
            color_state="comparing"
        )
        
        i = low - 1  # 小于基准元素的区域指针
        
        for j in range(low, high):
            # 记录右指针移动
            self._add_step(
                description=f"比较元素{arr[j]}与基准{pivot}",
                action="compare",
                array_state=deepcopy(arr),
pivot_index=pivot_index,
                pivot_value=pivot,
                right_pointer=j,
                compare_index=j,
                compare_value=arr[j],
                partition_range=[low, high],
                color_state="comparing"
            )
            
            if arr[j] < pivot:
                i += 1
                if i != j:
                    # 交换元素
                    self._add_step(
                        description=f"{arr[j]} < {pivot}，交换位置{arr[i]}和{arr[j]}",
                        action="swap",
                        array_state=deepcopy(arr),
                        pivot_index=pivot_index,
                        pivot_value=pivot,
                        left_pointer=i,
                        right_pointer=j,
                        swapped=True,
                        swap_indices=[i, j],
                        partition_range=[low, high],
                        color_state="swapping"
                    )
                    
                    arr[i], arr[j] = arr[j], arr[i]
                    self.data = deepcopy(arr)
                    
                    self._add_step(
                        description=f"交换后数组: {arr}",
                        action="swap_complete",
                        array_state=deepcopy(arr),
                        swapped=True,
                        swap_indices=[i, j],
                        partition_range=[low, high],
                        color_state="swapping"
                    )
        
        # 将基准元素放到正确位置
        if i + 1 != high:
            self._add_step(
                description=f"将基准{pivot}放到正确位置{arr[i+1]}",
                action="place_pivot",
                array_state=deepcopy(arr),
                pivot_index=high,
                pivot_value=pivot,
                swapped=True,
                swap_indices=[i + 1, high],
                partition_range=[low, high],
                color_state="swapping"
            )
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            self.data = deepcopy(arr)
            
            self._add_step(
                description=f"基准放置完成，数组: {arr}",
                action="partition_complete",
                array_state=deepcopy(arr),
                pivot_index=i + 1,
                pivot_value=pivot,
                partition_range=[low, high],
                color_state="completed"
            )
        
        return i + 1
    
    def _quick_sort(self, arr: List[int], low: int, high: int) -> None:
        """
        快速排序递归函数
        
        Args:
            arr: 数组
            low: 起始索引
            high: 结束索引
        """
        if low < high:
            self._add_step(
                description=f"开始排序子数组 [{low}:{high}] = {arr[low:high+1]}",
                action="subarray_start",
                array_state=deepcopy(arr),
                partition_range=[low, high],
                color_state="comparing"
            )
            
            # 分区
            pivot_pos = self._partition(arr, low, high)
            
            # 递归排序左半部分
            self._add_step(
                description=f"基准{pivot_pos}已排序，递归排序左半部分[{low}:{pivot_pos-1}]" if pivot_pos > low else f"基准位置{low}，无需排序左半部分",
                action="recurse_left",
                array_state=deepcopy(arr),
                partition_range=[low, pivot_pos - 1] if pivot_pos > low else None,
                color_state="comparing"
            )
            
            if pivot_pos > low:
                self._quick_sort(arr, low, pivot_pos - 1)
            
            # 递归排序右半部分
            self._add_step(
                description=f"递归排序右半部分[{pivot_pos+1}:{high}]" if pivot_pos < high else f"无需排序右半部分",
                action="recurse_right",
                array_state=deepcopy(arr),
                partition_range=[pivot_pos + 1, high] if pivot_pos < high else None,
                color_state="comparing"
            )
            
            if pivot_pos < high:
                self._quick_sort(arr, pivot_pos + 1, high)
    
    def sort(self) -> List[Dict[str, Any]]:
        """
        执行快速排序，返回所有步骤
        
        Returns:
            步骤数据列表
        """
        self.steps = []
        self.step_id = 0
        
        # 初始化步骤
        self._add_step(
            description=f"初始数组: {self.data}",
            action="init",
            array_state=deepcopy(self.data),
            color_state="normal"
        )
        
        # 开始排序
        self._quick_sort(self.data, 0, len(self.data) - 1)
        
        # 完成步骤
        self._add_step(
            description=f"快速排序完成！最终数组: {self.data}",
            action="complete",
            array_state=deepcopy(self.data),
            color_state="completed"
        )
        
        return self.steps
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """获取所有步骤"""
        return self.sort()


def run_quicksort_algorithm(data: List[int]) -> List[Dict[str, Any]]:
    """
    运行快速排序算法的便捷函数
    
    Args:
        data: 输入的整数数组
        
    Returns:
        步骤数据列表
    """
    runner = QuickSortRunner(data)
    return runner.get_steps()
