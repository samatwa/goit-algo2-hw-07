import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


# Функція для обчислення чисел Фібоначчі з використанням Splay Tree
class Node:
    """Вузол дерева."""

    def __init__(self, key, value, parent=None):
        self.key = key
        self.data = value
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    """Дерево з сплаюванням."""

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставка нового елемента в дерево."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        """Рекурсивна вставка елемента в дерево."""
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
        else:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)

    def find(self, key):
        """Пошук елемента в дереві із застосуванням сплаювання."""
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None  # Якщо елемент не знайдено.

    def _splay(self, node):
        """Реалізація сплаювання для переміщення вузла до кореня."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig-ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


# Функція Фібоначчі з використанням Splay Tree
def fibonacci_splay(n, tree):
    cached = tree.find(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val


# Функція Фібоначчі з використанням @lru_cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Вимірювання часу
test_values = list(range(0, 501, 50))
lru_times = []
splay_times = []

for n in test_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=5) / 5
    tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=5) / 5
    lru_times.append(lru_time)
    splay_times.append(splay_time)

# Побудова графіка
plt.plot(test_values, lru_times, label="LRU Cache", marker="o")
plt.plot(test_values, splay_times, label="Splay Tree", marker="s")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Виведення таблиці
print(f"{'n':<10} {'LRU Cache Time (s)':<22} {'Splay Tree Time (s)':<22}")
print("-" * 54)
for i in range(len(test_values)):
    print(f"{test_values[i]:<10} {lru_times[i]:<22.10f} {splay_times[i]:<22.10f}")
