from src.tdas.linked_list import LinkedList


class Product:
    def __init__(self, name, assembly_sequence):
        self.name = name
        self.assembly_sequence = LinkedList()  # Linked list to store assembly steps
        for step in assembly_sequence.split():
            self.assembly_sequence.append(step)

    def __repr__(self):
        return f"<Product {self.name}>"
