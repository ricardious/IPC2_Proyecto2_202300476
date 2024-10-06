from src.tdas.linked_list import LinkedList
from src.models.machine import Machine
from src.models.product import Product
import xml.etree.ElementTree as ET


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    machines = LinkedList()

    for machine_node in root.findall('Maquina'):
        name = machine_node.find('NombreMaquina').text
        production_lines = int(machine_node.find('CantidadLineasProduccion').text)
        components = int(machine_node.find('CantidadComponentes').text)
        assembly_time = int(machine_node.find('TiempoEnsamblaje').text)

        # Create machine object
        machine = Machine(name, production_lines, components, assembly_time)

        # Create linked list for products
        machine.products = LinkedList()

        # Parse the products
        for product_node in machine_node.find('ListadoProductos').findall('Producto'):
            product_name = product_node.find('nombre').text
            assembly_sequence = product_node.find('elaboracion').text.strip()

            # Create product object and add it to the machine's products linked list
            product = Product(product_name, assembly_sequence)
            machine.products.append(product)

        machines.append(machine)

    return machines

