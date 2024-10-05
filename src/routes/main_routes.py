from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.utils.graphviz_generator import generate_tda_graph
from src.utils.report_generator import generate_html_report
from src.utils.xml_handler import parse_xml
from src.models.assembly import Assembly
from src.tdas.linked_list import LinkedList  # Correct import for LinkedList
from config import Config
import os

# Create blueprint
main_bp = Blueprint('main', __name__)

# Use LinkedList for machines
machines = LinkedList()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@main_bp.route('/')
def index():
    return render_template('pages/home.html')


@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    file_name = None
    file_size = None

    if request.method == 'POST':
        print("POST request received")

        if 'xml_file' not in request.files:
            flash('No file part')
            print("No file part found in request")
            return render_template('pages/upload.html', file_name=file_name, file_size=file_size)

        file = request.files['xml_file']
        print(f"File received: {file.filename}")

        if file.filename == '':
            flash('No selected file')
            print("No file selected by the user")
            return render_template('pages/upload.html', file_name=file_name, file_size=file_size)

        if file and file.filename.endswith('.xml'):
            filepath = os.path.join(Config.DATA_INPUT_DIR, file.filename)

            try:
                file.save(filepath)
                print(f"File saved at {filepath}")
                file_size = os.path.getsize(filepath)
                file_name = file.filename
                print(f"File name: {file_name}, File size: {file_size} bytes")
            except Exception as e:
                print(f"Error saving file: {e}")
                flash("Error saving file")
                return render_template('pages/upload.html', file_name=file_name, file_size=file_size)

            try:
                global machines
                machines = parse_xml(filepath)
                print("XML parsed successfully")
            except Exception as e:
                print(f"Error parsing XML: {e}")
                flash("Error parsing XML")
                return render_template('pages/upload.html', file_name=file_name, file_size=file_size)

            if file and allowed_file(file.filename):
                flash('File processed successfully (but not saved)')
                return redirect(url_for('main.select_machine'))

            flash('File successfully uploaded and parsed')

    print(f"Rendering template with file_name: {file_name}, file_size: {file_size}")

    return render_template('pages/upload.html', file_name=file_name, file_size=file_size)


@main_bp.route('/select_machine', methods=['GET', 'POST'])
def select_machine():
    global machines
    if machines.length() == 0:
        flash('No machines loaded. Please upload an XML file.')
        return redirect(url_for('main.upload'))

    selected_machine = None
    selected_machine_index = None
    products = LinkedList()

    if request.method == 'POST':
        selected_machine_index = int(request.form['machine'])
        selected_machine = machines.get(selected_machine_index)

        if selected_machine:
            products = selected_machine.products

        if 'simulate' in request.form:
            selected_product_index = int(request.form['product'])
            selected_product = products.get(selected_product_index)

            if selected_product:
                assembly = Assembly(selected_machine)
                assembly.simulate_product_assembly(selected_product)

                return render_template(
                    'pages/result.html',
                    machine=selected_machine,
                    product=selected_product,
                    steps=assembly.steps,
                    total_time=assembly.time
                )
    else:
        selected_machine_index = 0
        selected_machine = machines.get(0)
        products = selected_machine.products

    return render_template('pages/machines.html', machines=machines, selected_machine=selected_machine, products=products, selected_machine_index=selected_machine_index)


@main_bp.route('/generate_report/<int:machine_id>/<int:product_id>', methods=['GET'])
def generate_report(machine_id, product_id):
    global machines
    selected_machine = machines.get(machine_id)
    selected_product = selected_machine.products.get(product_id)

    assembly = Assembly(selected_machine)
    assembly.simulate_product_assembly(selected_product)

    generate_html_report(selected_machine, selected_product, assembly.steps, assembly.time)

    generate_tda_graph(assembly.steps, title=f"Assembly Steps for {selected_product.name}", filename=f"assembly_steps_{selected_product.name}")

    flash('Report and graph successfully generated!')
    return redirect(url_for('main.index'))





