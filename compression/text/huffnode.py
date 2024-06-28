class HuffNode:
    """
    A class to represent a node in the Huffman tree.
    """

    def __init__(self, char: str, freq: int) -> None:
        """
        Constructor for the HuffNode class.
        :param char: Character represented by the node.
        :param freq: Frequency of the character.
        """
        self.char = char
        self.freq = freq

        self.left = None
        self.right = None

    def __lt__(self, other: 'HuffNode') -> bool:
        """
        Less-than comparison operator for HuffNode.
        :param other: Another HuffNode to compare with.
        :return: True if the frequency of this node is less than the other node, False otherwise.
        """
        return self.freq < other.freq

    def __str__(self) -> str:
        """
        String representation of the HuffNode class.
        :return: String representation of the HuffNode class.
        """
        return f'[char: {self.char}, freq: {self.freq}]'
