import unittest

from doubly_linked_list import DoublyLinkedList


class DoublyLinkedListTest(unittest.TestCase):
    def assertStructure(self, dll, expected):
        """同時檢查順向、逆向走訪與長度，確認 prev / next 沒有接錯。"""
        self.assertEqual(list(dll), expected)
        self.assertEqual(list(reversed(dll)), expected[::-1])
        self.assertEqual(len(dll), len(expected))

    def test_empty(self):
        dll = DoublyLinkedList()
        self.assertStructure(dll, [])
        self.assertFalse(dll)
        with self.assertRaises(IndexError):
            dll.pop()
        with self.assertRaises(IndexError):
            dll.popleft()

    def test_append_and_appendleft(self):
        dll = DoublyLinkedList()
        dll.append(2)
        dll.append(3)
        dll.appendleft(1)
        self.assertStructure(dll, [1, 2, 3])

    def test_insert_matches_list(self):
        for index in (-10, -2, 0, 1, 3, 10):
            expected = [1, 2, 3]
            dll = DoublyLinkedList(expected)
            expected.insert(index, "x")
            dll.insert(index, "x")
            self.assertStructure(dll, expected)

    def test_pop(self):
        dll = DoublyLinkedList([1, 2, 3, 4, 5])
        self.assertEqual(dll.pop(), 5)
        self.assertEqual(dll.popleft(), 1)
        self.assertEqual(dll.pop(1), 3)
        self.assertStructure(dll, [2, 4])

    def test_remove_and_index(self):
        dll = DoublyLinkedList([1, 2, 3, 2])
        self.assertEqual(dll.index(2), 1)
        dll.remove(2)
        self.assertStructure(dll, [1, 3, 2])
        with self.assertRaises(ValueError):
            dll.remove(99)
        with self.assertRaises(ValueError):
            dll.index(99)

    def test_indexing_from_both_ends(self):
        values = list(range(7))
        dll = DoublyLinkedList(values)
        for i in range(-7, 7):
            self.assertEqual(dll[i], values[i])
        with self.assertRaises(IndexError):
            dll[7]
        with self.assertRaises(IndexError):
            dll[-8]

    def test_setitem_and_delitem(self):
        dll = DoublyLinkedList([1, 2, 3])
        dll[1] = 20
        del dll[0]
        self.assertStructure(dll, [20, 3])

    def test_contains_and_eq(self):
        dll = DoublyLinkedList([1, 2, 3])
        self.assertIn(2, dll)
        self.assertNotIn(4, dll)
        self.assertEqual(dll, DoublyLinkedList([1, 2, 3]))
        self.assertNotEqual(dll, DoublyLinkedList([1, 2]))
        self.assertNotEqual(dll, [1, 2, 3])

    def test_reverse(self):
        dll = DoublyLinkedList([1, 2, 3, 4])
        dll.reverse()
        self.assertStructure(dll, [4, 3, 2, 1])
        dll.append(0)
        dll.appendleft(5)
        self.assertStructure(dll, [5, 4, 3, 2, 1, 0])

    def test_reverse_empty(self):
        dll = DoublyLinkedList()
        dll.reverse()
        self.assertStructure(dll, [])

    def test_clear(self):
        dll = DoublyLinkedList([1, 2, 3])
        dll.clear()
        self.assertStructure(dll, [])
        dll.append(1)
        self.assertStructure(dll, [1])

    def test_str_and_repr(self):
        dll = DoublyLinkedList([1, "a"])
        self.assertEqual(str(dll), "head <-> 1 <-> 'a' <-> tail")
        self.assertEqual(repr(dll), "DoublyLinkedList([1, 'a'])")


if __name__ == "__main__":
    unittest.main()
