from src.tdas.linked_list import LinkedList


class Machine:
    def __init__(self, name, production_lines, components, assembly_time):
        self.name = name
        self.production_lines = production_lines  # Number of production lines (n)
        self.components = components  # Number of components per line (m)
        self.assembly_time = assembly_time  # Time taken to assemble components
        self.products = LinkedList()  # Use a linked list to store products

    def add_product(self, product):
        self.products.append(product)

    def __repr__(self):
        return f"<Machine {self.name}: {self.production_lines} lines, {self.components} components>"
