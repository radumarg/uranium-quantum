import importlib
import math

BaseExporter = importlib.import_module("base-exporter")


class Exporter(BaseExporter.BaseExporter):
    def start_code(self):
        return f"\
from qiskit import QuantumRegister\n\
from qiskit.circuit import ClassicalRegister\n\
from qiskit import QuantumCircuit, execute, Aer\n\
from qiskit.circuit.library.standard_gates import iswap\n\
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate\n\
cr = ClassicalRegister({self._bits})\n\
qr = QuantumRegister({self._qubits})\n\
qc = QuantumCircuit(qr, cr)\n\n\n"

    def end_code(self):
        return f"\
simulator = Aer.get_backend('qasm_simulator')\n\
job = execute(qc, backend=simulator, shots=10)\n\
job_result = job.result()\n\
print(job_result.status)\n"

    @staticmethod
    def _gate_u3(
        target, theta_radians, phi_radians, lambda_radians, add_comments=False
    ):
        out = "# u3 gate\n" if add_comments else ""
        out += f"qc.u({theta_radians}, {phi_radians}, {lambda_radians}, qr[{target}])\n"
        return out

    @staticmethod
    def _gate_u2(target, phi_radians, lambda_radians, add_comments=False):
        out = "# u2 gate\n" if add_comments else ""
        out += f"qc.u({math.pi/2}, {phi_radians}, {lambda_radians}, qr[{target}])\n"
        return out

    @staticmethod
    def _gate_u1(target, lambda_radians, add_comments=False):
        out = "# u1 gate\n" if add_comments else ""
        out += f"qc.p({lambda_radians}, qr[{target}])\n"
        return out

    @staticmethod
    def _gate_identity(target, add_comments=False):
        out = "# identity gate\n" if add_comments else ""
        out += f"qc.id(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_hadamard(target, add_comments=False):
        out = "# hadamard gate\n" if add_comments else ""
        out += f"qc.h(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_pauli_x(target, add_comments=False):
        out = "# pauli-x gate\n" if add_comments else ""
        out += f"qc.x(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_pauli_y(target, add_comments=False):
        out = "# pauli-y gate\n" if add_comments else ""
        out += f"qc.y(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_pauli_z(target, add_comments=False):
        out = "# pauli-z gate\n" if add_comments else ""
        out += f"qc.z(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_pauli_x_root(target, root, add_comments=False):
        # TODO
        out = "# pauli-x-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_y_root(target, root, add_comments=False):
        # TODO
        out = "# pauli-y-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_z_root(target, root, add_comments=False):
        # TODO
        out = "# pauli-z-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_x_root_dagger(target, root, add_comments=False):
        # TODO
        out = "# pauli-x-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_y_root_dagger(target, root, add_comments=False):
        # TODO
        out = "# pauli-y-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_pauli_z_root_dagger(target, root, add_comments=False):
        # TODO
        out = "# pauli-z-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_sqrt_not(target, add_comments=False):
        out = "# sqrt-not gate\n" if add_comments else ""
        out += f"qc.sx(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_t(target, add_comments=False):
        out = "# t gate\n" if add_comments else ""
        out += f"qc.t(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_t_dagger(target, add_comments=False):
        out = "# t-dagger gate\n" if add_comments else ""
        out += f"qc.tdg(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_rx_theta(target, theta, add_comments=False):
        out = "# rx-theta gate\n" if add_comments else ""
        out += f"qc.rx({theta}, qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ry_theta(target, theta, add_comments=False):
        out = "# ry-theta gate\n" if add_comments else ""
        out += f"qc.ry({theta}, qr[{target}])\n"
        return out

    @staticmethod
    def _gate_rz_theta(target, theta, add_comments=False):
        out = "# rz-theta gate\n" if add_comments else ""
        out += f"qc.rz({theta}, qr[{target}])\n"
        return out

    @staticmethod
    def _gate_s(target, add_comments=False):
        out = "# s gate\n" if add_comments else ""
        out += f"qc.s(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_s_dagger(target, add_comments=False):
        out = "# s-dagger gate\n" if add_comments else ""
        out += f"qc.sdg(qr[{target}])\n"
        return out

    @staticmethod
    def _gate_swap(target, target2, add_comments=False):
        out = "# swap gate\n" if add_comments else ""
        out += f"qc.swap(qr[{target}], qr[{target2}])\n"
        return out

    @staticmethod
    def _gate_iswap(target, target2, add_comments=False):
        out = "# iswap gate\n" if add_comments else ""
        out += f"qc.iswap(qr[{target}], qr[{target2}])\n"
        return out

    @staticmethod
    def _gate_swap_phi(target, target2, phi, add_comments=False):
        raise BaseExporter.ExportException("The swap-phi gate is not implemented.")

    @staticmethod
    def _gate_sqrt_swap(target, target2, add_comments=False):
        out = "# sqrt-swap gate\n" if add_comments else ""
        out += f"qc.u({math.pi/2}, {math.pi/2}, {-math.pi}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, {-math.pi/2}, {math.pi}, qr[{target2}])\n"
        out += f"qc.cx(qr[{target}], qr[{target2}])\n"
        out += f"qc.u({math.pi/4}, {-math.pi/2}, {-math.pi/2}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, 0, {1.75 * math.pi}, qr[{target2}])\n"
        out += f"qc.cx(qr[{target}], qr[{target2}])\n"
        out += f"qc.u({math.pi/4}, {-math.pi}, {-math.pi/2}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, {math.pi}, {math.pi/2}, qr[{target2}])\n"
        out += f"qc.cx(qr[{target}], qr[{target2}])\n"
        out += f"qc.u({math.pi/2}, 0, {-1.5 * math.pi}, qr[{target}])\n"
        out += f"qc.u({math.pi/2}, {math.pi/2}, 0, qr[{target2}])\n"
        return out

    @staticmethod
    def _gate_xx(target, target2, theta, add_comments=False):
        out = "# xx gate\n" if add_comments else ""
        out += f"qc.append(RXXGate({theta}), [{target}, {target2}])\n"
        return out

    @staticmethod
    def _gate_yy(target, target2, theta, add_comments=False):
        out = "# yy gate\n" if add_comments else ""
        out += f"qc.append(RYYGate({theta}), [{target}, {target2}])\n"
        return out

    @staticmethod
    def _gate_zz(target, target2, theta, add_comments=False):
        out = "# zz gate\n" if add_comments else ""
        out += f"qc.append(RXXGate({theta}), [{target}, {target2}])\n"
        return out

    @staticmethod
    def _gate_ctrl_hadamard(control, target, controlstate, add_comments=False):
        out = "# ctrl-hadamard gate\n" if add_comments else ""
        out += f"qc.ch(qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_u3(
        control,
        target,
        controlstate,
        theta_radians,
        phi_radians,
        lambda_radians,
        add_comments=False,
    ):
        out = "# ctrl-u3 gate\n" if add_comments else ""
        out += f"qc.cu({theta_radians}, {phi_radians}, {lambda_radians}, {math.pi/2}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_u2(
        control, target, controlstate, phi_radians, lambda_radians, add_comments=False
    ):
        out = "# ctrl-u2 gate\n" if add_comments else ""
        out += f"qc.cu({math.pi/2}, {phi_radians}, {lambda_radians}, {math.pi/2}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_u1(
        control, target, controlstate, lambda_radians, add_comments=False
    ):
        out = "# ctrl-u1 gate\n" if add_comments else ""
        out += f"qc.cp({lambda_radians}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_t(control, target, controlstate, add_comments=False):
        out = "# ctrl-t gate\n" if add_comments else ""
        out += f"qc.cp({math.pi/4}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_t_dagger(control, target, controlstate, add_comments=False):
        out = "# ctrl-t-dagger gate\n" if add_comments else ""
        out += f"qc.cp({-math.pi/4}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x(control, target, controlstate, add_comments=False):
        out = "# ctrl-pauli-x gate\n" if add_comments else ""
        out += f"qc.cx(qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_y(control, target, controlstate, add_comments=False):
        out = "# ctrl-pauli-y gate\n" if add_comments else ""
        out += f"qc.cy(qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_z(control, target, controlstate, add_comments=False):
        out = "# ctrl-pauli-z gate\n" if add_comments else ""
        out += f"qc.cz(qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x_root(
        control, target, controlstate, root, add_comments=False
    ):
        # TODO
        out = "# ctrl-pauli-x-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_y_root(
        control, target, controlstate, root, add_comments=False
    ):
        # TODO
        out = "# ctrl-pauli-y-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_z_root(
        control, target, controlstate, root, add_comments=False
    ):
        # TODO
        out = "# ctrl-pauli-z-root gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_x_root_dagger(
        control, target, controlstate, root, add_comments=False
    ):
        # TODO
        out = "# ctrl-pauli-x-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_y_root_dagger(
        control, target, controlstate, root, add_comments=False
    ):
        # TODO
        out = "# ctrl-pauli-y-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_pauli_z_root_dagger(
        control, target, controlstate, root, add_comments=False
    ):
        # TODO
        out = "# ctrl-pauli-z-root-dagger gate\n" if add_comments else ""
        return out

    @staticmethod
    def _gate_ctrl_sqrt_not(control, target, controlstate, add_comments=False):
        out = "# ctrl-sqrt-not gate\n" if add_comments else ""
        out += f"qc.csx(qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_rx_theta(
        control, target, controlstate, theta_radians, add_comments=False
    ):
        out = "# ctrl-rx-theta gate\n" if add_comments else ""
        out += f"qc.crx({theta_radians}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_ry_theta(
        control, target, controlstate, theta_radians, add_comments=False
    ):
        out = "# ctrl-ry-theta gate\n" if add_comments else ""
        out += f"qc.cry({theta_radians}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_rz_theta(
        control, target, controlstate, theta_radians, add_comments=False
    ):
        out = "# ctrl-rz-theta gate\n" if add_comments else ""
        out += f"qc.crz({theta_radians}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_s(control, target, controlstate, add_comments=False):
        out = "# ctrl-s gate\n" if add_comments else ""
        out += f"qc.cp({math.pi/2}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_ctrl_s_dagger(control, target, controlstate, add_comments=False):
        out = "# ctrl-s-dagger gate\n" if add_comments else ""
        out += f"qc.cp({-math.pi/2}, qr[{control}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_toffoli(
        control, control2, target, controlstate, controlstate2, add_comments=False
    ):
        out = "# toffoli gate\n" if add_comments else ""
        out += f"qc.ccx(qr[{control}], qr[{control2}], qr[{target}])\n"
        return out

    @staticmethod
    def _gate_fredkin(control, target, target2, controlstate, add_comments=False):
        out = "# fredkin gate\n" if add_comments else ""
        out += f"qc.cswap(qr[{control}], qr[{target}], qr[{target2}])\n"
        return out

    @staticmethod
    def _gate_measure_x(target, classic_bit, add_comments=False):
        raise BaseExporter.ExportException("The measure-x gate is not implemented.")

    @staticmethod
    def _gate_measure_y(target, classic_bit, add_comments=False):
        raise BaseExporter.ExportException("The measure-y gate is not implemented.")

    @staticmethod
    def _gate_measure_z(target, classic_bit, add_comments=False):
        out = "# measure-z gate\n" if add_comments else ""
        out += f"qc.measure(qr[{target}], cr[{classic_bit}])\n"
        return out
