"""Tests circuit composer - the python code used for
creating quantum circuits in yaml format."""

import filecmp
import pytest

from ..circuit_composer import (
    QuantumRegistry,
    QbitAleadyTaken,
    QbitIndexLargerThanRegistrySize,
)


def single_qbit_gates(args):

    return [
        f"gate_u3({args[0]}, 1, 2, 3)",
        f"gate_u2({args[1]}, 2, 3)",
        f"gate_u1({args[2]}, 2)",
        f"gate_identity({args[3]})",
        f"gate_hadamard({args[4]})",
        f"gate_pauli_x({args[5]})",
        f"gate_pauli_y({args[6]})",
        f"gate_pauli_z({args[7]})",
        f"gate_t({args[8]})",
        f"gate_t_dagger({args[9]})",
        f"gate_rx_theta({args[10]}, 12)",
        f"gate_ry_theta({args[11]}, 13)",
        f"gate_rz_theta({args[12]}, 14)",
        f"gate_s({args[13]})",
        f"gate_s_dagger({args[14]})",
        f"gate_measure_x({args[15]}, 0)",
        f"gate_measure_y({args[16]}, 0)",
        f"gate_measure_z({args[17]}, 0)",
        f"gate_pauli_x_root({args[18]}, t=2.0)",
        f"gate_pauli_y_root({args[19]}, k=7.0)",
        f"gate_pauli_z_root({args[20]}, k=9.0)",
        f"gate_pauli_x_root_dagger({args[21]}, k=23.0)",
        f"gate_pauli_y_root_dagger({args[22]}, k=12.0)",
        f"gate_pauli_z_root_dagger({args[23]}, t=8.0)",
        # repeat several gates s.t. len(single_qbit_gates)=len(two_qbit_gates)
        f"gate_u3({args[24]}, 1, 2, 3)",
        f"gate_u2({args[25]}, 2, 3)",
        f"gate_u1({args[26]}, 2)",
    ]


def two_qbit_gates(args0, args1):

    return [
        f"gate_ctrl_u3({args0[0]}, 1, {args1[0]}, 1.0, 2.0, 3.0)",
        f"gate_ctrl_u2({args0[1]}, 1, {args1[1]}, 2.0, 3.0)",
        f"gate_ctrl_u1({args0[2]}, 1, {args1[2]}, 1.0)",
        f"gate_ctrl_hadamard({args0[3]}, 1, {args1[3]})",
        f"gate_ctrl_pauli_x({args0[4]}, 1, {args1[4]})",
        f"gate_ctrl_pauli_x({args0[5]}, 1, {args1[5]})",
        f"gate_ctrl_pauli_z({args0[6]}, 1, {args1[6]})",
        f"gate_ctrl_t({args0[7]}, 1, {args1[7]})",
        f"gate_ctrl_t_dagger({args0[8]}, 1, {args1[8]})",
        f"gate_ctrl_rx_theta({args0[9]}, 1, {args1[9]}, 2.0)",
        f"gate_ctrl_ry_theta({args0[10]}, 1, {args1[10]}, 3.0)",
        f"gate_ctrl_rz_theta({args0[11]}, 1, {args1[11]}, 4.0)",
        f"gate_ctrl_s({args0[12]}, 1, {args1[12]})",
        f"gate_ctrl_s_dagger({args0[13]}, 1, {args1[13]})",
        f"gate_ctrl_pauli_x_root({args0[14]}, 1, {args1[14]}, k=2.0)",
        f"gate_ctrl_pauli_y_root({args0[15]}, 1, {args1[15]}, k=2.0)",
        f"gate_ctrl_pauli_z_root({args0[16]}, 1, {args1[16]}, k=2.0)",
        f"gate_ctrl_pauli_x_root_dagger({args0[17]}, 0, {args1[17]}, t=2.0)",
        f"gate_ctrl_pauli_y_root_dagger({args0[18]}, 0, {args1[18]}, t=2.0)",
        f"gate_ctrl_pauli_z_root_dagger({args0[19]}, 0, {args1[19]}, t=2.0)",
        f"gate_swap({args0[20]}, {args1[20]})",
        f"gate_sqrt_swap({args0[21]}, {args1[21]})",
        f"gate_swap_phi({args0[22]}, {args1[22]}, 2)",
        f"gate_iswap({args0[23]}, {args1[23]})",
        f"gate_xx({args0[24]}, {args1[24]}, 3.0)",
        f"gate_yy({args0[25]}, {args1[25]}, 4.0)",
        f"gate_zz({args0[26]}, {args1[26]}, 5.0)",
    ]


SINGLE_QBIT_GATES = single_qbit_gates([x for x in range(27)])


@pytest.mark.parametrize("gate", SINGLE_QBIT_GATES)
def test_throws_when_single_qbit_gates_repeat(gate):
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(len(SINGLE_QBIT_GATES))
        eval(f"quantum_registry.increment_step().{gate}.{gate}")


TWO_QBIT_GATES = two_qbit_gates([x for x in range(27)], [x + 1 for x in range(27)])


@pytest.mark.parametrize("gate", TWO_QBIT_GATES)
def test_throws_when_two_qbit_gates_repeat(gate):
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(len(TWO_QBIT_GATES) + 1)
        eval(f"quantum_registry.increment_step().{gate}.{gate}")


TWO_QBIT_GATES = two_qbit_gates([x for x in range(27)], [x for x in range(27)])


@pytest.mark.parametrize("gate", TWO_QBIT_GATES)
def test_assert_raised_when_two_bit_gates_are_called_with_duplicated_arguments(gate):
    with pytest.raises(AssertionError):
        quantum_registry = QuantumRegistry(len(TWO_QBIT_GATES))
        eval(f"quantum_registry.increment_step().{gate}")


SINGLE_QBIT_GATES = single_qbit_gates([x for x in range(27)])
TWO_QBIT_GATES = two_qbit_gates([x for x in range(27)], [x + 27 for x in range(27)])
GATES = [(SINGLE_QBIT_GATES[i], TWO_QBIT_GATES[i]) for i in range(27)]


@pytest.mark.parametrize("single_qbit_gate, two_qbit_gate", GATES)
def test_throws_when_single_and_control_arguments_overlap(
    single_qbit_gate, two_qbit_gate
):
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(55)
        eval(f"quantum_registry.increment_step().{single_qbit_gate}.{two_qbit_gate}")


SINGLE_QBIT_GATES = single_qbit_gates([1 for _ in range(27)])
TWO_QBIT_GATES = two_qbit_gates([0 for _ in range(27)], [2 for _ in range(27)])
GATES = [(TWO_QBIT_GATES[i], SINGLE_QBIT_GATES[i]) for i in range(27)]


@pytest.mark.parametrize("two_qbit_gate, single_qbit_gate", GATES)
def test_throws_when_qbits_overlap(two_qbit_gate, single_qbit_gate):
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(3)
        eval(f"quantum_registry.increment_step().{two_qbit_gate}.{single_qbit_gate}")


SINGLE_QBIT_GATES = single_qbit_gates([1 for _ in range(27)])


@pytest.mark.parametrize("gate", SINGLE_QBIT_GATES)
def test_throws_when_registry_is_too_small_1(gate):
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(1)
        eval(f"quantum_registry.increment_step().{gate}")


TWO_QBIT_GATES = two_qbit_gates([0 for _ in range(27)], [2 for _ in range(27)])


@pytest.mark.parametrize("gate", TWO_QBIT_GATES)
def test_throws_when_registry_is_too_small_2(gate):
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(1)
        eval(f"quantum_registry.increment_step().{gate}")


SINGLE_QBIT_GATES = single_qbit_gates([2 for _ in range(27)])
TWO_QBIT_GATES = two_qbit_gates([3 for _ in range(27)], [5 for _ in range(27)])
GATES = [(TWO_QBIT_GATES[i], SINGLE_QBIT_GATES[i]) for i in range(27)]


@pytest.mark.parametrize("single_qbit_gate, two_qbit_gate", GATES)
def test_throws_when_single_when_argument_overlap(single_qbit_gate, two_qbit_gate):
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(5)
        eval(f"quantum_registry.increment_step().{single_qbit_gate}.{two_qbit_gate}")


SINGLE_QBIT_GATES_1 = single_qbit_gates([1 for _ in range(27)])
TWO_QBIT_GATES = two_qbit_gates([3 for _ in range(27)], [5 for _ in range(27)])
GATES = [(TWO_QBIT_GATES[i], SINGLE_QBIT_GATES[i]) for i in range(27)]
SINGLE_QBIT_GATES_2 = single_qbit_gates([7 for _ in range(27)])
GATES = [
    (SINGLE_QBIT_GATES_1[i], TWO_QBIT_GATES[i], SINGLE_QBIT_GATES_2[i])
    for i in range(24)
]


@pytest.mark.parametrize("single_qbit_gate_1, two_qbit_gate, single_qbit_gate_2", GATES)
def test_no_throw(single_qbit_gate_1, two_qbit_gate, single_qbit_gate_2):
    quantum_registry = QuantumRegistry(8)
    eval(
        f"quantum_registry.increment_step().{single_qbit_gate_1}.{two_qbit_gate}.{single_qbit_gate_2}"
    )


def test_toffoli_throws():
    """Throws QbitAleadyTaken."""
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.increment_step().gate_toffoli(1, 1, 2, 1, 3).gate_toffoli(
            3, 1, 4, 1, 5
        )


def test_toffoli_throws_2():
    """Throws QbitAleadyTaken."""
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.increment_step().gate_toffoli(0, 1, 1, 1, 2).gate_toffoli(
            1, 1, 5, 1, 6
        )


def test_toffoli_throws_3():
    """Throws QbitAleadyTaken."""
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.increment_step().gate_toffoli(7, 1, 5, 1, 6).gate_toffoli(
            0, 1, 1, 1, 5
        )


def test_toffoli_throws_4():
    """Throws QbitIndexLargerThanRegistrySize."""
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.gate_hadamard(1).gate_toffoli(10, 1, 1, 1, 0)


def test_toffoli_throws_5():
    """Throws QbitIndexLargerThanRegistrySize."""
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.gate_hadamard(1).gate_toffoli(0, 1, 2, 1, 10)


def test_toffoli_throws_6():
    """Throws QbitIndexLargerThanRegistrySize."""
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.gate_hadamard(1).gate_toffoli(10, 1, 2, 1, 1)


def test_toffoli_nothrows():
    """Does not throw."""
    quantum_registry = QuantumRegistry(10)
    quantum_registry.increment_step().gate_toffoli(1, 1, 2, 1, 3)
    quantum_registry.increment_step().gate_toffoli(5, 1, 4, 1, 2)
    quantum_registry.increment_step().gate_toffoli(0, 1, 1, 1, 2)
    assert quantum_registry.current_step() == 3


def test_fredkin_throws():
    """Throws QbitAleadyTaken."""
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.increment_step().gate_fredkin(1, 1, 2, 3).gate_toffoli(
            1, 0, 3, 1, 5
        )


def test_fredkin_throws_2():
    """Throws QbitAleadyTaken."""
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.increment_step().gate_fredkin(0, 1, 1, 2).gate_fredkin(
            1, 1, 5, 6
        )


def test_fredkin_throws_3():
    """Throws QbitAleadyTaken."""
    with pytest.raises(QbitAleadyTaken):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.increment_step().gate_fredkin(7, 1, 5, 6).gate_fredkin(
            0, 1, 1, 5
        )


def test_fredkin_throws_4():
    """Throws QbitIndexLargerThanRegistrySize."""
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.gate_hadamard(1).gate_fredkin(0, 1, 2, 10)


def test_fredkin_throws_5():
    """Throws QbitIndexLargerThanRegistrySize."""
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.gate_hadamard(1).gate_fredkin(0, 1, 10, 1)


def test_fredkin_throws_6():
    """Throws QbitIndexLargerThanRegistrySize."""
    with pytest.raises(QbitIndexLargerThanRegistrySize):
        quantum_registry = QuantumRegistry(10)
        quantum_registry.gate_hadamard(1).gate_fredkin(10, 1, 2, 1)


def test_fredkin_nothrows():
    """Does not throw."""
    quantum_registry = QuantumRegistry(10)
    quantum_registry.increment_step().gate_fredkin(1, 1, 2, 3)
    quantum_registry.increment_step().gate_fredkin(5, 1, 4, 2)
    quantum_registry.increment_step().gate_fredkin(0, 1, 1, 2)
    assert quantum_registry.current_step() == 3


def test_full():
    """Test circuit_composer."""
    quantum_registry = QuantumRegistry(22)

    # single qbit gates
    quantum_registry.gate_identity(0)
    quantum_registry.gate_u3(1, 3.14 / 2, 3.14 / 2, 3.14 / 2)
    quantum_registry.gate_u2(2, 3.14 / 2, 3.14 / 2)
    quantum_registry.gate_u1(3, 3.14 / 2)
    quantum_registry.gate_identity(4)
    quantum_registry.gate_hadamard(5)
    quantum_registry.gate_pauli_x(6)
    quantum_registry.gate_pauli_y(7)
    quantum_registry.gate_pauli_z(8)
    quantum_registry.gate_t(9)
    quantum_registry.gate_t_dagger(10)
    quantum_registry.gate_rx_theta(11, 3.14 / 2)
    quantum_registry.gate_ry_theta(12, 3.14 / 2)
    quantum_registry.gate_rz_theta(13, 3.14 / 2)
    quantum_registry.gate_s(14)
    quantum_registry.gate_s_dagger(15)
    quantum_registry.gate_pauli_x_root(16, t=2.0)
    quantum_registry.gate_pauli_y_root(17, k=7.0)
    quantum_registry.gate_pauli_z_root(18, k=22.0)
    quantum_registry.gate_pauli_x_root_dagger(19, k=29.0)
    quantum_registry.gate_pauli_y_root_dagger(20, k=8.0)
    quantum_registry.gate_pauli_z_root_dagger(21, t=1.1)

    # controled single qbit gates
    quantum_registry.increment_step().gate_ctrl_u3(
        1, 1, 2, 3.14 / 2, 3.14 / 2, 3.14 / 2
    )
    quantum_registry.increment_step().gate_ctrl_u2(2, 1, 3, 3.14 / 2, 3.14 / 2)
    quantum_registry.increment_step().gate_ctrl_u1(3, 0, 4, 3.14 / 2)
    quantum_registry.increment_step().gate_ctrl_hadamard(4, 1, 5)
    quantum_registry.increment_step().gate_ctrl_pauli_x(5, 0, 6)
    quantum_registry.increment_step().gate_ctrl_pauli_y(6, 1, 7)
    quantum_registry.increment_step().gate_ctrl_pauli_z(7, 0, 8)
    quantum_registry.increment_step().gate_ctrl_t(8, 1, 9)
    quantum_registry.increment_step().gate_ctrl_t_dagger(9, 0, 10)
    quantum_registry.increment_step().gate_ctrl_rx_theta(10, 1, 11, 3.14 / 2)
    quantum_registry.increment_step().gate_ctrl_ry_theta(11, 0, 12, 3.14 / 2)
    quantum_registry.increment_step().gate_ctrl_rz_theta(12, 1, 13, 3.14 / 2)
    quantum_registry.increment_step().gate_ctrl_s(13, 0, 14)
    quantum_registry.increment_step().gate_ctrl_s_dagger(14, 1, 15)
    quantum_registry.increment_step().gate_ctrl_pauli_x_root(15, 0, 16, t=2.0)
    quantum_registry.increment_step().gate_ctrl_pauli_y_root(16, 1, 17, k=17.0)
    quantum_registry.increment_step().gate_ctrl_pauli_z_root(17, 0, 18, t=2.0)
    quantum_registry.increment_step().gate_ctrl_pauli_x_root_dagger(18, 0, 19, k=22.0)
    quantum_registry.increment_step().gate_ctrl_pauli_y_root_dagger(19, 1, 20, k=35.0)
    quantum_registry.increment_step().gate_ctrl_pauli_z_root_dagger(20, 0, 21, t=2.22)

    # swap gates
    quantum_registry.increment_step().gate_swap(1, 2)
    quantum_registry.gate_iswap(4, 5)
    quantum_registry.gate_sqrt_swap(6, 7)
    quantum_registry.gate_swap_phi(9, 10, 3.14 / 2)

    # ising gates
    quantum_registry.increment_step().gate_xx(1, 2, 0.5)
    quantum_registry.gate_yy(4, 6, 0.5)
    quantum_registry.gate_zz(8, 10, 0.5)

    # fredkin and toffoli
    quantum_registry.increment_step().gate_toffoli(4, 1, 5, 1, 6)
    quantum_registry.increment_step().gate_fredkin(7, 1, 8, 9)

    #measure gates
    quantum_registry.increment_step().gate_measure_x(0, 0)
    quantum_registry.gate_measure_y(1, 1)
    quantum_registry.gate_measure_z(2, 2)

    quantum_registry.export("test/tmp.yaml")
    assert filecmp.cmp(
        "test/tmp.yaml", "test/all_my_gates.yaml"
    ), "The output tmp.yaml file is different from reference all_my_gates.yaml file."


if __name__ == "__main__":
    pass
