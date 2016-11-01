#!/usr/bin/python3
import sys
import math
import collections

class HuffmanTree():
    
    def __init__(self, radix, root_node, verbose = False):
        """
            Initialize a tree
        """
        self.radix = radix
        self.root_node = root_node
        self.nodes = []
        self.encoding = {}
        self.verbose = verbose

    def build_huffman_tree(self, huffman_nodes, level = 0):
        """
            Recursive Huffman function to build the entire Huffman tree based on a list of HuffmanNodes and their probabilities.
        """
        if self.verbose:
            print("\nHuffmanTree.huffman_encode()")
        # sort the list of HuffmanNodes by their weights from least to greatest
        huffman_nodes = sorted(huffman_nodes, key = lambda node: node.weight)

        if len(huffman_nodes) > 1:
            if self.verbose:
                print("huffman_nodes: ", [node.weight for node in huffman_nodes])
                print("len(huffman_nodes) = %d" %len(huffman_nodes))
                if len(huffman_nodes) == 2:
                    print("We should stop after this iteration")

            # pop the lowest weight nodes (symbols) from the list of nodes.
            children = []
            # if this is the first grouping of nodes and the radix is greater than 2, we must
            # pick a first cluster size s such that (N - s)/(r - 1) is an integer, where N is
            # the number of symbols in the symbol set, and r is the radix. See the paper by 
            # Huffman (1952).
            if (level == 0) and (self.radix > 2):
                for s in range(self.radix, 1, -1):
                    if (len(huffman_nodes) - s)%(self.radix-1) == 0:
                        if self.verbose:
                            print("Popping %d children" %s)

                        for n in range(0,s):
                            children.append(huffman_nodes.pop(0))
                        break

            else:
                if self.verbose:
                    print("Popping 2 children")
                for n in range(0,self.radix):
                    children.append(huffman_nodes.pop(0))

            if self.verbose:
                print("huffman_nodes after popping children: ", [node.weight for node in huffman_nodes])
                print("nodes in children list: ", [node.weight for node in children])
            
                
            
            # make an empty parent node
            parent_weight = sum(child.weight for child in children)
            parent_node = HuffmanNode(symbol = "%s_%1.2f" %(level, parent_weight), weight = parent_weight, parent = None, children = children, level = level + 1)
            self.nodes.append(parent_node)
            if self.verbose:
                print("Parent node level: ", parent_node.level)

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
            Add children nodes to a parent node. Simply adjusts the parent pointers
            of the child nodes to point to the parent.

            parent - A single HuffmanNode object.
            children - An iterable of HuffmanNode objects.
        """
        if self.verbose:
            print("Adding children")
        for child in children:
            child.parent = parent
            child.level = parent.level - 1  # 0 is the bottom of the tree
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

    def traverse_and_encode(self, node):
        """
            Traverse the Huffman tree from the given node and assign code words for each symbol.
        """
        #print("In " + node.symbol)
        if len(node.children) > 0:

            # This is NOT a leaf node.
            for i, child in enumerate(node.children):

                # Convert to alpha symbols if i exceeds 9
                if i > 9:
                    i = self._large_base_convert(i)

                # consider the case where node is the root node. Assign initial codewords to each child.
                if node.parent is None:
                    child.code.append(i)

                # All other nodes besides the root fall under this. They all have parents. Good for them.
                else:
                    # The child inherits the parent's code
                    for e in node.code:
                        child.code.append(e)

                    # The child also gets a new code symbol appended to the end.
                    child.code.append(i)
                self.traverse_and_encode(child)
        else:

            # This IS a leaf node. In other words, this is the code of a distinct symbol. Yay!
            if node.parent is not None:
                node.code = ''.join(str(e) for e in node.code)
                self.encoding[node.symbol] = node.code
                if self.verbose:
                    print("%s: %s" %(node.symbol, node.code))

        #print("Out " + node.symbol)
        return

    def _large_base_convert(self, number):
        """
            Utility function to map numbers greater than 9 to ascii characters starting with 10 -> 'a'
        """
        return chr((number-9) + (ord('a') - 1))


class HuffmanNode():

    def __init__(self, symbol, weight, parent = None, children = [], level = None, levelnode = None):
        self.symbol = symbol
        self.weight = weight
        self.code = []
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
    def __init__(self, argv):

        self.input_file = argv[0]
        self.verbose = False
        self.output_file = None
        self.radix = 2

        if '-v' in argv:
            self.verbose = True

        if '-o' in argv:
            self.output_file = argv[argv.index('-o') + 1]

        if '-r' in argv:
            self.radix = int(argv[argv.index('-r') + 1])

        # Read the problem definition into the dict symbols
        symbols = self._read_problem(self.input_file) #TODO - replace passing in filename with file prompt
        if symbols == -1:
            print("Exiting Program")
            return
        else:
            if self.verbose:
                print("Symbols and weights:")
                for symbol in symbols:
                    print("%s: %f" %(symbol, symbols[symbol]))

        # create a list of sorted nodes from the symbols and their weights
        self.huffman_nodes = self._create_nodes(symbols)
        return




    def _read_problem(self, infile):
        """
            Read in a Huffman encoding problem from a text file. Return a 
            dict keyed on the symbols with the symbol probabilities (weights)
            as the values.
        """
        symbols = {}
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
        print("\nRunning Huffman encoding")
        print("Infile: %s\nRadix: %d" %(self.input_file, self.radix))
        if self.output_file:
            print("Output: %s" %self.output_file)

        # create a HuffmanTree object to store the tree relations of the HuffmanNodes
        huff_tree = HuffmanTree(radix = self.radix, root_node = None, verbose = self.verbose)

        # build the huffman tree
        huff_tree.build_huffman_tree(self.huffman_nodes)

        # assign codewords to the nodes in the huffman tree
        huff_tree.traverse_and_encode(huff_tree.root_node)

        # sort the encoding alphabetically by symbol
        huff_tree.encoding = collections.OrderedDict(sorted(huff_tree.encoding.items()))
        
        if self.output_file is None or self.verbose is True:
            print("\nCode:")
            for symbol in huff_tree.encoding:
                print("%s: %s" %(symbol, huff_tree.encoding[symbol]))
        if self.output_file is not None:
            # save the encoding to the given file

            with open(self.output_file, 'w') as of:
                for symbol in huff_tree.encoding:
                    of.write("%s, %s\n" %(symbol, huff_tree.encoding[symbol]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
            Usage: huffman.py symbol_file [-o output_file] [-r radix] [-v]\n
                symbol_file: File containing the symbols and associated weights (probabilities) in csv.
                -o output_file: Put the encoding output into output_file in csv.
                -r radix: Encode using the given radix. Defaults to radix = 2 (binary).
                -v: Verbose mode. Prints out a lot of stuff.
            """)
    else:
        encoder = HuffmanEncoder(sys.argv[1:])
        encoder.huffman_encode()




