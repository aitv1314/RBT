RBT_RED = 0
RBT_BLACK = 1

"""
红黑树是一棵二叉树， 有五大特征：
特征一： 节点要么是红色，要么是黑色（红黑树名字由来）。
特征二： 根节点是黑色的
特征三： 每个叶节点(nil或空节点)是黑色的。
特征四： 每个红色节点的两个子节点都是黑色的（相连的两个节点不能都是红色的）。
特征五： 从任一个节点到其每个叶子节点的所有路径都是包含相同数量的黑色节点。
"""


class RBTNode():
    def __init__(self, val, left, right, color):
        self.val = val
        self.left = left
        self.right = right
        self.parent = None
        self.color = color

    def __lt__(self, other):
        return self.val < other.val

    def __eq__(self, other):
        return other is not None and self.val == other.val

    def SetChild(self, nd, left):
        if left:
            self.left = nd
        else:
            self.right = nd
        if nd is not None:
            nd.parent = self
        return

    def GetChild(self, left):
        if left:
            return self.left
        else:
            return self.right

    def IsBlack(self):
        return self.color

    def SetColor(self, color):
        self.color = color
        return


class RBTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, node):
        """
        左旋做了3件事
        1.右孩子的左孩子赋给node的右节点
        2.右孩子的左孩子设为node
        3.右孩子的父亲设为node的父亲（非空）
        :param node:
        :return:
        """
        print("left_rotate", node.val)
        # 中间变量接一下
        right = node.right
        parent = node.parent
        # 第一步：node的右节点挂上右孩子的左节点，同时维护右孩子左节点的父亲
        node.right = right.left
        if node.right:
            right.left.parent = node
        # 第二步：右节点的左孩子挂上node，同时维护node的父亲
        right.left = node
        node.parent = right
        # 第三步：右孩子挂在node的parent下
        right.parent = parent
        if not parent:
            # node没有parent，说明node上一级是root
            self.root = parent
        else:
            if parent.left == node:
                # 如果原来node在左边，现在也挂到左边
                parent.left = right
            else:
                parent.right = right
        pass

    def right_rotate(self, node):
        """
        1.node放到左孩子右节点上
        2.node左孩子的右孩子放到node左孩子上
        3.node父亲（非空）作为node左孩子的父亲
        :param node:
        :return:
        """
        print("right_rotate", node.val)
        #中间节点接一下
        parent = node.parent
        left = node.left
        #第一步
        left.right = node
        node.parent = left.right
        #第二步
        node.left = left.right
        if left.right:
            left.right.parent = node
        #第三步
        left.parent = parent
        if not parent:
            self.root = left
        else:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left
        pass

    def insert(self, node):
        """
        0.每次插入只插入红色节点
        1.插入的是根节点，直接变为黑色节点
        2.插入的节点的父节点是黑色节点，则不调整
        3.
        :param node:
        :return:
        """