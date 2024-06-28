from .huffnode import HuffNode
from .binary_heap import BinaryHeap


class HuffmanEncoding:
    """
    A class to represent Huffman Encoding.
    """

    def __init__(self) -> None:
        """
        Constructor for the HuffmanEncoding class.
        """
        pass

    def get_char_frequency(self, content: str) -> dict:
        """
        Method to calculate the frequency of each character in the given content.
        :param content: The string content to analyze.
        :return: A dictionary with characters as keys and their frequencies as values.
        """
        char_frequency = {}

        for c in content:
            if c not in char_frequency:
                char_frequency[c] = 1
            else:
                char_frequency[c] += 1

        return char_frequency

    def build_tree(self, content: str) -> 'HuffNode':
        """
        Method to build the Huffman tree for the given content.
        :param content: The string content to build the tree for.
        :return: The root node of the Huffman tree.
        """
        freq_by_char = self.get_char_frequency(content=content)
        print('\t\tFrequence by char:', freq_by_char)

        nodes = [HuffNode(char=c, freq=f) for c, f in freq_by_char.items()]
        h = BinaryHeap(nodes, criteria=(lambda a, b: a < b))

        while len(h) > 1:
            node1 = h.pop()
            node2 = h.pop()

            merged = HuffNode(None, node1.freq +
                              node2.freq if node2 else node1.freq)
            merged.left = node1
            merged.right = node2
            h.push(merged)

        return h.pop()

    def build_codes(self, node: 'HuffNode', prefix: str = '', code: dict = None) -> dict:
        """
        Method to build the Huffman codes for characters.
        :param node: The current node in the Huffman tree.
        :param prefix: The current Huffman code prefix.
        :param code: The dictionary to store Huffman codes.
        :return: A dictionary with characters as keys and their Huffman codes as values.
        """
        if code is None:
            code = {}

        if node is not None:
            if node.char is not None:
                code[node.char] = prefix

            self.build_codes(node.left, prefix + '0', code)
            self.build_codes(node.right, prefix + '1', code)

        return code

    def __encode(self, text: str, code: dict) -> str:
        """
        Private method to encode the given text using the Huffman codes.
        :param text: The text to encode.
        :param code: The Huffman codes dictionary.
        :return: The encoded text as a string of bits.
        """
        return ''.join(code[char] for char in text)

    def __decode(self, encoded_text: str, root: 'HuffNode') -> str:
        """
        Private method to decode the given encoded text using the Huffman tree.
        :param encoded_text: The encoded text as a string of bits.
        :param root: The root of the Huffman tree.
        :return: The decoded text.
        """
        decoded_text = []
        node = root
        for bit in encoded_text:
            if bit == '0':
                node = node.left
            else:
                node = node.right

            if node.char is not None:
                decoded_text.append(node.char)
                node = root

        return ''.join(decoded_text)

    def encoding(self, text: str) -> tuple:
        """
        Method to encode the given text and return the encoded text and Huffman tree.
        :param text: The text to encode.
        :return: A tuple containing the encoded text and the root of the Huffman tree.
        """
        root = self.build_tree(text)
        code = self.build_codes(root)
        enc = self.__encode(text, code)
        return enc, root

    def decoding(self, encoded_text: str, root: 'HuffNode') -> str:
        """
        Method to decode the given encoded text using the Huffman tree.
        :param encoded_text: The encoded text as a string of bits.
        :param root: The root of the Huffman tree.
        :return: The decoded text.
        """
        return self.__decode(encoded_text, root)