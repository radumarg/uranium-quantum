import importlib
import math

BaseExporter = importlib.import_module("uranium_quantum.circuit_exporter.base-exporter")


class Exporter(BaseExporter.BaseExporter):
    def start_code(self):
        return f"\
import numpy as np\n\
from qiskit import QuantumRegister\n\
from qiskit.circuit import ClassicalRegister\n\
from qiskit import QuantumCircuit\n\
\n\
from qiskit.circuit.library.standard_gates import XGate, YGate, ZGate, HGate\n\
from qiskit.circuit.library import RXGate, RYGate, RZGate\n\
from qiskit.circuit.library import SGate, SdgGate, TGate, TdgGate\n\
from qiskit.circuit.library import U1Gate, U2Gate, U3Gate\n\
from qiskit.circuit.library.standard_gates import iswap\n\
\n\
cr = ClassicalRegister({self._bits})\n\
qr = QuantumRegister({self._qubits})\n\
qc = QuantumCircuit(qr, cr)\n\n"

    def end_code(self):
        return f""

    @staticmethod
    def get_controlled_gate(name, controls, label, theta_radians=None, phi_radians=None, lambda_radians=None):
        controlstates = ""
        for control in controls:
            if control['state'] in ["0", "+", "+i"]:
                controlstates += "0"
            else:
                controlstates += "1"
        radians = ""
        if theta_radians != None:
          radians += f"{theta_radians}"
        if phi_radians != None:
          if radians:
            radians += f", {phi_radians}"
          else:
            radians += f"{phi_radians}"
        if lambda_radians != None:
          if radians:
            radians += f", {lambda_radians}"
          else:
            radians += f"{lambda_radians}"
        return f"{name}({radians}).control(num_ctrl_qubits={len(controls)}, ctrl_state='{controlstates}', label='{label}')"

    
    @staticmethod
    def controlled_gate_code(name, controls, targets, label, theta_radians=None, phi_radians=None, lambda_radians=None):
        controlled_gate = Exporter.get_controlled_gate(name, controls, label, theta_radians, phi_radians, lambda_radians)
        qubits = ""
        for control in controls:
            if qubits:
                qubits += ", "
            qubits += f"qr[{control['target']}]"
        for target in targets:
            if qubits:
                qubits += ", "
            qubits += f"qr[{target}]"
        return f"qc.append({controlled_gate}, [{qubits}])"

    @staticmethod
    def _gate_u3(
        controls, targets, theta_radians, phi_radians, lambda_radians, add_comments=True
    ):
        out = "# u3 gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('U3Gate', controls, targets, label='U3', theta_radians=theta_radians, phi_radians=phi_radians, lambda_radians=lambda_radians)
            out += f"{code}\n"
        else:
            out += f"qc.u3({theta_radians}, {phi_radians}, {lambda_radians}, qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_u2(controls, targets, phi_radians, lambda_radians, add_comments=True):
        out = "# u2 gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('U2Gate', controls, targets, label='U2', phi_radians=phi_radians, lambda_radians=lambda_radians)
            out += f"{code}\n"
        else:
            out += f"qc.u2({phi_radians}, {lambda_radians}, qr[{targets[0]}])\n"
        return out


    @staticmethod
    def _gate_u1(controls, targets, lambda_radians, add_comments=True):
        out = "# u1 gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('U1Gate', controls, targets, label='U1', lambda_radians=lambda_radians)
            out += f"{code}\n"
        else:
            out += f"qc.p({lambda_radians}, qr[{targets[0]}])\n"
        return out


    @staticmethod
    def _gate_identity(targets, add_comments=True):
        out = "# identity gate\n" if add_comments else ""
        out += f"qc.id(qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_hadamard(controls, targets, add_comments=True):
        out = "# hadamard gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('HGate', controls, targets, label='H')
            out += f"{code}\n"
        else:
            out += f"qc.h(qr[{targets[0]}])\n"
        return out

    # @staticmethod
    # def _gate_hadamard_xy(controls, targets, add_comments=True):
    #     out = "# hadamard-xy gate\n" if add_comments else ""
    #     #out += f"h q0[{target}];\n"
    #     return out

    # @staticmethod
    # def _gate_hadamard_yz(controls, targets, add_comments=True):
    #     out = "# hadamard-yz gate\n" if add_comments else ""
    #     #out += f"h q0[{target}];\n"
    #     return out

    @staticmethod
    def _gate_hadamard_zx(controls, targets, add_comments=True):
        out = "# hadamard-zx gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('HGate', controls, targets, label='H')
            out += f"{code}\n"
        else:
            out += f"qc.h(qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_pauli_x(controls, targets, add_comments=True):
        out = "# pauli-x gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('XGate', controls, targets, label='X')
            out += f"{code}\n"
        else:
            out += f"qc.x(qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_pauli_y(controls, targets, add_comments=True):
        out = "# pauli-y gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('YGate', controls, targets, label='Y')
            out += f"{code}\n"
        else:
            out += f"qc.y(qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_pauli_z(controls, targets, add_comments=True):
        out = "# pauli-z gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('ZGate', controls, targets, label='Z')
            out += f"{code}\n"
        else:
            out += f"qc.z(qr[{targets[0]}])\n"
        return out

    # @staticmethod
    # def _gate_pauli_x_root(controls, targets, root, add_comments=True):
    #     out = "# pauli-x-root gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_y_root(controls, targets, root, add_comments=True):
    #     out = "# pauli-y-root gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_z_root(controls, targets, root, add_comments=True):
    #     out = "# pauli-z-root gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_x_root_dagger(controls, targets, root, add_comments=True):
    #     out = "# pauli-x-root-dagger gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_y_root_dagger(controls, targets, root, add_comments=True):
    #     out = "# pauli-y-root-dagger gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_z_root_dagger(controls, targets, root, add_comments=True):
    #     out = "# pauli-z-root-dagger gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    @staticmethod
    def _gate_t(controls, targets, add_comments=True):
        out = "# t gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('TGate', controls, targets, label='T')
            out += f"{code}\n"
        else:
            out += f"qc.t(qr[{targets[0]}])\n"
        return out


    @staticmethod
    def _gate_t_dagger(controls, targets, add_comments=True):
        out = "# t-dagger gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('TdgGate', controls, targets, label='Tdg')
            out += f"{code}\n"
        else:
            out += f"qc.tdg(qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_rx_theta(controls, targets, theta_radians, add_comments=True):
        out = "# rx-theta gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('RXGate', controls, targets, label='Rx', theta_radians=theta_radians)
            out += f"{code}\n"
        else:
            out += f"qc.rx({theta_radians}, qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_ry_theta(controls, targets, theta_radians, add_comments=True):
        out = "# ry-theta gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('RYGate', controls, targets, label='Ry', theta_radians=theta_radians)
            out += f"{code}\n"
        else:
            out += f"qc.ry({theta_radians}, qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_rz_theta(controls, targets, theta_radians, add_comments=True):
        out = "# rz-theta gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('RZGate', controls, targets, label='Rz', theta_radians=theta_radians)
            out += f"{code}\n"
        else:
            out += f"qc.rz({theta_radians}, qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_s(controls, targets, add_comments=True):
        out = "# s gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('SGate', controls, targets, label='S')
            out += f"{code}\n"
        else:
            out += f"qc.s(qr[{targets[0]}])\n"
        return out

    @staticmethod
    def _gate_s_dagger(controls, targets, add_comments=True):
        out = "# s-dagger gate\n" if add_comments else ""
        if controls:
            code = Exporter.controlled_gate_code('SdgGate', controls, targets, label='Sdg')
            out += f"{code}\n"
        else:
            out += f"qc.sdg(qr[{targets[0]}])\n"
        return out

    # @staticmethod
    # def _gate_swap(controls, targets, add_comments=True):
    #     out = "# swap gate\n" if add_comments else ""
    #     # out += f"swap q0[{target}], q0[{target2}];\n"
    #     return out

    # @staticmethod
    # def _gate_swap_root(controls, targets, add_comments=True):
    #     out = "# swap gate\n" if add_comments else ""
    #     # out += f"swap q0[{target}], q0[{target2}];\n"
    #     return out
      # @staticmethod
    # def _gate_swap_root_dagger(controls, targets, add_comments=True):
    #     out = "# swap gate\n" if add_comments else ""
    #     # out += f"swap q0[{target}], q0[{target2}];\n"
    #     return out
  
    # @staticmethod
    # def _gate_iswap(controls, targets, add_comments=True):
    #     out = "# iswap gate\n" if add_comments else ""
    #     # out += f"iswap q0[{target}], q0[{target2}];\n"
    #     return out

    # @staticmethod
    # def _gate_fswap(controls, targets, add_comments=True):
    #     out = "# fswap gate\n" if add_comments else ""
    #     # out += f"fswap q0[{target}], q0[{target2}];\n"
    #     return out

    # @staticmethod
    # def _gate_swap_theta(controls, targets, phi, add_comments=True):
    #     out = "# swap phi gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_sqrt_swap(controls, targets, add_comments=True):
    #     out = "# sqrt-swap gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_xx(controls, targets, theta, add_comments=True):
    #     out = "# xx gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_yy(controls, targets, theta, add_comments=True):
    #     out = "# yy gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_zz(controls, targets, theta, add_comments=True):
    #     out = "# zz gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_xy(controls, targets, theta, add_comments=True):
    #     out = "# xy gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_qft(controls, targets, add_comments=True):
    #     out = "# qft gate\n" if add_comments else ""
    #     # out += f"t q0[{target}];\n"
    #     return out

    # @staticmethod
    # def _gate_qft_dagger(controls, targets, add_comments=True):
    #     out = "# qft-dagger gate\n" if add_comments else ""
    #     #out += f"tdg q0[{target}];\n"
    #     return out

    # @staticmethod
    # def _gate_aggregate(controls, targets, add_comments=True):
    #     out = "# aggregate gate\n" if add_comments else ""
    #     # out += f"t q0[{target}];\n"
    #     return out

    @staticmethod
    def _gate_measure_x(targets, classic_bit, add_comments=True):
        raise BaseExporter.ExportException("The measure-x gate is not implemented.")

    @staticmethod
    def _gate_measure_y(targets, classic_bit, add_comments=True):
        raise BaseExporter.ExportException("The measure-y gate is not implemented.")

    @staticmethod
    def _gate_measure_z(targets, classic_bit, add_comments=True):
        out = "# measure-z gate\n" if add_comments else ""
        out += f"qc.measure({targets[0]}, {classic_bit})"
        return out
