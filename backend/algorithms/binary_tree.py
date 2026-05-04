"""
二叉树遍历算法执行器
展示二叉树的构建和三种遍历方式（前序、中序、后序）
"""
from typing import List, Dict, Any, Optional
from copy import deepcopy


class TreeNode:
    """二叉树节点"""
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
    
    def __repr__(self):
        return f"TreeNode({self.val})"


class BinaryTreeRunner:
    """
    二叉树遍历算法执行器
    
    展示二叉树的构建过程和三种遍历方式
    使用数组索引构建完全二叉树
    """
    
    def __init__(self, data: List[int]):
        """
        初始化二叉树执行器
        
        Args:
            data: 输入的整数数组，将被构造成完全二叉树
        """
        self.original_data = deepcopy(data)
        self.data = deepcopy(data)
        self.root: Optional[TreeNode] = None
        self.steps = []
        self.step_id = 0
        self.traversal_result = []
    
    def _build_tree_from_array(self, data: List[int]) -> Optional[TreeNode]:
        """
        从数组构建完全二叉树
        
        Args:
            data: 数据数组
            
        Returns:
            树的根节点
        """
        if not data:
            return None
        
        # 使用队列构建二叉树
        root = TreeNode(data[0])
        queue = [root]
        i = 1
        
        while queue and i < len(data):
            node = queue.pop(0)
            
            # 构建左子节点
            if i < len(data):
                node.left = TreeNode(data[i])
                queue.append(node.left)
                i += 1
            
            # 构建右子节点
            if i < len(data):
                node.right = TreeNode(data[i])
                queue.append(node.right)
                i += 1
        
        return root
    
    def _get_tree_structure(self, node: Optional[TreeNode], 
                           node_positions: Dict[int, tuple] = None,
                           level: int = 0, 
                           pos: int = 0,
                           x_pos: int = 0) -> List[Dict[str, Any]]:
        """
        获取树的层级结构信息（用于可视化布局）
        
        Args:
            node: 当前节点
            node_positions: 节点位置字典 {值: (层级, 水平位置)}
            level: 当前层级
            pos: 当前位置索引
            x_pos: X坐标
            
        Returns:
            节点位置信息列表
        """
        if node_positions is None:
            node_positions = {}
        
        if node is None:
            return []
        
        # 计算位置
        # 同一层节点之间用固定间隔
        nodes_in_level = 2 ** level
        spacing = 100 / (nodes_in_level + 1)
        x = spacing * (pos + 1)
        
        node_positions[node.val] = {
            "level": level,
            "x": x,
            "y": 20 + level * 80,  # 每层间隔80px
            "value": node.val,
            "children": []
        }
        
        # 递归处理左右子节点
        if node.left:
            left_pos = pos * 2
            self._get_tree_structure(node.left, node_positions, level + 1, left_pos, x_pos)
            node_positions[node.val]["children"].append(node.left.val)
        
        if node.right:
            right_pos = pos * 2 + 1
            self._get_tree_structure(node.right, node_positions, level + 1, right_pos, x_pos)
            node_positions[node.val]["children"].append(node.right.val)
        
        return node_positions
    
    def _add_step(self,
                  description: str,
                  action: str,
                  tree_data: List[int] = None,
                  tree_structure: Dict[int, Dict] = None,
                  current_node: int = None,
                  current_level: int = None,
visited_values: List[int] = None,
                  visited_order: List[int] = None,
                  highlight_nodes: List[int] = None,
                  traversal_type: str = None,
                  color_state: str = "normal") -> None:
        """
        添加一个步骤记录
        
        Args:
            description: 步骤文字描述
            action: 操作类型
            tree_data: 树的数组表示
            tree_structure: 树的结构信息
            current_node: 当前操作节点值
            current_level: 当前层级
            visited_values: 已访问的节点值列表
            visited_order: 访问顺序
            highlight_nodes: 需要高亮的节点值列表
            traversal_type: 遍历类型
            color_state: 颜色状态
        """
        self.step_id += 1
        
        step = {
            "step_id": self.step_id,
            "algorithm": "btree",
            "description": description,
            "action": action,
            "tree_data": tree_data if tree_data is not None else self.data,
            "tree_structure": tree_structure or {},
            "current_node": current_node,
            "current_level": current_level,
            "visited_values": visited_values or [],
            "visited_order": visited_order or [],
            "highlight_nodes": highlight_nodes or [],
            "traversal_type": traversal_type,
            "color_state": color_state
        }
        self.steps.append(step)
    
    def build_tree(self) -> List[Dict[str, Any]]:
        """
        构建二叉树，返回所有步骤
        
        Returns:
            步骤数据列表
        """
        self.steps = []
        self.step_id = 0
        
        # 初始化步骤
        self._add_step(
            description=f"开始构建二叉树，数据: {self.data}",
            action="init",
            tree_data=self.data,
            color_state="normal"
        )
        
        if not self.data:
            self._add_step(
                description="空数组，无法构建二叉树",
                action="error",
                tree_data=[],
                color_state="error"
            )
            return self.steps
        
        # 创建根节点
        self._add_step(
            description=f"创建根节点: {self.data[0]}",
            action="create_root",
            tree_data=self.data[:1],
            tree_structure=self._get_tree_structure(self.root) if self.root else {},
            current_node=self.data[0],
            current_level=0,
            highlight_nodes=[self.data[0]],
            color_state="comparing"
        )
        
        # 逐个添加节点
        for i, val in enumerate(self.data):
            if i == 0:
                self.root = TreeNode(val)
                structure = self._get_tree_structure(self.root)
                self._add_step(
                    description=f"节点 {val} 作为根节点",
                    action="node_added",
                    tree_data=self.data[:i+1],
                    tree_structure=structure,
                    current_node=val,
                    highlight_nodes=[val],
                    color_state="completed"
                )
            else:
                # 找到插入位置
                parent_idx = (i - 1) // 2
                is_left = i % 2 == 1
                parent_val = self.data[parent_idx]
                side = "左" if is_left else "右"
                
                self._add_step(
                    description=f"添加节点 {val}",
                    action="add_start",
                    tree_data=self.data[:i+1],
                    tree_structure=self._get_tree_structure(self.root),
                    current_node=val,
                    highlight_nodes=[val, parent_val],
                    color_state="comparing"
                )
                
                # 实际插入
                self.root = self._build_tree_from_array(self.data[:i+1])
                
                self._add_step(
                    description=f"节点 {val} 作为 {parent_val} 的{side}子节点添加完成",
                    action="node_added",
                    tree_data=self.data[:i+1],
                    tree_structure=self._get_tree_structure(self.root),
                    current_node=val,
                    highlight_nodes=[val, parent_val],
                    color_state="completed"
                )
        
        # 构建完成
        structure = self._get_tree_structure(self.root)
        self._add_step(
            description=f"二叉树构建完成！共{len(self.data)}个节点",
            action="complete",
            tree_data=self.data,
            tree_structure=structure,
            color_state="completed"
        )
        
        return self.steps
    
    def _preorder(self, node: Optional[TreeNode], visited: List[int]) -> List[int]:
        """
        前序遍历：根-左-右
        
        Args:
            node: 当前节点
            visited: 已访问节点列表
        """
        if node is None:
            return visited
        
        visited.append(node.val)
        self._add_step(
            description=f"前序遍历：访问根节点 {node.val}",
            action="visit_root",
            tree_data=self.data,
            tree_structure=self._get_tree_structure(self.root),
            current_node=node.val,
            visited_values=visited.copy(),
            visited_order=visited.copy(),
            highlight_nodes=[node.val],
            traversal_type="preorder",
            color_state="comparing"
        )
        
        self._preorder(node.left, visited)
        self._preorder(node.right, visited)
        
        return visited
    
    def _inorder(self, node: Optional[TreeNode], visited: List[int]) -> List[int]:
        """
        中序遍历：左-根-右
        
        Args:
            node: 当前节点
            visited: 已访问节点列表
        """
        if node is None:
            return visited
        
        self._inorder(node.left, visited)
        visited.append(node.val)
        
        self._add_step(
            description=f"中序遍历：访问根节点 {node.val}",
            action="visit_root",
            tree_data=self.data,
            tree_structure=self._get_tree_structure(self.root),
            current_node=node.val,
            visited_values=visited.copy(),
            visited_order=visited.copy(),
            highlight_nodes=[node.val],
            traversal_type="inorder",
            color_state="comparing"
        )
        
        self._inorder(node.right, visited)
        
        return visited
    
    def _postorder(self, node: Optional[TreeNode], visited: List[int]) -> List[int]:
        """
        后序遍历：左-右-根
        
        Args:
            node: 当前节点
            visited: 已访问节点列表
        """
        if node is None:
            return visited
        
        self._postorder(node.left, visited)
        self._postorder(node.right, visited)
        visited.append(node.val)
        
        self._add_step(
            description=f"后序遍历：访问根节点 {node.val}",
            action="visit_root",
            tree_data=self.data,
            tree_structure=self._get_tree_structure(self.root),
            current_node=node.val,
            visited_values=visited.copy(),
            visited_order=visited.copy(),
            highlight_nodes=[node.val],
            traversal_type="postorder",
            color_state="comparing"
        )
        
        return visited
    
    def traverse(self, traversal_type: str = "preorder") -> List[Dict[str, Any]]:
        """
        执行二叉树遍历
        
        Args:
            traversal_type: 遍历类型 (preorder, inorder, postorder)
            
        Returns:
            步骤数据列表
        """
        self.steps = []
        self.step_id = 0
        
        # 首先构建树
        self.root = self._build_tree_from_array(self.data)
        
        type_names = {
            "preorder": "前序遍历（根-左-右）",
            "inorder": "中序遍历（左-根-右）",
            "postorder": "后序遍历（左-右-根）"
        }
        
        # 初始化步骤
        self._add_step(
            description=f"开始{type_names.get(traversal_type, traversal_type)}",
            action="init",
            tree_data=self.data,
            tree_structure=self._get_tree_structure(self.root),
            traversal_type=traversal_type,
            color_state="normal"
        )
        
        # 执行遍历
        visited = []
        if traversal_type == "preorder":
            self._preorder(self.root, visited)
        elif traversal_type == "inorder":
            self._inorder(self.root, visited)
        elif traversal_type == "postorder":
            self._postorder(self.root, visited)
        
        # 遍历完成
        self._add_step(
            description=f"{type_names.get(traversal_type, traversal_type)}完成！访问顺序: {visited}",
            action="complete",
            tree_data=self.data,
            tree_structure=self._get_tree_structure(self.root),
            visited_values=visited.copy(),
            visited_order=visited.copy(),
            traversal_type=traversal_type,
            color_state="completed"
        )
        
        return self.steps
    
    def run(self, traversal_type: str = "preorder") -> List[Dict[str, Any]]:
        """
        运行完整的二叉树演示（构建+遍历）
        
        Args:
            traversal_type: 遍历类型
            
        Returns:
            步骤数据列表
        """
        build_steps = self.build_tree()
        
        # 重置用于遍历
        self.root = self._build_tree_from_array(self.original_data)
        traverse_steps = self.traverse(traversal_type)
        
        # 重新编号
        for i, step in enumerate(traverse_steps):
            step["step_id"] = len(build_steps) + i + 1
        
        return build_steps + traverse_steps
    
    def get_steps(self, traversal_type: str = "preorder") -> List[Dict[str, Any]]:
        """获取所有步骤"""
        return self.run(traversal_type)


def run_btree_algorithm(data: List[int], traversal_type: str = "preorder") -> List[Dict[str, Any]]:
    """
    运行二叉树算法演示的便捷函数
    
    Args:
        data: 输入的整数数组
        traversal_type: 遍历类型
        
    Returns:
        步骤数据列表
    """
    runner = BinaryTreeRunner(data)
    return runner.get_steps(traversal_type)
