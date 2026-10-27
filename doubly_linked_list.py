"""雙向鏈結串列（Doubly Linked List）教學用實作。

設計重點：
1. 頭尾各放一個哨兵節點（sentinel），串列永遠至少有兩個節點，
   插入與刪除時不用特別處理「空串列」或「動到頭尾」的情況。
2. 所有改指標的動作只集中在 _link_before 與 _unlink 兩個方法，
   其他公開方法都建立在它們之上，同樣的指標邏輯只寫一次。
3. 介面命名比照內建 list 與 collections.deque，學生可以用熟悉的方式操作。

結構示意（H、T 為哨兵，不存資料）：

    H <-> [1] <-> [2] <-> [3] <-> T
"""

from collections.abc import Iterable, Iterator
from typing import Any


class Node:
    """串列中的單一節點，記錄值以及前、後兩個鄰居。"""

    __slots__ = ("value", "prev", "next")

    def __init__(self, value: Any = None) -> None:
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class DoublyLinkedList:
    """以頭尾哨兵實作的雙向鏈結串列。"""

    def __init__(self, iterable: Iterable[Any] = ()) -> None:
        self._head = Node()  # 第一個真正的節點是 self._head.next
        self._tail = Node()  # 最後一個真正的節點是 self._tail.prev
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for value in iterable:
            self.append(value)

    # ------------------------------------------------------------
    # 核心指標操作：只有這兩個方法會修改 prev / next
    # ------------------------------------------------------------

    def _link_before(self, node: Node, value: Any) -> Node:
        """在 node 前面插入一個新節點並回傳它。O(1)"""
        new = Node(value)
        new.prev = node.prev
        new.next = node
        node.prev.next = new
        node.prev = new
        self._size += 1
        return new

    def _unlink(self, node: Node) -> Any:
        """把 node 從串列中拆下並回傳它的值。O(1)"""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None  # 切斷舊連結，避免被誤用
        self._size -= 1
        return node.value

    # ------------------------------------------------------------
    # 走訪輔助
    # ------------------------------------------------------------

    def _node_at(self, index: int) -> Node:
        """依索引取得節點，支援負索引。O(n)

        雙向串列可以往回走，所以從離目標較近的那一端出發，
        最多只需要走 n/2 步。
        """
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("索引超出範圍")

        if index < self._size // 2:
            node = self._head.next
            for _ in range(index):
                node = node.next
        else:
            node = self._tail.prev
            for _ in range(self._size - 1 - index):
                node = node.prev
        return node

    def _find_node(self, value: Any) -> Node | None:
        """回傳第一個值等於 value 的節點，找不到時回傳 None。O(n)"""
        node = self._head.next
        while node is not self._tail:
            if node.value == value:
                return node
            node = node.next
        return None

    # ------------------------------------------------------------
    # 新增
    # ------------------------------------------------------------

    def append(self, value: Any) -> None:
        """加到尾端。O(1)"""
        self._link_before(self._tail, value)

    def appendleft(self, value: Any) -> None:
        """加到頭端。O(1)"""
        self._link_before(self._head.next, value)

    def insert(self, index: int, value: Any) -> None:
        """插入到 index 的位置。O(n)

        行為比照 list.insert：索引超出範圍時，直接放到頭或尾。
        """
        if index < 0:
            index = max(0, index + self._size)
        if index >= self._size:
            self.append(value)
        else:
            self._link_before(self._node_at(index), value)

    # ------------------------------------------------------------
    # 刪除
    # ------------------------------------------------------------

    def pop(self, index: int = -1) -> Any:
        """移除並回傳 index 位置的值，預設為最後一個。頭尾 O(1)，中間 O(n)"""
        return self._unlink(self._node_at(index))

    def popleft(self) -> Any:
        """移除並回傳第一個值。O(1)"""
        return self.pop(0)

    def remove(self, value: Any) -> None:
        """移除第一個值等於 value 的節點。O(n)"""
        node = self._find_node(value)
        if node is None:
            raise ValueError(f"{value!r} 不在串列中")
        self._unlink(node)

    def clear(self) -> None:
        """清空串列。O(1)"""
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    # ------------------------------------------------------------
    # 查詢與變形
    # ------------------------------------------------------------

    def index(self, value: Any) -> int:
        """回傳第一個值等於 value 的索引。O(n)"""
        for i, item in enumerate(self):
            if item == value:
                return i
        raise ValueError(f"{value!r} 不在串列中")

    def reverse(self) -> None:
        """原地反轉。O(n)

        把每個節點（含兩個哨兵）的 prev 與 next 對調，
        最後再把頭尾哨兵的身分互換即可。
        """
        node = self._head
        while node is not None:
            node.prev, node.next = node.next, node.prev
            node = node.prev  # 對調後，原本的 next 存在 prev 裡
        self._head, self._tail = self._tail, self._head

    # ------------------------------------------------------------
    # Python 協定：讓串列能用 len()、for、in、[]、== 等語法
    # ------------------------------------------------------------

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        node = self._head.next
        while node is not self._tail:
            yield node.value
            node = node.next

    def __reversed__(self) -> Iterator[Any]:
        node = self._tail.prev
        while node is not self._head:
            yield node.value
            node = node.prev

    def __contains__(self, value: Any) -> bool:
        return self._find_node(value) is not None

    def __getitem__(self, index: int) -> Any:
        return self._node_at(index).value

    def __setitem__(self, index: int, value: Any) -> None:
        self._node_at(index).value = value

    def __delitem__(self, index: int) -> None:
        self._unlink(self._node_at(index))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DoublyLinkedList):
            return NotImplemented
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __repr__(self) -> str:
        return f"DoublyLinkedList([{', '.join(map(repr, self))}])"

    def __str__(self) -> str:
        """畫出串列結構，上課示範時比較直觀。"""
        return " <-> ".join(["head", *map(repr, self), "tail"])


if __name__ == "__main__":
    dll = DoublyLinkedList([1, 2, 3])
    print(dll)                 # head <-> 1 <-> 2 <-> 3 <-> tail

    dll.appendleft(0)
    dll.append(4)
    dll.insert(2, 1.5)
    print(dll)                 # head <-> 0 <-> 1 <-> 1.5 <-> 2 <-> 3 <-> 4 <-> tail

    print(dll.pop())           # 4
    print(dll.popleft())       # 0
    dll.remove(1.5)
    print(dll[-1], len(dll))   # 3 3

    dll.reverse()
    print(repr(dll))           # DoublyLinkedList([3, 2, 1])
    print(list(reversed(dll))) # [1, 2, 3]
