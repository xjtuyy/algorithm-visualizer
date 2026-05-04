"""
链表操作算法执行器
展示链表的创建和遍历过程
"""
from typing import List, Dict, Any, Optional
from copy import deepcopy


class ListNode:
    """链表节点"""
    def __init__(self, val: int):
        self.val = val
        self.next: Optional['ListNode'] = None
    
    def __repr__(self):
        return f"ListNode({self.val})"


class LinkedListRunner:
    """
    链表操作算法执行器
    
    展示链表的创建过程和遍历过程
    """
    
    def __init__(self, data: List[int]):
        """
        初始化链表执行器
        
        Args:
            data: 输入的整数数组，将被构造成链表
        """
        self.original_data = deepcopy(data)
        self.data = deepcopy(data)
        self.head: Optional[ListNode] = None
        self.steps = []
        self.step_id = 0
    
    def _build_linked_list(self, data: List[int]) -> Optional[ListNode]:
        """
        从数组构建链表
        
        Args:
            data: 数据数组
            
        Returns:
            链表头节点
        """
        if not data:
            return None
        
        head = ListNode(data[0])
        current = head
        
        for i in range(1, len(data)):
            current.next = ListNode(data[i])
            current = current.next
        
        return head
    
    def _linked_list_to_array(self, head: Optional[ListNode]) -> List[int]:
        """
        将链表转换为数组（用于可视化）
        
        Args:
            head: 链表头节点
            
        Returns:
            数组表示
        """
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result
    
    def _linked_list_to_nodes(self, head: Optional[ListNode]) -> List[Dict[str, Any]]:
        """
        将链表转换为节点列表（用于可视化）
        
        Args:
            head: 链表头节点
            
        Returns:
            节点列表，包含索引和值
        """
        nodes = []
        current = head
        idx = 0
        while current:
            nodes.append({
                "index": idx,
                "value": current.val,
                "next_index": idx + 1 if current.next else None
            })
            current = current.next
            idx += 1
        return nodes
    
    def _add_step(self,
                  description: str,
                  action: str,
                  list_state: List[int] = None,
                  nodes: List[Dict[str, Any]] = None,
                  current_index: int = None,
                  current_value: int = None,
                  visited_indices: List[int] = None,
                  highlight_indices: List[int] = None,
                  color_state: str = "normal") -> None:
        """
        添加一个步骤记录
        
        Args:
            description: 步骤文字描述
            action: 操作类型
            list_state: 链表当前状态（数组形式）
            nodes: 链表节点列表
            current_index: 当前操作节点索引
            current_value: 当前操作节点值
            visited_indices: 已访问的节点索引
            highlight_indices: 需要高亮的节点索引
            color_state: 颜色状态
        """
        self.step_id += 1
        
        step = {
            "step_id": self.step_id,
            "algorithm": "linkedlist",
            "description": description,
            "action": action,
            "list_state": list_state if list_state is not None else self._linked_list_to_array(self.head),
            "nodes": nodes if nodes is not None else self._linked_list_to_nodes(self.head),
            "current_index": current_index,
            "current_value": current_value,
            "visited_indices": visited_indices or [],
            "highlight_indices": highlight_indices or [],
            "color_state": color_state
        }
        self.steps.append(step)
    
    def create_list(self) -> List[Dict[str, Any]]:
        """
        创建链表，返回所有步骤
        
        Returns:
            步骤数据列表
        """
        self.steps = []
        self.step_id = 0
        
        # 初始化步骤
        self._add_step(
            description=f"开始创建链表，数据: {self.data}",
            action="init",
            list_state=self.data,
            nodes=[],
            color_state="normal"
        )
        
        if not self.data:
            self._add_step(
                description="空数组，无法创建链表",
                action="error",
                list_state=[],
                nodes=[],
                color_state="error"
            )
            return self.steps
        
        # 创建第一个节点
        self._add_step(
            description=f"创建头节点: {self.data[0]}",
            action="create_head",
            list_state=self.data[:1],
            nodes=[{
                "index": 0,
                "value": self.data[0],
                "next_index": 1 if len(self.data) > 1 else None
            }],
            current_index=0,
            current_value=self.data[0],
            highlight_indices=[0],
            color_state="comparing"
        )
        
        self.head = self._build_linked_list(self.data[:1])
        visited = [0]
        
        # 创建后续节点
        for i in range(1, len(self.data)):
            self._add_step(
                description=f"在尾部添加节点: {self.data[i]}",
                action="append",
                list_state=self.data[:i+1],
                nodes=self._linked_list_to_nodes(self.head),
                current_index=i,
                current_value=self.data[i],
                visited_indices=visited.copy(),
                highlight_indices=[i],
                color_state="comparing"
            )
            
            # 添加新节点到链表
            current = self.head
            while current.next:
                current = current.next
            current.next = ListNode(self.data[i])
            
            visited.append(i)
            
            self._add_step(
                description=f"节点 {self.data[i]} 添加完成",
                action="append_complete",
                list_state=self._linked_list_to_array(self.head),
                nodes=self._linked_list_to_nodes(self.head),
                visited_indices=visited.copy(),
                highlight_indices=[i],
                color_state="completed"
            )
        
        # 创建完成
        self._add_step(
            description=f"链表创建完成！共{len(self.data)}个节点",
            action="complete",
            list_state=self._linked_list_to_array(self.head),
            nodes=self._linked_list_to_nodes(self.head),
            visited_indices=list(range(len(self.data))),
            color_state="completed"
        )
        
        return self.steps
    
    def traverse_list(self) -> List[Dict[str, Any]]:
        """
        遍历链表，返回所有步骤
        
        Returns:
            步骤数据列表
        """
        self.steps = []
        self.step_id = 0
        
        # 首先创建链表
        self.head = self._build_linked_list(self.data)
        
        # 初始化步骤
        self._add_step(
            description=f"开始遍历链表，节点数据: {self.data}",
            action="init",
            list_state=self.data,
            nodes=self._linked_list_to_nodes(self.head),
            color_state="normal"
        )
        
        if not self.head:
            self._add_step(
                description="链表为空，遍历结束",
                action="empty",
                list_state=[],
                nodes=[],
                color_state="completed"
            )
            return self.steps
        
# 开始遍历
        current = self.head
        idx = 0
        visited = []
        result = []
        
        self._add_step(
            description=f"从头节点开始遍历",
            action="traverse_start",
            list_state=self.data,
            nodes=self._linked_list_to_nodes(self.head),
            current_index=0,
            current_value=current.val,
            highlight_indices=[0],
            color_state="comparing"
        )
        
        while current:
            visited.append(idx)
            result.append(current.val)
            
            self._add_step(
                description=f"访问节点 {idx}: 值 = {current.val}",
                action="visit",
                list_state=result + self.data[len(result):],
                nodes=self._linked_list_to_nodes(self.head),
                current_index=idx,
                current_value=current.val,
                visited_indices=visited.copy(),
                highlight_indices=[idx],
                color_state="completed"
            )
            
            if current.next:
                self._add_step(
                    description=f"移动到下一个节点",
                    action="move_next",
                    list_state=result + self.data[len(result):],
                    nodes=self._linked_list_to_nodes(self.head),
                    visited_indices=visited.copy(),
                    color_state="normal"
                )
            
            current = current.next
            idx += 1
        
        # 遍历完成
        self._add_step(
            description=f"遍历完成！访问顺序: {result}",
            action="complete",
            list_state=self.data,
            nodes=self._linked_list_to_nodes(self.head),
            visited_indices=visited.copy(),
            color_state="completed"
        )
        
        return self.steps
    
    def run(self) -> List[Dict[str, Any]]:
        """
        运行完整的链表演示（创建+遍历）
        
        Returns:
            步骤数据列表
        """
        create_steps = self.create_list()
        self.data = deepcopy(self.original_data)  # 重置数据用于遍历演示
        self.head = None
        traverse_steps = self.traverse_list()
        
        # 重新编号
        for i, step in enumerate(traverse_steps):
            step["step_id"] = len(create_steps) + i + 1
        
        return create_steps + traverse_steps
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """获取所有步骤"""
        return self.run()


def run_linkedlist_algorithm(data: List[int]) -> List[Dict[str, Any]]:
    """
    运行链表算法演示的便捷函数
    
    Args:
        data: 输入的整数数组
        
    Returns:
        步骤数据列表
    """
    runner = LinkedListRunner(data)
    return runner.get_steps()
