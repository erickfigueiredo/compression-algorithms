from copy import deepcopy


class BinaryHeap:
    """
    A class to represent a binary heap.
    """

    def __init__(self, data: list[any] = [], criteria: callable = (lambda a, b: a < b)) -> None:
        """
        Constructor for the BinaryHeap class.
        :param data: Initial list of elements to build the heap.
        :param criteria: Comparison function to establish heap order.
        """
        self.__data = deepcopy(data)
        self.__criteria = criteria
        self.__bottom_up_heapify()

    def get_heap(self) -> list[any]:
        """
        Getter for the heap.
        :return: A deep copy of the heap data.
        """
        return deepcopy(self.__data)

    def push(self, value: any) -> None:
        """
        Method to insert a new value into the heap.
        :param value: The value to be added to the heap.
        """
        self.__data.append(value)
        index = len(self.__data) - 1
        parent_index = self.__get_parent_by_index(index)

        while index > 0 and self.__criteria(self.__data[index], self.__data[parent_index]):
            self.__data[index], self.__data[parent_index] = self.__data[parent_index], self.__data[index]
            index = parent_index
            parent_index = self.__get_parent_by_index(index)

    def pop(self) -> any:
        """
        Method to remove and return the root value of the heap.
        :return: The root value of the heap.
        """
        if not len(self.__data):
            return None

        value = self.__data[0]
        self.__data[0] = self.__data[-1]
        del self.__data[-1]
        self.heapify(0)
        return value

    def heapify(self, parent: int) -> None:
        """
        Method to maintain the heap property.
        :param parent: Index of the parent node.
        """
        top = parent

        l = 2 * parent + 1
        r = 2 * parent + 2

        if l < len(self.__data) and self.__criteria(self.__data[l], self.__data[top]):
            top = l

        if r < len(self.__data) and self.__criteria(self.__data[r], self.__data[top]):
            top = r

        if top != parent:
            self.__data[top], self.__data[parent] = self.__data[parent], self.__data[top]
            self.heapify(top)

    def __bottom_up_heapify(self) -> None:
        """
        Method to build the heap from an unordered list.
        """
        if len(self.__data) <= 1:
            return

        index = len(self.__data) - 1

        for i in range(index // 2, -1, -1):
            self.heapify(i)

    def __get_parent_by_index(self, index: int) -> int:
        """
        Method to get the parent index of a given node.
        :param index: Index of the child node.
        :return: Index of the parent node.
        """
        return (index - 1) // 2

    def __len__(self) -> int:
        """
        Method to get the number of elements in the heap.
        :return: Number of elements in the heap.
        """
        return len(self.__data)