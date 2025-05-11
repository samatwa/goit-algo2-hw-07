import time
import random


class Node:
    """
    Клас Node представляє вузол двусвязного списку.
    Він містить ключ, значення та посилання на наступний і попередній вузли.
    """

    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Клас DoublyLinkedList представляє двусвязний список.
    Він містить посилання на голову та хвіст списку.
    Методи включають додавання вузлів, видалення вузлів, переміщення вузлів на початок списку та видалення останнього вузла.
    """

    def __init__(self):
        """
        Ініціалізація двусвязного списку з головою та хвостом, які спочатку є None.
        """

        self.head = None
        self.tail = None

    def push(self, key, value):
        """
        Додає новий вузол на початок списку.
        Якщо список порожній, оновлює хвіст списку.
        Якщо список не порожній, оновлює попередній вузол голови.
        """

        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        """
        Видаляє вузол зі списку.
        Якщо вузол є головою або хвостом списку, оновлює відповідні посилання.
        """

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        """
        Переміщує вузол на початок списку.
        Якщо вузол вже є головою, нічого не робить.
        Якщо вузол не є головою, видаляє його з поточної позиції та додає на початок списку.
        """

        if node != self.head:
            self.remove(node)
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_last(self):
        """
        Видаляє останній вузол зі списку.
        """

        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


# This class implements an LRU (Least Recently Used) Cache using a dictionary and a doubly linked list.
class LRUCache:
    """
    Клас LRUCache реалізує кеш LRU (Least Recently Used) за допомогою словника та двусвязного списку.
    Він містить методи для отримання значення за ключем, додавання нового ключа-значення та видалення найменш використовуваного елемента.
    """

    def __init__(self, capacity):
        """
        Ініціалізація кешу з максимальною ємністю.
        """

        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        """
        Отримує значення за ключем з кешу.
        Якщо ключ не існує, повертає -1.
        """

        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        """
        Додає новий ключ-значення до кешу. Якщо ключ вже існує, оновлює його значення.
        Якщо кеш досягнув максимальної ємності, видаляє найменш використовуваний елемент.
        """
        # Якщо ключ вже існує, оновлюємо його значення та переміщуємо його на початок списку
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        # Якщо ключ не існує, додаємо його до кешу
        # Якщо кеш досягнув максимальної ємності, видаляємо найменш використовуваний елемент
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

    def invalidate_affected_ranges(self, index):
        """
        Інвалідація всіх відрізків у кеші, які включають вказаний індекс.
        Цей метод видаляє всі ключі, які містять оновлений індекс.
        Це необхідно для того, щоб уникнути повернення застарілих значень з кешу.
        """
        keys_to_remove = []

        for key in self.cache:
            # Перевіряємо, чи є ключ кортежем (L, R) і чи включає він індекс
            if isinstance(key, tuple) and len(key) == 2:
                L, R = key
                if L <= index <= R:
                    keys_to_remove.append(key)

        # Видаляємо всі ключі, які містять оновлений індекс
        for key in keys_to_remove:
            if key in self.cache:
                node = self.cache[key]
                self.list.remove(node)
                del self.cache[key]


# Обчислення без кешу


def range_sum_no_cache(array: list, L: int, R: int) -> int:
    """
    Ця функція обчислює суму чисел у масиві з L до R без використання кешу.
    """
    return sum(array[L : R + 1])


def update_no_cache(array: list, index: int, value: int) -> None:
    """
    Ця функція оновлює значення елемента у масиві за індексом index без використання кешу.
    """
    array[index] = value


# Обчислення з кешем

# Ініціалізація кешу з максимальною ємністю 1000
lru_cache_object = LRUCache(1000)


def range_sum_with_cache(array: list, L: int, R: int) -> int:
    """
    Ця функція обчислює суму чисел у масиві з L до R з використанням кешу.
    Якщо результат вже є в кеші, він повертається з кешу.
    """
    cache_key = (L, R)
    result = lru_cache_object.get(cache_key)
    if result is not None:
        return result
    result = sum(array[L : R + 1])
    lru_cache_object.put(cache_key, result)
    return result


def update_with_cache(array: list, index: int, value: int) -> None:
    """
    Ця функція оновлює значення елемента у масиві за індексом index з використанням кешу.
    Якщо оновлення впливає на кеш, то відповідні відрізки в кеші інвалідуються.
    """
    array[index] = value

    # Інвалідуємо всі відрізки в кеші, які включають оновлений індекс
    lru_cache_object.invalidate_affected_ranges(index)


def main():
    # Генерація даних
    N = 100000
    Q = 50000

    # Генерація масиву з N випадкових чисел
    array_no_cache = [random.randint(1, 100) for _ in range(N)]
    array_with_cache = array_no_cache.copy()

    # Генерація Q випадкових запитів
    queries = []
    for _ in range(Q):
        if random.random() < 0.5:
            L = random.randint(0, N - 2)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            idx = random.randint(0, N - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))

    # Виконання без кешу
    start_time = time.time()
    for op in queries:
        if op[0] == "Range":
            range_sum_no_cache(array_no_cache, op[1], op[2])
        else:
            update_no_cache(array_no_cache, op[1], op[2])
    end_time = time.time()
    no_cache_time = round(end_time - start_time, 2)

    # Виконання з кешем
    start_time = time.time()
    for op in queries:
        if op[0] == "Range":
            range_sum_with_cache(array_with_cache, op[1], op[2])
        else:
            update_with_cache(array_with_cache, op[1], op[2])
    end_time = time.time()
    cache_time = round(end_time - start_time, 2)

    # Виведення результатів
    print(f"Час виконання без кешування: {no_cache_time} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time} секунд")


if __name__ == "__main__":
    main()
