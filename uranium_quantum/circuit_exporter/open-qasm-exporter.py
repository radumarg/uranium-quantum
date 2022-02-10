import importlib
import math

BaseExporter = importlib.import_module("uranium_quantum.circuit_exporter.base-exporter")


class Exporter(BaseExporter.BaseExporter):
    def start_code(self):
        return f'\
OPENQASM 2.0;\n\
include "qelib1.inc";\n\
qreg q0[{self._qubits}];\n\
creg c0[{self._bits}];\n\n\n'

    def end_code(self):
        return ""

    # @staticmethod
    # def _gate_u3(
    #     targets, controls, theta_radians, phi_radians, lambda_radians, add_comments=True
    # ):
    #     out = "# u3 gate\n" if add_comments else ""
    #     # out += f"u({theta_radians}, {phi_radians}, {lambda_radians}) q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_u2(targets, controls, phi_radians, lambda_radians, add_comments=True):
    #     out = "# u2 gate\n" if add_comments else ""
    #     # out += f"u({math.pi/2}, {phi_radians}, {lambda_radians}) q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_u1(targets, controls, lambda_radians, add_comments=True):
    #     out = "# u1 gate\n" if add_comments else ""
    #     # out += f"p({lambda_radians}) q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_identity(targets, controls, add_comments=True):
    #     out = "# identity gate\n" if add_comments else ""
    #     # out += f"id q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_hadamard(targets, controls, add_comments=True):
    #     out = "# hadamard gate\n" if add_comments else ""
    #     #out += f"h q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_hadamard_xy(targets, controls, add_comments=True):
    #     out = "# hadamard-xy gate\n" if add_comments else ""
    #     #out += f"h q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_hadamard_yz(targets, controls, add_comments=True):
    #     out = "# hadamard-yz gate\n" if add_comments else ""
    #     #out += f"h q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_hadamard_zx(targets, controls, add_comments=True):
    #     out = "# hadamard-zx gate\n" if add_comments else ""
    #     #out += f"h q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_pauli_x(targets, controls, add_comments=True):
    #     out = "# pauli-x gate\n" if add_comments else ""
    #     # out += f"x q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_pauli_y(targets, controls, add_comments=True):
    #     out = "# pauli-y gate\n" if add_comments else ""
    #     #out += f"y q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_pauli_z(targets, controls, add_comments=True):
    #     out = "# pauli-z gate\n" if add_comments else ""
    #     # out += f"z q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_pauli_x_root(targets, controls, root, add_comments=True):
    #     out = "# pauli-x-root gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_y_root(targets, controls, root, add_comments=True):
    #     out = "# pauli-y-root gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_z_root(targets, controls, root, add_comments=True):
    #     out = "# pauli-z-root gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_x_root_dagger(targets, controls, root, add_comments=True):
    #     out = "# pauli-x-root-dagger gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_y_root_dagger(targets, controls, root, add_comments=True):
    #     out = "# pauli-y-root-dagger gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_pauli_z_root_dagger(targets, controls, root, add_comments=True):
    #     out = "# pauli-z-root-dagger gate\n" if add_comments else ""
    #     root = f"(2**{root[4:]})" if '^' in root else root[2:]
    #     return out

    # @staticmethod
    # def _gate_t(targets, controls, add_comments=True):
    #     out = "# t gate\n" if add_comments else ""
    #     # out += f"t q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_t_dagger(targets, controls, add_comments=True):
    #     out = "# t-dagger gate\n" if add_comments else ""
    #     #out += f"tdg q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_rx_theta(targets, controls, theta, add_comments=True):
    #     out = "# rx-theta gate\n" if add_comments else ""
    #     # out += f"rx({theta}) q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_ry_theta(targets, controls, theta, add_comments=True):
    #     out = "# ry-theta gate\n" if add_comments else ""
    #     # out += f"ry({theta}) q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_rz_theta(targets, controls, theta, add_comments=True):
    #     out = "# rz-theta gate\n" if add_comments else ""
    #     #out += f"rz({theta}) q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_s(targets, controls, add_comments=True):
    #     out = "# s gate\n" if add_comments else ""
    #     # out += f"s q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_s_dagger(targets, controls, add_comments=True):
    #     out = "# s-dagger gate\n" if add_comments else ""
    #     # out += f"sdg q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_swap(targets, controls, add_comments=True):
    #     out = "# swap gate\n" if add_comments else ""
    #     # out += f"swap q0[{target}], q0[{target2}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_swap_root(targets, controls, add_comments=True):
    #     out = "# swap gate\n" if add_comments else ""
    #     # out += f"swap q0[{target}], q0[{target2}];\n\n"
    #     return out
      # @staticmethod
    # def _gate_swap_root_dagger(targets, controls, add_comments=True):
    #     out = "# swap gate\n" if add_comments else ""
    #     # out += f"swap q0[{target}], q0[{target2}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_iswap(targets, controls, add_comments=True):
    #     out = "# iswap gate\n" if add_comments else ""
    #     # out += f"iswap q0[{target}], q0[{target2}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_fswap(targets, controls, add_comments=True):
    #     out = "# fswap gate\n" if add_comments else ""
    #     # out += f"fswap q0[{target}], q0[{target2}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_swap_theta(targets, controls, phi, add_comments=True):
    #     out = "# swap phi gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_sqrt_swap(targets, controls, add_comments=True):
    #     out = "# sqrt-swap gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_xx(targets, controls, theta, add_comments=True):
    #     out = "# xx gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_yy(targets, controls, theta, add_comments=True):
    #     out = "# yy gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_zz(targets, controls, theta, add_comments=True):
    #     out = "# zz gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_xy(targets, controls, theta, add_comments=True):
    #     out = "# xy gate\n" if add_comments else ""
    #     return out

    # @staticmethod
    # def _gate_qft(targets, controls, add_comments=True):
    #     out = "# qft gate\n" if add_comments else ""
    #     # out += f"t q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_qft_dagger(targets, controls, add_comments=True):
    #     out = "# qft-dagger gate\n" if add_comments else ""
    #     #out += f"tdg q0[{target}];\n\n"
    #     return out

    # @staticmethod
    # def _gate_aggregate(targets, controls, add_comments=True):
    #     out = "# aggregate gate\n" if add_comments else ""
    #     # out += f"t q0[{target}];\n\n"
    #     return out

    @staticmethod
    def _gate_measure_x(targets, controls, classic_bit, add_comments=True):
        raise BaseExporter.ExportException("The measure-x gate is not implemented.")

    @staticmethod
    def _gate_measure_y(targets, controls, classic_bit, add_comments=True):
        raise BaseExporter.ExportException("The measure-y gate is not implemented.")

    @staticmethod
    def _gate_measure_z(targets, controls, classic_bit, add_comments=True):
        out = "# measure-z gate\n" if add_comments else ""
        out += f"measure q0[{targets[0]}] -> c0[{classic_bit}];\n\n"
        return out
