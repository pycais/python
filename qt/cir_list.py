class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None  # 添加指向前一个节点的指针


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.current = None  # 用于追踪当前节点

    def append(self, key, value):
        new_node = Node(key, value)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.prev = current
            new_node.next = self.head
            self.head.prev = new_node

    def next(self):
        if self.current is None:
            self.current = self.head
        else:
            self.current = self.current.next
        return self.current.key, self.current.value

    def previous(self):
        if self.current is None:
            self.current = self.head
        else:
            self.current = self.current.prev
        return self.current.key, self.current.value

    def find(self, key):
        current = self.head
        if self.head:
            while True:
                if current.key == key:
                    return current.value
                current = current.next
                if current == self.head:
                    break
        return None

    def display(self):
        nodes = []
        current = self.head
        if self.head:
            while True:
                nodes.append(f"{current.key}: {current.value}")
                current = current.next
                if current == self.head:
                    break
        print(" -> ".join(nodes))


if __name__ == '__main__':

    # 示例使用
    cll = CircularLinkedList()
    cll.append(1, "value1")
    cll.append(2, "value2")
    cll.append(3, "value3")
    cll.append(4, "value4")
    cll.display()  # 输出: 1: value1 -> 2: value2 -> 3: value3 -> 4: value4

    # 迭代测试
    print(cll.next())  # 输出: (1, 'value1')
    print(cll.next())  # 输出: (2, 'value2')
    print(cll.previous())  # 输出: (1, 'value1')
    print(cll.previous())  # 输出: (4, 'value4')
    from collections import OrderedDict

    qq = OrderedDict({'a': 2, 'd': 3, 'c': 2})
    print(qq)
