from src.tdas.linked_list import LinkedList  # Correct import for LinkedList
from src.utils.report_generator import generate_html_report  # Correct import for report generation
from src.utils.graphviz_generator import generate_tda_graph  # Import the graph generator


class Assembly:
    def __init__(self, machine):
        self.machine = machine
        self.time = 0  # Track the total time for the assembly process
        self.current_positions = LinkedList()  # Correct use of LinkedList to store current positions
        self.steps = LinkedList()  # Correct use of LinkedList to store steps for report generation

        # Initialize the current position of each line to 0
        for _ in range(self.machine.production_lines):
            self.current_positions.append(0)

    def move_arm(self, line, target_component):
        # Get the current position from the linked list
        current_position = self.current_positions.get(line)
        movement_time = abs(target_component - current_position)
        self.time += movement_time

        # Log the movement step in the steps LinkedList
        self.steps.append(f"Move arm to component {target_component} on line {line + 1} (Took {movement_time} seconds)")

        # Update the position in the linked list
        self.current_positions.append(target_component)

        # Generate graph of the current positions after the move
        generate_tda_graph(self.current_positions, title=f"Arm Position at Time {self.time}", filename=f"arm_position_{self.time}")

    def assemble(self, line):
        # Add assembly time
        self.time += self.machine.assembly_time

        # Log the assembly step in the steps LinkedList
        self.steps.append(f"Assemble component on line {line + 1} (Took {self.machine.assembly_time} seconds)")

        # Generate graph of the assembly steps
        generate_tda_graph(self.steps, title=f"Assembly Steps at Time {self.time}", filename=f"assembly_steps_{self.time}")

    def simulate_product_assembly(self, product):
        print(f"Simulating assembly for {product.name}")

        current_step = product.assembly_sequence.head
        while current_step:
            step = current_step.data
            line = int(step[1]) - 1  # Extract the line number (L1 -> line 0)
            component = int(step[3])  # Extract the component number (C2 -> component 2)

            # Move the arm and assemble the component
            self.move_arm(line, component)
            self.assemble(line)

            current_step = current_step.next

        print(f"Total time for {product.name} assembly: {self.time} seconds")

        # Generate HTML report
        generate_html_report(self.machine, product, self.steps, self.time)  # Use LinkedList directly for steps
