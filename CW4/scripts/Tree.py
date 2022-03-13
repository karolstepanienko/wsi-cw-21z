# Autor: Karol Stepanienko


# Leaves - int that identifies the class
# Node - int that identifies the attribute (attribute index)
# d_j_list - values that attribute d can take
class Tree:
    def __init__(self, d, d_j_list, ID3_results):
        self.node = d
        self.branches = d_j_list
        self.values = ID3_results
        # Dictionary that holds:
        # keys - parameter values
        # values - classes or other trees
        self.children = self.get_children(d_j_list, ID3_results)

    def get_children(self, d_j_list, ID3_results) -> dict:
        children = {}
        for d_j, c in zip(d_j_list, ID3_results):
            children[d_j] = c
        return children

    def print_tree(self, tabulators=0):
        space = "   "
        print(space * tabulators + "Node " + str(self.node) + " start")

        for d_j, child in self.children.items():
            if type(child) == Tree:
                print(space * tabulators + "{" + str(d_j) + ": ")
                tabulators += 1
                child.print_tree(tabulators)
                tabulators -= 1
                print(space * tabulators + "}")
            else:
                print(space * tabulators + "{" + str(d_j) + ": " + str(child) + "}")

        print(space * tabulators + "Node " + str(self.node) + " end")

    def __str__(self):
        return "Node: " + str(self.node) + ";\n" + "Children: " + str(self.children)