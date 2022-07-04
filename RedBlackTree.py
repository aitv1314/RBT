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


class RBTNode:
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

    def set_child(self, nd, left):
        if left:
            self.left = nd
        else:
            self.right = nd
        if nd is not None:
            nd.parent = self
        return

    def get_child(self, left):
        if left:
            return self.left
        else:
            return self.right

    def is_black(self):
        return self.color

    def set_color(self, color):
        self.color = color
        return


class RBTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, n):
        """
        左旋做了3件事
        1.右孩子的左孩子赋给node的右节点
        2.右孩子的左孩子设为node
        3.右孩子的父亲设为node的父亲（非空）
        :param n:
        :return:
        """
        print("left_rotate", n.val)
        # 中间变量接一下
        r = n.right
        p = n.parent
        # 第一步：node的右节点挂上右孩子的左节点，同时维护右孩子左节点的父亲
        n.right = r.left
        if n.right:
            r.left.parent = n
        # 第二步：右节点的左孩子挂上node，同时维护node的父亲
        r.left = n
        n.parent = r
        # 第三步：右孩子挂在node的parent下
        r.parent = p
        if not p:
            # node没有parent，说明node上一级是root
            self.root = p
        else:
            if p.left == n:
                # 如果原来node在左边，现在也挂到左边
                p.left = r
            else:
                p.right = r
        pass

    def right_rotate(self, n):
        """
        1.node放到左孩子右节点上
        2.node左孩子的右孩子放到node左孩子上
        3.node父亲（非空）作为node左孩子的父亲
        :param n:
        :return:
        """
        print("right_rotate", n.val)
        # 中间节点接一下
        p = n.parent
        l = n.left
        # 第一步
        l.right = n
        n.parent = l.right
        # 第二步
        n.left = l.right
        if l.right:
            l.right.parent = n
        # 第三步
        l.parent = p
        if not p:
            self.root = l
        else:
            if p.left == n:
                p.left = l
            else:
                p.right = l
        pass

    def insert_fixup(self, n):
        while n.parent.color == RBT_RED:
            if n.parent == n.parent.parent.left:
                # 叔叔节点
                u = n.parent.parent.right
                if u.color == RBT_RED:
                    n.parent.color = RBT_BLACK
                    u.color = RBT_BLACK
                    n.parent.parent = RBT_RED
                    n = n.parent.parent
                elif n == n.parent.right:
                    n = n.parent
                    self.left_rotate(n)
                else:
                    n.parent.color = RBT_BLACK
                    n.parent.parent.color = RBT_RED
                    self.right_rotate(n.parent.parent)
            else:
                # 同上
                u = n.parent.parent.left
                if u.color == RBT_RED:
                    n.parent.color = RBT_BLACK
                    u.color = RBT_BLACK
                    n.parent.parent = RBT_RED
                    n = n.parent.parent
                elif n == n.parent.left:
                    n = n.parent
                    self.right_rotate(n)
                else:
                    n.parent.color = RBT_BLACK
                    n.parent.parent.color = RBT_RED
                    self.left_rotate(n.parent.parent)
        self.root.color = RBT_BLACK
        pass

    def insert(self, n):
        """
        0.每次插入只插入红色节点
        1.插入的是根节点，直接变为黑色节点
        2.插入的节点的父节点是黑色节点，则不调整
        3.插入的节点父节点时红色节点，调用insert_fixup调整整颗树，重新平衡
        :param n:
        :return:
        """
        x = self.root
        y = None
        if x is not None:
            y = x
            if x.val > n.val:
                x = x.left
            else:
                x = x.right
        n.parent = y
        if y is None:
            self.root = n
        elif y.val > n.val:
            n.parent.left = n
        else:
            y.right = n
        n.right = None
        n.left = None
        n.color = RBT_RED
        self.insert_fixup(n)
        pass

    def rbt_transplant(self, u, v):
        # 将u.parent下挂的u节点更换成v
        if u.p is None:
            self.root = u
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
        pass

    def tree_minmum(self, node):
        # 查找后继
        while node.left is not None:
            node = node.left
        return node

    def rbt_delete_fixup(self, n):
        # 修复删除后的树
        while n is not self.root and n.color == RBT_BLACK:
            if n == n.parent.left:
                w = n.parent.right
                # 情况1--》可以转化为情况2、3、4：x的兄弟节点w是红色
                if w.color == RBT_RED:
                    w.color = RBT_BLACK
                    n.parent.color = RBT_RED
                    self.left_rotate(n.parent)
                # 情况2：x的兄弟节点w是黑色，而且w的两个子节点都是黑色的
                if w.left.color == RBT_BLACK and w.right.color == RBT_BLACK:
                    w.color = RBT_RED
                    n = n.p
                else:
                    # 情况3--》可以转化为情况4：x的兄弟节点w是黑色的，w的左孩子节点是红色的，w的右孩子节点是黑色的
                    if w.right.color == RBT_BLACK:
                        w.left.color = RBT_BLACK
                        w.color = RBT_RED
                        self.right_rotate(w)
                    # 情况4：x的兄弟节点w是褐色的，且w的右孩子是红色的
                    w.color = n.parent.color
                    n.parent.color = RBT_BLACK
                    w.right.color = RBT_BLACK
                    n = self.root
            else:
                w = n.parent.left
                # 情况1--》可以转化为情况2、3、4：x的兄弟节点w是红色
                if w.color == RBT_RED:
                    w.color = RBT_BLACK
                    n.parent.color = RBT_RED
                    self.right_rotate(n.parent)
                # 情况2：x的兄弟节点w是黑色，而且w的两个子节点都是黑色的
                if w.right.color == RBT_BLACK and w.left.color == RBT_BLACK:
                    w.color = RBT_RED
                    n = n.p
                else:
                    # 情况3--》可以转化为情况4：x的兄弟节点w是黑色的，w的左孩子节点是红色的，w的右孩子节点是黑色的
                    if w.left.color == RBT_BLACK:
                        w.right.color = RBT_BLACK
                        w.color = RBT_RED
                        self.right_rotate(w)
                    # 情况4：x的兄弟节点w是褐色的，且w的右孩子是红色的
                    w.color = n.parent.color
                    n.parent.color = RBT_BLACK
                    w.left.color = RBT_BLACK
                    n = self.root
        n.color = RBT_BLACK
        pass

    def delete(self, n):
        y = n
        y_original_color = y.color
        if n.left is None:
            x = n.right
            self.rbt_transplant(n, n.right)
        elif n.right is None:
            x = n.left
            self.rbt_transplant(n, n.right)
        else:
            """后继节点：就是一个节点在中序遍历中的下一个节点。
            在中序遍历中，如果该节点有右子树，该节点的后继节点，就是再二叉树中，该节点的右子树中，最左的节点。 
            当x节点没有右子树，就去查找x是哪个节点的左子树"""
            y = self.tree_minumum(n.right)
            y_original_color = y.color
            x = y.right
            if y.parent == n:
                x.p = y
            else:
                self.rbt_transplant(y, y.right)
                y.right = n.right
                y.right.parent = y
            self.rbt_transplant(n, y)
            y.left = n.left
            n.left.parent = y
            y.color = n.color
        if y_original_color == RBT_BLACK:
            self.rbt_delete_fixup(x)
        pass
