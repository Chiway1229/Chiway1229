"""雙向鏈結串列互動操作程式。

單一檔案即可執行：python3 dll_program.py
依照選單輸入數字，就能新增、刪除、搜尋、反轉串列，
每次操作後都會印出目前的串列結構。
"""


class Node:
    """串列中的單一節點，記錄值以及前、後兩個鄰居。"""

    def __init__(self, value=None):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """以頭尾哨兵實作的雙向鏈結串列。"""

    def __init__(self):
        self.head = Node()  # 哨兵，第一個真正的節點是 head.next
        self.tail = Node()  # 哨兵，最後一個真正的節點是 tail.prev
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _link_before(self, node, value):
        """在 node 前面插入新節點。O(1)"""
        new = Node(value)
        new.prev = node.prev
        new.next = node
        node.prev.next = new
        node.prev = new
        self.size += 1

    def _unlink(self, node):
        """把 node 從串列中拆下並回傳它的值。O(1)"""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node.value

    def _node_at(self, index):
        """依索引取得節點，從離目標較近的一端開始走。O(n)"""
        if not 0 <= index < self.size:
            raise IndexError("索引超出範圍")
        if index < self.size // 2:
            node = self.head.next
            for _ in range(index):
                node = node.next
        else:
            node = self.tail.prev
            for _ in range(self.size - 1 - index):
                node = node.prev
        return node

    def append(self, value):
        self._link_before(self.tail, value)

    def appendleft(self, value):
        self._link_before(self.head.next, value)

    def insert(self, index, value):
        if index >= self.size:
            self.append(value)
        else:
            self._link_before(self._node_at(max(0, index)), value)

    def pop(self):
        if self.size == 0:
            raise IndexError("串列是空的")
        return self._unlink(self.tail.prev)

    def popleft(self):
        if self.size == 0:
            raise IndexError("串列是空的")
        return self._unlink(self.head.next)

    def remove(self, value):
        node = self.head.next
        while node is not self.tail:
            if node.value == value:
                self._unlink(node)
                return
            node = node.next
        raise ValueError(f"找不到 {value!r}")

    def index(self, value):
        for i, item in enumerate(self.forward()):
            if item == value:
                return i
        return -1

    def reverse(self):
        """把每個節點（含哨兵）的 prev、next 對調，再交換頭尾哨兵。O(n)"""
        node = self.head
        while node is not None:
            node.prev, node.next = node.next, node.prev
            node = node.prev
        self.head, self.tail = self.tail, self.head

    def forward(self):
        node = self.head.next
        while node is not self.tail:
            yield node.value
            node = node.next

    def backward(self):
        node = self.tail.prev
        while node is not self.head:
            yield node.value
            node = node.prev

    def __len__(self):
        return self.size

    def __str__(self):
        return " <-> ".join(["head", *map(repr, self.forward()), "tail"])


def parse_value(text):
    """把輸入轉成整數或浮點數，轉不了就保留字串。"""
    for convert in (int, float):
        try:
            return convert(text)
        except ValueError:
            pass
    return text


MENU = """
========== 雙向鏈結串列 ==========
 1. 從尾端新增       2. 從頭端新增
 3. 插入到指定位置   4. 刪除尾端
 5. 刪除頭端         6. 刪除指定值
 7. 搜尋值的位置     8. 反轉串列
 9. 正向與反向走訪   0. 離開
=================================="""


def main():
    dll = DoublyLinkedList()
    for value in (10, 20, 30):
        dll.append(value)

    while True:
        print(MENU)
        print(f"目前串列（長度 {len(dll)}）：{dll}")
        choice = input("請選擇功能：").strip()

        try:
            if choice == "1":
                dll.append(parse_value(input("要新增的值：")))
            elif choice == "2":
                dll.appendleft(parse_value(input("要新增的值：")))
            elif choice == "3":
                text = input("插入位置（從 0 開始）：").strip()
                if not text.isdigit():
                    raise ValueError("位置必須是 0 以上的整數")
                index = int(text)
                dll.insert(index, parse_value(input("要插入的值：")))
            elif choice == "4":
                print(f"已刪除 {dll.pop()!r}")
            elif choice == "5":
                print(f"已刪除 {dll.popleft()!r}")
            elif choice == "6":
                value = parse_value(input("要刪除的值："))
                dll.remove(value)
                print(f"已刪除 {value!r}")
            elif choice == "7":
                value = parse_value(input("要搜尋的值："))
                position = dll.index(value)
                if position == -1:
                    print(f"找不到 {value!r}")
                else:
                    print(f"{value!r} 在索引 {position}")
            elif choice == "8":
                dll.reverse()
                print("已反轉")
            elif choice == "9":
                print("正向：", list(dll.forward()))
                print("反向：", list(dll.backward()))
            elif choice == "0":
                print("再見！")
                break
            else:
                print("請輸入 0 到 9 的數字")
        except (IndexError, ValueError) as error:
            print(f"錯誤：{error}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n程式結束")
