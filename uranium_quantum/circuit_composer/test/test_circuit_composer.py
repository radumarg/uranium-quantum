"""Tests circuit composer - the python code used for
creating quantum circuits in yaml format."""

import filecmp
import pytest

from ..circuit_composer import (
    QuantumCircuit,
    QbitAleadyTaken,
    QbitIndexLargerThanCircuitSize,
)

TEST_DATA_SET_COUNT = 30

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
        # repeat several gates s.t. len(single_qbit_gates)=len(two_qbit_gates)
        f"gate_u3([], [{args[24]}], 1, 2, 3)",
        f"gate_u2([], [{args[25]}], 2, 3)",
        f"gate_u1([], [{args[26]}], 2)",
        f"gate_v([], [{args[27]}])",
        f"gate_v_dagger([], [{args[28]}])",
        f"gate_h([], [{args[?]}])",
        f"gate_h_dagger([], [{args[?]}])",
        f"gate_hadamard_xy([], [{args[?]}])",
        f"gate_hadamard_yz([], [{args[?]}])",
        f"gate_c([], [{args[?]}])",
        f"gate_c_dagger([], [{args[?]}])",
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
        f"gate_rz_theta([{{'target':{args0[11]}, 'state': '1'}}], [{args1[11]}], 4.0)",
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
        f"gate_sqrt_swap_dagger([], [{args0[?]}, {args1[?]}])",
        f"gate_swap_theta([], [{args0[?]}, {args1[?]}], 2)",
        f"gate_swap_root([], [{args0[?]}, {args1[?]}], 7)",
        f"gate_swap_root_dagger([], [{args0[?]}, {args1[?]}], 7)",
        f"gate_iswap([], [{args0[?]}, {args1[?]}])",
        f"gate_xx([], [{args0[?]}, {args1[?]}], 3.0)",
        f"gate_yy([], [{args0[?]}, {args1[?]}], 4.0)",
        f"gate_zz([], [{args0[?]}, {args1[?]}], 5.0)",
        f"gate_cross_resonance([], [{args0[?]}, {args1[?]}], 1.1)",
        f"gate_cross_resonance_dagger([], [{args0[?]}, {args1[?]}], 1.1)",
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
    quantum_circuit = QuantumCircuit(22)

    # single qbit gates
    quantum_circuit.gate_identity([0])
    quantum_circuit.gate_u3([], [1], 3.14 / 2, 3.14 / 2, 3.14 / 2)
    quantum_circuit.gate_u2([], [2], 3.14 / 2, 3.14 / 2)
    quantum_circuit.gate_u1([], [3], 3.14 / 2)
    quantum_circuit.gate_identity([4])
    quantum_circuit.gate_hadamard([], [5])
    quantum_circuit.gate_pauli_x([], [6])
    quantum_circuit.gate_pauli_y([], [7])
    quantum_circuit.gate_pauli_z([], [8])
    quantum_circuit.gate_t([], [9])
    quantum_circuit.gate_t_dagger([], [10])
    quantum_circuit.gate_rx_theta([], [11], 3.14 / 2)
    quantum_circuit.gate_ry_theta([], [12], 3.14 / 2)
    quantum_circuit.gate_rz_theta([], [13], 3.14 / 2)
    quantum_circuit.gate_s([], [14])
    quantum_circuit.gate_s_dagger([], [15])
    quantum_circuit.gate_pauli_x_root([], [16], t=2.0)
    quantum_circuit.gate_pauli_y_root([], [17], k=7.0)
    quantum_circuit.gate_pauli_z_root([], [18], k=22.0)
    quantum_circuit.gate_pauli_x_root_dagger([], [19], k=29.0)
    quantum_circuit.gate_pauli_y_root_dagger([], [20], k=8.0)
    quantum_circuit.gate_pauli_z_root_dagger([], [21], t=1.1)

    # # controled single qbit gates
    # quantum_circuit.increment_step().gate_u3(
    #     1, 1, 2, 3.14 / 2, 3.14 / 2, 3.14 / 2
    # )
    # quantum_circuit.increment_step().gate_u2(2, 1, 3, 3.14 / 2, 3.14 / 2)
    # quantum_circuit.increment_step().gate_u1(3, 0, 4, 3.14 / 2)
    # quantum_circuit.increment_step().gate_hadamard(4, 1, 5)
    # quantum_circuit.increment_step().gate_pauli_x(5, 0, 6)
    # quantum_circuit.increment_step().gate_pauli_y(6, 1, 7)
    # quantum_circuit.increment_step().gate_pauli_z(7, 0, 8)
    # quantum_circuit.increment_step().gate_t(8, 1, 9)
    # quantum_circuit.increment_step().gate_t_dagger(9, 0, 10)
    # quantum_circuit.increment_step().gate_rx_theta(10, 1, 11, 3.14 / 2)
    # quantum_circuit.increment_step().gate_ry_theta(11, 0, 12, 3.14 / 2)
    # quantum_circuit.increment_step().gate_rz_theta(12, 1, 13, 3.14 / 2)
    # quantum_circuit.increment_step().gate_s(13, 0, 14)
    # quantum_circuit.increment_step().gate_s_dagger(14, 1, 15)
    # quantum_circuit.increment_step().gate_pauli_x_root(15, 0, 16, t=2.0)
    # quantum_circuit.increment_step().gate_pauli_y_root(16, 1, 17, k=17.0)
    # quantum_circuit.increment_step().gate_pauli_z_root(17, 0, 18, t=2.0)
    # quantum_circuit.increment_step().gate_pauli_x_root_dagger(18, 0, 19, k=22.0)
    # quantum_circuit.increment_step().gate_pauli_y_root_dagger(19, 1, 20, k=35.0)
    # quantum_circuit.increment_step().gate_pauli_z_root_dagger(20, 0, 21, t=2.22)

    # # swap gates
    # quantum_circuit.increment_step().gate_swap(1, 2)
    # quantum_circuit.gate_iswap(4, 5)
    # quantum_circuit.gate_sqrt_swap(6, 7)
    # quantum_circuit.gate_swap_theta(9, 10, 3.14 / 2)

    # # ising gates
    # quantum_circuit.increment_step().gate_xx(1, 2, 0.5)
    # quantum_circuit.gate_yy(4, 6, 0.5)
    # quantum_circuit.gate_zz(8, 10, 0.5)

    # # fredkin and toffoli
    # quantum_circuit.increment_step().gate_toffoli(4, 1, 5, 1, 6)
    # quantum_circuit.increment_step().gate_fredkin(7, 1, 8, 9)

    #measure gates
    quantum_circuit.increment_step().gate_measure_x([0], 0)
    quantum_circuit.gate_measure_y([1], 1)
    quantum_circuit.gate_measure_z([2], 2)

    quantum_circuit.export("test/tmp.yaml")
    # assert filecmp.cmp(
    #     "test/tmp.yaml", "test/all_my_gates.yaml"
    # ), "The output tmp.yaml file is different from reference all_my_gates.yaml file."


if __name__ == "__main__":
    pass
