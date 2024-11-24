class CustomStack:
    def __init__(self, name=None):
        self._elements = []
        self._count = 0
        self.name = name

    def push(self, value):
        """Функція додає елемент у стек"""
        self._elements.append(value)
        self._count += 1

    def pop(self):
        """Видаляє верхній елемент зі стека"""
        if self._count > 0:
            top_element = self._elements.pop()
            self._count -= 1
            return top_element
        return None

    def peek(self):
        """Повертає верхній елемент без його видалення"""
        return self._elements[-1] if self._count > 0 else None

    def clear(self):
        """Очищує стек"""
        self._elements = []
        self._count = 0

    def get_size(self):
        """Повертає кількість елементів у стеку"""
        return self._count
