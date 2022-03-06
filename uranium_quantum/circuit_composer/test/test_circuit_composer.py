"""Tests circuit composer - the python code used for
creating quantum circuits in yaml format."""

import filecmp
import pytest

from ..circuit_composer import (
    QuantumCircuit,
    QbitAleadyTaken,
    QbitIndexLargerThanCircuitSize,
)

TEST_DATA_SET_COUNT = 47

def single_qbit_gates(args):

    return [
        f"gate_u3([], [{args[0]}], 1, 2, 3)",
        f"gate_u2([], [{args[1]}], 2, 3)",
        f"gate_u1([], [{args[2]}], 2)",
        f"gate_identity([{args[3]}])",
        f"gate_hadamard([], [{args[4]}])",
        f"gate_pauli_x([], [{args[5]}])",
        f"gate_pauli_y([], [{args[6]}])",
        f"gate_pauli_z([], [{args[7]}])",
        f"gate_t([], [{args[8]}])",
        f"gate_t_dagger([], [{args[9]}])",
        f"gate_rx_theta([], [{args[10]}], 12)",
        f"gate_ry_theta([], [{args[11]}], 13)",
        f"gate_rz_theta([], [{args[12]}], 14)",
        f"gate_s([], [{args[13]}])",
        f"gate_s_dagger([], [{args[14]}])",
        f"gate_measure_x([{args[15]}], 0)",
        f"gate_measure_y([{args[16]}], 0)",
        f"gate_measure_z([{args[17]}], 0)",
        f"gate_pauli_x_root([], [{args[18]}], t=2.0)",
        f"gate_pauli_y_root([], [{args[19]}], k=7.0)",
        f"gate_pauli_z_root([], [{args[20]}], k=9.0)",
        f"gate_pauli_x_root_dagger([], [{args[21]}], k=23.0)",
        f"gate_pauli_y_root_dagger([], [{args[22]}], k=12.0)",
        f"gate_pauli_z_root_dagger([], [{args[23]}], t=8.0)",
        f"gate_v([], [{args[24]}])",
        f"gate_v_dagger([], [{args[25]}])",
        f"gate_h([], [{args[26]}])",
        f"gate_h_dagger([], [{args[27]}])",
        f"gate_hadamard_xy([], [{args[28]}])",
        f"gate_hadamard_yz([], [{args[29]}])",
        f"gate_hadamard_zx([], [{args[30]}])",
        f"gate_c([], [{args[31]}])",
        f"gate_c_dagger([], [{args[32]}])",
        f"gate_p([], [{args[33]}], 0.2)",
        # repeat several gates s.t. len(single_qbit_gates)=len(two_qbit_gates)
        f"gate_u3([], [{args[34]}], 1, 2, 3)",
        f"gate_u2([], [{args[35]}], 2, 3)",
        f"gate_u1([], [{args[36]}], 2)",
        f"gate_identity([{args[37]}])",
        f"gate_hadamard([], [{args[38]}])",
        f"gate_pauli_x([], [{args[39]}])",
        f"gate_pauli_y([], [{args[40]}])",
        f"gate_pauli_z([], [{args[41]}])",
        f"gate_t([], [{args[42]}])",
        f"gate_t_dagger([], [{args[43]}])",
        f"gate_rx_theta([], [{args[44]}], 12)",
        f"gate_ry_theta([], [{args[45]}], 13)",
        f"gate_rz_theta([], [{args[46]}], 14)",
        
    ]


def two_qbit_gates(args0, args1):

    return [
        f"gate_u3([{{'target': {args0[0]}, 'state': '1'}}], [{args1[0]}], 1.0, 2.0, 3.0)",
        f"gate_u2([{{'target': {args0[1]}, 'state': '1'}}], [{args1[1]}], 2.0, 3.0)",
        f"gate_u1([{{'target': {args0[2]}, 'state': '1'}}], [{args1[2]}], 1.0)",
        f"gate_hadamard([{{'target': {args0[3]}, 'state': '1'}}], [{args1[3]}])",
        f"gate_pauli_x([{{'target': {args0[4]}, 'state': '1'}}], [{args1[4]}])",
        f"gate_pauli_x([{{'target': {args0[5]}, 'state': '1'}}], [{args1[5]}])",
        f"gate_pauli_z([{{'target': {args0[6]}, 'state': '1'}}], [{args1[6]}])",
        f"gate_t([{{'target': {args0[7]}, 'state': '1'}}], [{args1[7]}])",
        f"gate_t_dagger([{{'target': {args0[8]}, 'state': '1'}}], [{args1[8]}])",
        f"gate_rx_theta([{{'target': {args0[9]}, 'state': '1'}}], [{args1[9]}], 2.0)",
        f"gate_ry_theta([{{'target': {args0[10]}, 'state': '1'}}], [{args1[10]}], 3.0)",
        f"gate_rz_theta([{{'target': {args0[11]}, 'state': '1'}}], [{args1[11]}], 4.0)",
        f"gate_s([{{'target': {args0[12]}, 'state': '1'}}], [{args1[12]}])",
        f"gate_s_dagger([{{'target': {args0[13]}, 'state': '1'}}], [{args1[13]}])",
        f"gate_pauli_x_root([{{'target': {args0[14]}, 'state': '1'}}], [{args1[14]}], k=2.0)",
        f"gate_pauli_y_root([{{'target': {args0[15]}, 'state': '1'}}], [{args1[15]}], k=2.0)",
        f"gate_pauli_z_root([{{'target': {args0[16]}, 'state': '1'}}], [{args1[16]}], k=2.0)",
        f"gate_pauli_x_root_dagger([{{'target': {args0[17]}, 'state': '1'}}], [{args1[17]}], t=2.0)",
        f"gate_pauli_y_root_dagger([{{'target': {args0[18]}, 'state': '1'}}], [{args1[18]}], t=2.0)",
        f"gate_pauli_z_root_dagger([{{'target': {args0[19]}, 'state': '1'}}], [{args1[19]}], t=2.0)",
        f"gate_swap([], [{args0[20]}, {args1[20]}])",
        f"gate_sqrt_swap([], [{args0[21]}, {args1[21]}])",
        f"gate_sqrt_swap_dagger([], [{args0[22]}, {args1[22]}])",
        f"gate_swap_theta([], [{args0[23]}, {args1[23]}], 2)",
        f"gate_swap_root([], [{args0[24]}, {args1[24]}], 7)",
        f"gate_swap_root_dagger([], [{args0[25]}, {args1[25]}], 7)",
        f"gate_iswap([], [{args0[26]}, {args1[26]}])",
        f"gate_fswap([], [{args0[27]}, {args1[27]}])",
        f"gate_swap_root([], [{args0[28]}, {args1[28]}], 7)",
        f"gate_swap_root_dagger([], [{args0[29]}, {args1[29]}], 7)",
        f"gate_xx([], [{args0[30]}, {args1[30]}], 3.0)",
        f"gate_yy([], [{args0[31]}, {args1[31]}], 4.0)",
        f"gate_zz([], [{args0[32]}, {args1[32]}], 5.0)",
        f"gate_xy([], [{args0[33]}, {args1[33]}], 6.0)",
        f"gate_molmer_sorensen([], [{args0[34]}, {args1[34]}])",
        f"gate_molmer_sorensen_dagger([], [{args0[35]}, {args1[35]}])",
        f"gate_berkeley([], [{args0[36]}, {args1[36]}])",
        f"gate_berkeley_dagger([], [{args0[37]}, {args1[37]}])",
        f"gate_ecp([], [{args0[38]}, {args1[38]}])",
        f"gate_ecp_dagger([], [{args0[39]}, {args1[39]}])",
        f"gate_w([], [{args0[40]}, {args1[40]}])",
        f"gate_a([], [{args0[41]}, {args1[41]}], 1.1, 1.2)",
        f"gate_magic([], [{args0[42]}, {args1[42]}])",
        f"gate_magic_dagger([], [{args0[43]}, {args1[43]}])",
        f"gate_givens([], [{args0[44]}, {args1[44]}], 1.1)",
        f"gate_cross_resonance([], [{args0[45]}, {args1[45]}], 1.1)",
        f"gate_cross_resonance_dagger([], [{args0[46]}, {args1[46]}], 1.1)",
    ]


SINGLE_QBIT_GATES = single_qbit_gates([x for x in range(TEST_DATA_SET_COUNT)])


@pytest.mark.parametrize("gate", SINGLE_QBIT_GATES)
def test_throws_when_single_qbit_gates_repeat(gate):
    with pytest.raises(QbitAleadyTaken):
        quantum_circuit = QuantumCircuit(len(SINGLE_QBIT_GATES))
        eval(f"quantum_circuit.increment_step().{gate}.{gate}")


TWO_QBIT_GATES = two_qbit_gates([x for x in range(TEST_DATA_SET_COUNT)], [x + 1 for x in range(TEST_DATA_SET_COUNT)])


@pytest.mark.parametrize("gate", TWO_QBIT_GATES)
def test_throws_when_two_qbit_gates_repeat(gate):
    with pytest.raises(QbitAleadyTaken):
        quantum_circuit = QuantumCircuit(len(TWO_QBIT_GATES) + 1)
        eval(f"quantum_circuit.increment_step().{gate}.{gate}")


TWO_QBIT_GATES = two_qbit_gates([x for x in range(TEST_DATA_SET_COUNT)], [x for x in range(TEST_DATA_SET_COUNT)])


@pytest.mark.parametrize("gate", TWO_QBIT_GATES)
def test_assert_raised_when_two_bit_gates_are_called_with_duplicated_arguments(gate):
    with pytest.raises(AssertionError):
        quantum_circuit = QuantumCircuit(len(TWO_QBIT_GATES))
        eval(f"quantum_circuit.increment_step().{gate}")


SINGLE_QBIT_GATES = single_qbit_gates([x for x in range(TEST_DATA_SET_COUNT)])
TWO_QBIT_GATES = two_qbit_gates([x for x in range(TEST_DATA_SET_COUNT)], [x + TEST_DATA_SET_COUNT for x in range(TEST_DATA_SET_COUNT)])
GATES = [(SINGLE_QBIT_GATES[i], TWO_QBIT_GATES[i]) for i in range(TEST_DATA_SET_COUNT)]


@pytest.mark.parametrize("single_qbit_gate, two_qbit_gate", GATES)
def test_throws_when_single_and_control_arguments_overlap(
    single_qbit_gate, two_qbit_gate
):
    with pytest.raises(QbitAleadyTaken):
        quantum_circuit = QuantumCircuit(55)
        eval(f"quantum_circuit.increment_step().{single_qbit_gate}.{two_qbit_gate}")


SINGLE_QBIT_GATES = single_qbit_gates([1 for _ in range(TEST_DATA_SET_COUNT)])
TWO_QBIT_GATES = two_qbit_gates([0 for _ in range(TEST_DATA_SET_COUNT)], [2 for _ in range(TEST_DATA_SET_COUNT)])
GATES = [(TWO_QBIT_GATES[i], SINGLE_QBIT_GATES[i]) for i in range(TEST_DATA_SET_COUNT)]


@pytest.mark.parametrize("two_qbit_gate, single_qbit_gate", GATES)
def test_throws_when_qbits_overlap(two_qbit_gate, single_qbit_gate):
    with pytest.raises(QbitAleadyTaken):
        quantum_circuit = QuantumCircuit(3)
        eval(f"quantum_circuit.increment_step().{two_qbit_gate}.{single_qbit_gate}")


SINGLE_QBIT_GATES = single_qbit_gates([1 for _ in range(TEST_DATA_SET_COUNT)])


@pytest.mark.parametrize("gate", SINGLE_QBIT_GATES)
def test_throws_when_circuit_is_too_small_1(gate):
    with pytest.raises(QbitIndexLargerThanCircuitSize):
        quantum_circuit = QuantumCircuit(1)
        eval(f"quantum_circuit.increment_step().{gate}")


TWO_QBIT_GATES = two_qbit_gates([0 for _ in range(TEST_DATA_SET_COUNT)], [2 for _ in range(TEST_DATA_SET_COUNT)])


@pytest.mark.parametrize("gate", TWO_QBIT_GATES)
def test_throws_when_circuit_is_too_small_2(gate):
    with pytest.raises(QbitIndexLargerThanCircuitSize):
        quantum_circuit = QuantumCircuit(1)
        eval(f"quantum_circuit.increment_step().{gate}")


SINGLE_QBIT_GATES = single_qbit_gates([2 for _ in range(TEST_DATA_SET_COUNT)])
TWO_QBIT_GATES = two_qbit_gates([3 for _ in range(TEST_DATA_SET_COUNT)], [5 for _ in range(TEST_DATA_SET_COUNT)])
GATES = [(TWO_QBIT_GATES[i], SINGLE_QBIT_GATES[i]) for i in range(TEST_DATA_SET_COUNT)]


@pytest.mark.parametrize("single_qbit_gate, two_qbit_gate", GATES)
def test_throws_when_single_when_argument_overlap(single_qbit_gate, two_qbit_gate):
    with pytest.raises(QbitIndexLargerThanCircuitSize):
        quantum_circuit = QuantumCircuit(5)
        eval(f"quantum_circuit.increment_step().{single_qbit_gate}.{two_qbit_gate}")


SINGLE_QBIT_GATES_1 = single_qbit_gates([1 for _ in range(TEST_DATA_SET_COUNT)])
TWO_QBIT_GATES = two_qbit_gates([3 for _ in range(TEST_DATA_SET_COUNT)], [5 for _ in range(TEST_DATA_SET_COUNT)])
GATES = [(TWO_QBIT_GATES[i], SINGLE_QBIT_GATES[i]) for i in range(TEST_DATA_SET_COUNT)]
SINGLE_QBIT_GATES_2 = single_qbit_gates([7 for _ in range(TEST_DATA_SET_COUNT)])
GATES = [
    (SINGLE_QBIT_GATES_1[i], TWO_QBIT_GATES[i], SINGLE_QBIT_GATES_2[i])
    for i in range(24)
]


@pytest.mark.parametrize("single_qbit_gate_1, two_qbit_gate, single_qbit_gate_2", GATES)
def test_no_throw(single_qbit_gate_1, two_qbit_gate, single_qbit_gate_2):
    quantum_circuit = QuantumCircuit(8)
    eval(
        f"quantum_circuit.increment_step().{single_qbit_gate_1}.{two_qbit_gate}.{single_qbit_gate_2}"
    )


def test_full():
    """Test circuit_composer."""
    quantum_circuit = QuantumCircuit(33)

    # single qbit gates
    quantum_circuit.gate_u3([], [1], 3.14 / 2, 3.14 / 2, 3.14 / 2)
    quantum_circuit.gate_u2([], [2], 3.14 / 2, 3.14 / 2)
    quantum_circuit.gate_u1([], [3], 3.14 / 2)
    quantum_circuit.gate_identity([4])
    quantum_circuit.gate_hadamard([], [5])
    quantum_circuit.gate_hadamard_xy([], [6])
    quantum_circuit.gate_hadamard_yz([], [7])
    quantum_circuit.gate_hadamard_zx([], [8])
    quantum_circuit.gate_pauli_x([], [9])
    quantum_circuit.gate_pauli_y([], [10])
    quantum_circuit.gate_pauli_z([], [11])
    quantum_circuit.gate_pauli_x_root([], [12], t=2.0)
    quantum_circuit.gate_pauli_y_root([], [13], k=7.0)
    quantum_circuit.gate_pauli_z_root([], [14], k=22.0)
    quantum_circuit.gate_pauli_x_root_dagger([], [15], k=29.0)
    quantum_circuit.gate_pauli_y_root_dagger([], [16], k=8.0)
    quantum_circuit.gate_pauli_z_root_dagger([], [17], t=1.1)
    quantum_circuit.gate_rx_theta([], [18], 3.14 / 2)
    quantum_circuit.gate_ry_theta([], [19], 3.14 / 2)
    quantum_circuit.gate_rz_theta([], [20], 3.14 / 2)
    quantum_circuit.gate_t([], [21])
    quantum_circuit.gate_t_dagger([], [22])
    quantum_circuit.gate_s([], [23])
    quantum_circuit.gate_s_dagger([], [24])
    quantum_circuit.gate_v([], [25])
    quantum_circuit.gate_v_dagger([], [26])
    quantum_circuit.gate_h([], [27])
    quantum_circuit.gate_h_dagger([], [28])
    quantum_circuit.gate_c([], [29])
    quantum_circuit.increment_step().gate_c_dagger([], [0])
    quantum_circuit.gate_p([], [1], 0.5)
    quantum_circuit.gate_measure_z([2], 32)

    # # controled single qbit gates
    quantum_circuit.increment_step().gate_u3([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [2], 3.14 / 2, 3.14 / 2, 3.14 / 2)
    quantum_circuit.increment_step().gate_u2([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [3], 3.14 / 2, 3.14 / 2)
    quantum_circuit.increment_step().gate_u1([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [4], 3.14 / 2)
    quantum_circuit.increment_step().gate_hadamard([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [5])
    quantum_circuit.increment_step().gate_hadamard_xy([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [6])
    quantum_circuit.increment_step().gate_hadamard_yz([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [7])
    quantum_circuit.increment_step().gate_hadamard_zx([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [8])
    quantum_circuit.increment_step().gate_pauli_x([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [9])
    quantum_circuit.increment_step().gate_pauli_y([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [10])
    quantum_circuit.increment_step().gate_pauli_z([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [11])
    quantum_circuit.increment_step().gate_pauli_x_root([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [12], t=2.0)
    quantum_circuit.increment_step().gate_pauli_y_root([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [13], k=7.0)
    quantum_circuit.increment_step().gate_pauli_z_root([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [14], k=22.0)
    quantum_circuit.increment_step().gate_pauli_x_root_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [15], k=29.0)
    quantum_circuit.increment_step().gate_pauli_y_root_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [16], k=8.0)
    quantum_circuit.increment_step().gate_pauli_z_root_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [17], t=1.1)
    quantum_circuit.increment_step().gate_rx_theta([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [18], 3.14 / 2)
    quantum_circuit.increment_step().gate_ry_theta([{'target': 0, 'state': '1'}, {'target': 1, 'state': '+i'}], [19], 3.14 / 2)
    quantum_circuit.increment_step().gate_rz_theta([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [20], 3.14 / 2)
    quantum_circuit.increment_step().gate_t([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [21])
    quantum_circuit.increment_step().gate_t_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [22])
    quantum_circuit.increment_step().gate_s([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [23])
    quantum_circuit.increment_step().gate_s_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [24])
    quantum_circuit.increment_step().gate_v([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [25])
    quantum_circuit.increment_step().gate_v_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [26])
    quantum_circuit.increment_step().gate_h([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [27])
    quantum_circuit.increment_step().gate_h_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [28])
    quantum_circuit.increment_step().gate_c([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [29])
    quantum_circuit.increment_step().gate_c_dagger([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [2])
    quantum_circuit.increment_step().gate_p([{'target': 0, 'state': '1'}, {'target': 1, 'state': '-'}], [3], 0.2)

    # two qbit gates
    quantum_circuit.increment_step().gate_swap([], [0, 1])
    quantum_circuit.gate_sqrt_swap([], [2, 3])
    quantum_circuit.gate_sqrt_swap_dagger([], [4, 5])
    quantum_circuit.gate_swap_theta([], [6, 7], 1.1)
    quantum_circuit.gate_iswap([], [8, 9])
    quantum_circuit.gate_fswap([], [10, 11])
    quantum_circuit.gate_swap_root([], [12, 13], 2.1)
    quantum_circuit.gate_swap_root_dagger([], [14, 15], 2.1)
    quantum_circuit.gate_xx([], [16, 17], 0.22)
    quantum_circuit.gate_yy([], [18, 19], 0.22)
    quantum_circuit.gate_zz([], [20, 21], 0.22)
    quantum_circuit.gate_xy([], [22, 23], 0.22)
    quantum_circuit.gate_molmer_sorensen([], [24, 25])
    quantum_circuit.increment_step().gate_molmer_sorensen_dagger([], [0, 1])
    quantum_circuit.gate_berkeley([], [2, 3])
    quantum_circuit.gate_berkeley_dagger([], [4, 5])
    quantum_circuit.gate_ecp([], [6, 7])
    quantum_circuit.gate_ecp_dagger([], [8, 9])
    quantum_circuit.gate_w([], [10, 11])
    quantum_circuit.gate_a([], [12, 13], 1.22, 1.44)
    quantum_circuit.gate_magic([], [14, 15])
    quantum_circuit.gate_magic_dagger([], [16, 17])
    quantum_circuit.gate_cross_resonance([], [18, 19], 0.1)
    quantum_circuit.gate_cross_resonance_dagger([], [20, 21], 0.2)
    quantum_circuit.gate_givens([], [22, 23], 2.1)

    # controlled two qbit gates
    quantum_circuit.increment_step().gate_swap([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4])
    quantum_circuit.increment_step().gate_sqrt_swap([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4])
    quantum_circuit.increment_step().gate_sqrt_swap_dagger([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4])
    quantum_circuit.increment_step().gate_swap_theta([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 1.2)
    quantum_circuit.increment_step().gate_iswap([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4])
    quantum_circuit.increment_step().gate_fswap([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4])
    quantum_circuit.increment_step().gate_swap_root([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 2)
    quantum_circuit.increment_step().gate_swap_root_dagger([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 3)
    quantum_circuit.increment_step().gate_xx([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 0.1)
    quantum_circuit.increment_step().gate_yy([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 0.1)
    quantum_circuit.increment_step().gate_zz([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 0.1)
    quantum_circuit.increment_step().gate_xy([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-i'}], [3,4], 0.1)
    quantum_circuit.increment_step().gate_molmer_sorensen([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_molmer_sorensen_dagger([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_berkeley([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_berkeley_dagger([{'target': 0, 'state': '-'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_ecp([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_ecp_dagger([{'target': 0, 'state': '+'}, {'target': 1, 'state': '-i'}], [3,4])
    quantum_circuit.increment_step().gate_w([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_a([{'target': 0, 'state': '0'}, {'target': 1, 'state': '-'}], [3,4], 0.1, 0.2)
    quantum_circuit.increment_step().gate_magic([{'target': 0, 'state': '+'}, {'target': 1, 'state': '+'}], [3,4])
    quantum_circuit.increment_step().gate_magic_dagger([{'target': 0, 'state': '+'}, {'target': 1, 'state': '-'}], [3,4])
    quantum_circuit.increment_step().gate_cross_resonance([{'target': 0, 'state': '+'}, {'target': 1, 'state': '-'}], [3,4], 0.1)
    quantum_circuit.increment_step().gate_cross_resonance_dagger([{'target': 0, 'state': '-'}, {'target': 1, 'state': '+i'}], [3,4], 0.1)
    quantum_circuit.increment_step().gate_givens([{'target': 0, 'state': '-'}, {'target': 1, 'state': '+i'}], [3,4], 0.1)
    
    quantum_circuit.export("test/tmp.yaml")

    assert filecmp.cmp(
        "test/tmp.yaml", "test/all_my_gates.yaml"
    ), "The output tmp.yaml file is different from reference all_my_gates.yaml file."


if __name__ == "__main__":
    pass
