import sys
import numpy
import math

class HuffmanTree():
    
    def __init__(self, radix, root_node):
        """
            Initialize a tree
        """
        self.radix = radix
        self.root_node = root_node
        self.nodes = []

    def build_huffman_tree(self, huffman_nodes, level = 0):
        """
            Recursive Huffman function to build the entire Huffman tree based on a list of HuffmanNodes and their probabilities.
        """
        print("HuffmantTree.huffman_encode()")
        # sort the list of HuffmanNodes by their weights from least to greatest
        huffman_nodes = sorted(huffman_nodes, key = lambda node: node.weight)

        while len(huffman_nodes) > 1:
            print("len(huffman_nodes) = %d" %len(huffman_nodes))

            # pop the r-lowest weight nodes (symbols) from the list of nodes.
            children = []
            for n in range(0,self.radix):
                children.append(huffman_nodes.pop(0))
            
            # make an empty parent node
            parent_weight = sum(child.weight for child in children)
            parent_node = HuffmanNode(symbol = "%s_%1.2f" %(level, parent_weight), weight = parent_weight, parent = None, children = children, level = level)
            self.nodes.append(parent_node)
            print(parent_node.level)

            # Set the children node's pointers to point to their parent, and 
            self.add_children(parent_node, children)
            # the new root node is the parent node we have just made. All other nodes so far should fall
            # under this node. NOTE - This might not necessarily be true while constructing the tree, although it
            # should be true once the tree is complete, as all nodes should fall under a single root.
            self.root_node = parent_node

            # Put the parent node back into the huffman_nodes list and re-sort it by weight
            huffman_nodes.insert(0, parent_node)
            hufman_nodes = sorted(huffman_nodes, key = lambda node: node.weight)

            # call the next level of recursion
            level += 1
            self.build_huffman_tree(huffman_nodes, level = level)
        return


    def add_children(self, parent, children):
        """
            Add a children nodes to a parent node. Simply adjusts the pointers
            of the respective parent and child nodes.
        """
        print("Adding children")
        print children
        for child in children:
            child.parent = parent
            child.level = parent.level + 1
        return

    def traverse_and_callback(self, start_node, callback = None):
        """
            Starting from the given node, traverse the Huffman tree, and apply 
            the callback function to each node.
        """
        if len(start_node.children) > 0:
            for child in start_node.children:
                print("\t%s\t\t%1.2f\t\t%d\t\t%s" %(child.symbol, child.weight, child.level, child.parent.symbol))
                # Pass the child node to the callback function, if there is one
                if callback != None:
                    callback(child)
                self.traverse_and_callback(child, callback = callback)


        return

class HuffmanNode():

    def __init__(self, symbol, weight, parent = None, children = [], level = None, levelnode = None):
        self.symbol = symbol
        self.weight = weight
        self.code = None
        self.code_length = None

        # tree location info
        self.level = level
        self.levelnode = levelnode

        # node topological parameters
        self.parent = parent
        self.children = children

    def is_orphaned():
        if self.parent is None:
            return True
        else:
            return False

    def is_childless():
        if len(self.children) == 0:
            return True
        else:
            return False

class HuffmanEncoder():
    def __init__(self, input_file):
        # Read the problem definition into the dict symbols
        symbols = self._read_problem(input_file[0]) #TODO - replace passing in filename with file prompt
        if symbols == -1:
            print("Exiting Program")
            return
        else:
            print symbols

        # create a list of sorted nodes from the symbols and their weights
        self.huffman_nodes = self._create_nodes(symbols)
        return




    def _read_problem(self, infile, radix = 2):
        """
            Read in a Huffman encoding problem from a text file. Return a 
            dict keyed on the symbols with the symbol probabilities (weights)
            as the values.
        """
        symbols = {}
        self.radix = radix
        with open(infile, 'r') as f:
            for line in f:
                line = line.rstrip('\n').split(',')
                if len(line) > 2:
                    print("Error: Too many input fields in %s" %infile)
                    return -1
                symbol = line[0]
                weight = float(line[1])

                symbols[symbol] = weight

        return symbols

    def _create_nodes(self, symbols_dict):
        """
            Create a list of HuffmanNode objects from the symbols and weights in symbols_dict
            sorted from least to greatest symbol weight (probability),
        """
        # create individual nodes for each symbol
        huffman_nodes = []
        for symbol in symbols_dict:
            node = HuffmanNode(symbol = symbol, weight = symbols_dict[symbol])
            huffman_nodes.append(node)

        # sort the list of nodes by increasing probability (weight)
        huffman_nodes = sorted(huffman_nodes, key = lambda node: node.weight)
        return huffman_nodes
    def huffman_base2_callback(self, node):
        """
            Callback function for HuffmanTree.traverse_and_callback() which calculates the 
            code word for the given node in the tree traversal sequence.

            Accepts a HuffmanNode as an argument, and only alters that node.
        """

    def huffman_encode(self):
        """
            Perform the Huffman encoding algorithm using symbols read in as huffman_nodes.
        """
        print("Running Huffman encoding")
        # create a HuffmanTree object to store the tree relations of the HuffmanNodes
        huff_tree = HuffmanTree(radix = 2, root_node = None)

        # make the two lowest-probability symbols siblings

        huff_tree.build_huffman_tree(self.huffman_nodes)

        # traverse the tree we just created
        print(huff_tree.root_node)
        print("\tSymbol\t|\tWeight\t|\tLevel\t|\tParent\t|")
        huff_tree.traverse_and_callback(huff_tree.root_node)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must pass a filename containing smybols and their frequency.")
    else:
        encoder = HuffmanEncoder(sys.argv[1:])
        encoder.huffman_encode()




