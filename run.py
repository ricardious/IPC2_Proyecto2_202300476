from src.models.assembly import Assembly
from src.utils.xml_handler import parse_xml

# Parse machines from XML
machines = parse_xml('data/input/input.xml')

if machines.length() == 0:
    print("No machines found in the XML file.")
else:
    # Get the first machine from the LinkedList
    machine = machines.get(0)  # Use LinkedList method `get` to access the first machine

    # Get the first product from the machine's products LinkedList
    product = machine.products.get(0)  # Use LinkedList method `get` to access the first product

    # Simulate the assembly process
    assembly = Assembly(machine)
    assembly.simulate_product_assembly(product)
