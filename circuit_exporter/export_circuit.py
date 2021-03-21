import click
import importlib
import yaml

QiskitExporter = importlib.import_module("qiskit-exporter")
OpenQASMExporter = importlib.import_module("open-qasm-exporter")
PyquilExporter = importlib.import_module("pyquil-exporter")
QuilExporter = importlib.import_module("quil-exporter")
CirqExporter = importlib.import_module("cirq-exporter")


def get_number_qubits(yaml):
    """Extract the numebr of qubits in yaml circuit."""
    qubits = 0
    if "steps" in yaml.keys():
        for step in yaml["steps"]:
            if "gates" in step:
                for gate in step["gates"]:
                    qubits = max(qubits, gate["target"] + 1)
                    if "target2" in gate:
                        qubits = max(qubits, gate["target2"] + 1)
                    if "control" in gate:
                        qubits = max(qubits, gate["control"] + 1)
                    if "control2" in gate:
                        qubits = max(qubits, gate["control2"] + 1)
    return qubits


def get_number_bits(yaml):
    """Extract the numebr of bits in yaml circuit."""
    bits = 0
    if "steps" in yaml.keys():
        for step in yaml["steps"]:
            if "gates" in step:
                for gate in step["gates"]:
                    if "bit" in gate:
                        bits = max(bits, gate["bit"] + 1)
    return bits


def export_yaml(yaml_data, exporter, add_comments):
    """Export quantium circuit from YAML format to target language."""
    code = exporter.start_code()
    if "steps" in yaml_data.keys():
        for step in yaml_data["steps"]:
            code += exporter.process_step(step, add_comments)
    code += exporter.end_code()
    return code


@click.command()
@click.option(
    "--file", "-f", required=True, help="A file with quantum circuit in yaml format."
)
@click.option(
    "--export_format",
    "-e",
    required=True,
    help="Specific format for exporting the circuit into: 'qiskit', 'openqasm', 'pyquil', 'quil' or 'cirq'.",
)
@click.option(
    "--comments", "-c", required=False, help="Comment code for each exported gate."
)
def main(file, export_format, comments):

    output_file = file.replace(".yaml", f"_{export_format}.py")

    if not file.endswith(".yaml"):
        print("A yaml file is required as input for this script.")
        return

    exporter = None
    if export_format.lower() == "qiskit":
        exporter = QiskitExporter.Exporter()
    elif export_format.lower() == "openqasm":
        exporter = OpenQASMExporter.Exporter()
        output_file = file.replace(".yaml", "_OpenQASM.qasm")
    elif export_format.lower() == "pyquil":
        exporter = PyquilExporter.Exporter()
    elif export_format.lower() == "quil":
        exporter = QuilExporter.Exporter()
        output_file = file.replace(".yaml", "_Quil.quil")
    elif export_format.lower() == "cirq":
        exporter = CirqExporter.Exporter()

    quantum_code = ""
    with open(file, "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            no_qubits = get_number_qubits(yaml_data)
            exporter.set_number_qubits(no_qubits)
            no_bits = get_number_bits(yaml_data)
            exporter.set_number_bits(no_bits)
            if comments:
                quantum_code = export_yaml(yaml_data, exporter, add_comments=True)
            else:
                quantum_code = export_yaml(yaml_data, exporter, add_comments=False)
        except yaml.YAMLError as ex:
            quantum_code = str(ex)

    with open(output_file, "w") as outfile:
        outfile.write(quantum_code)


if __name__ == "__main__":
    main()
