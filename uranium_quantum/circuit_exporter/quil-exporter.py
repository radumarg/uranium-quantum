import importlib

BaseExporter = importlib.import_module("base-exporter")


class Exporter(BaseExporter.BaseExporter):
    def _define_initial_code_section(self):
        return f"DECLARE ro BIT[{self._bits}]\n"

    def _define_sqrt_not_gate_code_section(self):
        return "\
# define sqrt-not gate\n\
DEFGATE srn:\n\
    0.5 + 0.5i, 0.5 - 0.5i\n\
    0.5 - 0.5i, 0.5 + 0.5i\n"

    def _define_u3_gates_code_section(self):
        return "\
# define u3 gate\n\
DEFGATE u3(%theta, %phi, %lambda):\n\
    COS(%theta/2), -1*EXP(i*%lambda)*SIN(%theta/2)\n\
    EXP(i*%phi)*SIN(%theta/2), EXP(i*%lambda + i*%phi)*COS(%theta/2)\n"

    def _define_u2_gates_code_section(self):
        return "\
# define u2 gate\n\
DEFGATE u2(%phi, %lambda):\n\
    1/SQRT(2), -1*EXP(i*%lambda)*1/SQRT(2)\n\
    EXP(i*%phi)*1/SQRT(2), EXP(i*%lambda + i*%phi)*1/SQRT(2)\n"

    def _define_sqrt_swap_code_section(self):
        return "\
# define sqrt-swap gate\n\
DEFGATE srswap:\n\
    1, 0, 0, 0\n\
    0, 0.5 + 0.5i, 0.5 - 0.5i, 0\n\
    0, 0.5 - 0.5i, 0.5 + 0.5i, 0\n\
    0, 0, 0, 1\n"

    def _define_crtl_hadamard(self):
        return "\
# define ctrl-hadamard gate\n\
DEFGATE ch:\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, 0.7071067811865475, 0.7071067811865475\n\
    0, 0, 0.7071067811865475, -0.7071067811865475\n"

    def _define_crtl_y(self):
        return "\
# define ctrl-pauli-y gate\n\
DEFGATE cy:\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, 0, -i\n\
    0, 0, i, 0\n"

    def _define_crtl_sqrt_not(self):
        return "\
# define ctrl-sqrt-not gate\n\
DEFGATE csrn:\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, 0.5+0.5i, 0.5-0.5i\n\
    0, 0, 0.5-0.5i, 0.5+0.5i\n"

    def _define_crtl_rx(self):
        return "\
# define ctrl-rx-theta gate\n\
DEFGATE crx(%theta):\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, COS(%theta/2), -i*SIN(%theta/2)\n\
    0, 0, -i*SIN(%theta/2), COS(%theta/2)\n\
"

    def _define_crtl_ry(self):
        return "\
# define ctrl-ry-theta gate\n\
DEFGATE cry(%theta):\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, COS(%theta/2), -1*SIN(%theta/2)\n\
    0, 0, SIN(%theta/2), COS(%theta/2)\n"

    def _define_crtl_rz(self):
        return "\
# define ctrl-rz-theta gate\n\
DEFGATE crz(%phi):\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, COS(%phi / 2) - i * SIN(%phi / 2), 0\n\
    0, 0, 0, COS(%phi / 2) + i * SIN(%phi / 2)\n"

    def _define_crtl_u2(self):
        return "\
# define u2 gate\n\
DEFGATE cu2(%phi, %lambda):\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, 1/SQRT(2), -1*EXP(i*%lambda)*1/SQRT(2)\n\
    0, 0, EXP(i*%phi)*1/SQRT(2), EXP(i*%lambda + i*%phi)*1/SQRT(2)\n"

    def _define_crtl_u3(self):
        return "\
DEFGATE cu3(%theta, %phi, %lambda):\n\
    1, 0, 0, 0\n\
    0, 1, 0, 0\n\
    0, 0, COS(%theta/2), -1*EXP(i*%lambda)*SIN(%theta/2)\n\
    0, 0, EXP(i*%phi)*SIN(%theta/2), EXP(i*%lambda + i*%phi)*COS(%theta/2)\n"

    def start_code(self):
        return (
            self._define_initial_code_section()
            + "\n"
            + self._define_sqrt_not_gate_code_section()
            + "\n"
            + self._define_u3_gates_code_section()
            + "\n"
            + self._define_u2_gates_code_section()
            + "\n"
            + self._define_sqrt_swap_code_section()
            + "\n"
            + self._define_crtl_hadamard()
            + "\n"
            + self._define_crtl_y()
            + "\n"
            + self._define_crtl_sqrt_not()
            + "\n"
            + self._define_crtl_rx()
            + "\n"
            + self._define_crtl_ry()
            + "\n"
            + self._define_crtl_rz()
            + "\n"
            + self._define_crtl_u2()
            + "\n"
            + self._define_crtl_u3()
            + "\n"
        )

    def end_code(self):
        return ""

    @staticmethod
    def _gate_u3(
        target, theta_radians, phi_radians, lambda_radians, add_comments=False
    ):
        out = "# u3 gate\n" if add_comments else ""
        out += f"u3 ({theta_radians}, {phi_radians}, {lambda_radians}) {target}\n"
        return out

    @staticmethod
    def _gate_u2(target, phi_radians, lambda_radians, add_comments=False):
        out = "# u2 gate\n" if add_comments else ""
        out += f"u2 ({phi_radians}, {lambda_radians}) {target}\n"
        return out

    @staticmethod
    def _gate_u1(target, lambda_radians, add_comments=False):
        out = "# u1 gate\n" if add_comments else ""
        out += f"PHASE ({lambda_radians}) {target}\n"
        return out

    @staticmethod
    def _gate_identity(target, add_comments=False):
        out = "# identity gate\n" if add_comments else ""
        out += f"I {target}\n"
        return out

    @staticmethod
    def _gate_hadamard(target, add_comments=False):
        out = "# hadamard gate\n" if add_comments else ""
        out += f"H {target}\n"
        return out

    @staticmethod
    def _gate_pauli_x(target, add_comments=False):
        out = "# pauli-x gate\n" if add_comments else ""
        out += f"X {target}\n"
        return out

    @staticmethod
    def _gate_pauli_y(target, add_comments=False):
        out = "# pauli-y gate\n" if add_comments else ""
        out += f"Y {target}\n"
        return out

    @staticmethod
    def _gate_pauli_z(target, add_comments=False):
        out = "# pauli-z gate\n" if add_comments else ""
        out += f"Z {target}\n"
        return out

    @staticmethod
    def _gate_sqrt_not(target, add_comments=False):
        out = "# sqrt-not gate\n" if add_comments else ""
        out += f"srn {target}\n"
        return out

    @staticmethod
    def _gate_t(target, add_comments=False):
        out = "# t gate\n" if add_comments else ""
        out += f"T {target}\n"
        return out

    @staticmethod
    def _gate_t_dagger(target, add_comments=False):
        out = "# t-dagger gate\n" if add_comments else ""
        out = f"PHASE (-pi / 4) {target}\n"
        return out

    @staticmethod
    def _gate_rx_theta(target, theta, add_comments=False):
        out = "# rx-theta gate\n" if add_comments else ""
        out += f"RX ({theta}) {target}\n"
        return out

    @staticmethod
    def _gate_ry_theta(target, theta, add_comments=False):
        out = "# ry-theta gate\n" if add_comments else ""
        out += f"RY ({theta}) {target}\n"
        return out

    @staticmethod
    def _gate_rz_theta(target, theta, add_comments=False):
        out = "# rz-theta gate\n" if add_comments else ""
        out += f"RZ ({theta}) {target}\n"
        return out

    @staticmethod
    def _gate_s(target, add_comments=False):
        out = "# s gate\n" if add_comments else ""
        out += f"S {target}\n"
        return out

    @staticmethod
    def _gate_s_dagger(target, add_comments=False):
        out = "# s-dagger gate\n" if add_comments else ""
        out += f"PHASE (-pi / 2) {target}\n"
        return out

    @staticmethod
    def _gate_swap(target, target2, add_comments=False):
        out = "# swap gate\n" if add_comments else ""
        out += f"SWAP {target} {target2}\n"
        return out

    @staticmethod
    def _gate_iswap(target, target2, add_comments=False):
        out = "# iswap gate\n" if add_comments else ""
        out += f"ISWAP {target} {target2}\n"
        return out

    @staticmethod
    def _gate_swap_phi(target, target2, phi, add_comments=False):
        raise BaseExporter.ExportException("The swap-phi gate is not implemented.")

    @staticmethod
    def _gate_sqrt_swap(target, target2, add_comments=False):
        out = "# sqrt-swap gate\n" if add_comments else ""
        out += f"srswap {target} {target2}\n"
        return out

    @staticmethod
    def _gate_ctrl_hadamard(control, target, add_comments=False):
        out = "# ctrl-hadamard gate\n" if add_comments else ""
        out += f"ch {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_u3(
        control, target, theta_radians, phi_radians, lambda_radians, add_comments=False
    ):
        out = "# ctrl-u3 gate\n" if add_comments else ""
        out += f"cu3 ({theta_radians} {phi_radians}, {lambda_radians}) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_u2(control, target, phi_radians, lambda_radians, add_comments=False):
        out = "# ctrl-u2 gate\n" if add_comments else ""
        out += f"cu2 ({phi_radians}, {lambda_radians}) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_u1(control, target, lambda_radians, add_comments=False):
        out = "# ctrl-u1 gate\n" if add_comments else ""
        out += f"CPHASE ({lambda_radians}) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_t(control, target, add_comments=False):
        out = "# ctrl-t gate\n" if add_comments else ""
        out += f"CPHASE (pi/4) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_t_dagger(control, target, add_comments=False):
        out = "# ctrl-t-dagger gate\n" if add_comments else ""
        out += f"CPHASE (-pi/4) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_x(control, target, add_comments=False):
        out = "# ctrl-pauli-x gate\n" if add_comments else ""
        out += f"CNOT {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_y(control, target, add_comments=False):
        out = "# ctrl-pauli-y gate\n" if add_comments else ""
        out += f"cy {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_pauli_z(control, target, add_comments=False):
        out = "# ctrl-pauli-z gate\n" if add_comments else ""
        out += f"CZ {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_sqrt_not(control, target, add_comments=False):
        out = "# ctrl-sqrt-not gate\n" if add_comments else ""
        out += f"csrn {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_rx_theta(control, target, theta_radians, add_comments=False):
        out = "# ctrl-rx-theta gate\n" if add_comments else ""
        out += f"crx ({theta_radians}) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_ry_theta(control, target, theta_radians, add_comments=False):
        out = "# ctrl-ry-theta gate\n" if add_comments else ""
        out += f"cry ({theta_radians}) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_rz_theta(control, target, theta_radians, add_comments=False):
        out = "# ctrl-rz-theta gate\n" if add_comments else ""
        out += f"crz ({theta_radians}) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_s(control, target, add_comments=False):
        out = "# ctrl-s gate\n" if add_comments else ""
        out += f"CPHASE (pi/2) {control} {target}\n"
        return out

    @staticmethod
    def _gate_ctrl_s_dagger(control, target, add_comments=False):
        out = "# ctrl-s-dagger gate\n" if add_comments else ""
        out += f"CPHASE (-pi/2) {control} {target}\n"
        return out

    @staticmethod
    def _gate_toffoli(control, control2, target, add_comments=False):
        out = "# toffoli gate\n" if add_comments else ""
        out += f"CCNOT {control} {control2} {target}\n"
        return out

    @staticmethod
    def _gate_fredkin(control, target, target2, add_comments=False):
        out = "# fredkin gate\n" if add_comments else ""
        out += f"CSWAP {control} {target} {target2}\n"
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
        out += f"MEASURE {target} ro[{classic_bit}]\n"
        return out
