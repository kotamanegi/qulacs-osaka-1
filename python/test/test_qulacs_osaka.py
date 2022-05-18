
# set library dir
import qulacs_osaka as qulacs
import unittest
import numpy as np
import warnings
import sys
from scipy.sparse import lil_matrix
for ind in range(1, len(sys.argv)):
    sys.path.append(sys.argv[ind])
sys.argv = sys.argv[:1]


class TestStateVector(unittest.TestCase):
    def setUp(self):
        self.n = 4
        self.dim = 2**self.n
        self.state = qulacs.StateVector(self.n)

    def tearDown(self):
        del self.state

    def test_state_dim(self):
        vector = self.state.get_vector()
        self.assertEqual(len(vector), self.dim, msg="check vector size")

    def test_zero_state(self):
        self.state.set_zero_state()
        vector = self.state.get_vector()
        vector_ans = np.zeros(self.dim)
        vector_ans[0] = 1.
        self.assertTrue(((vector - vector_ans) < 1e-10).all(),
                        msg="check set_zero_state")

    def test_comp_basis(self):
        pos = 0b0101
        self.state.set_computational_basis(pos)
        vector = self.state.get_vector()
        vector_ans = np.zeros(self.dim)
        vector_ans[pos] = 1.
        self.assertTrue(((vector - vector_ans) < 1e-10).all(),
                        msg="check set_computational_basis")


class TestQuantumCircuit(unittest.TestCase):
    def setUp(self):
        self.n = 4
        self.dim = 2**self.n
        self.state = qulacs.StateVector(self.n)
        self.circuit = qulacs.QuantumCircuit(self.n)

    def tearDown(self):
        del self.state
        del self.circuit

    def test_make_bell_state(self):
        self.circuit.add_gate(qulacs.gate.H(0))
        self.circuit.add_gate(qulacs.gate.CNOT(0, 1))
        self.state.set_zero_state()
        self.circuit.update_quantum_state(self.state)
        vector = self.state.get_vector()
        vector_ans = np.zeros(self.dim)
        vector_ans[0] = np.sqrt(0.5)
        vector_ans[3] = np.sqrt(0.5)
        self.assertTrue(((vector - vector_ans) < 1e-10).all(),
                        msg="check make bell state")


class TestObservable(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    """
    def test_get_matrix(self):
        n_qubits = 3
        obs = qulacs.Observable()
        obs.add_term(.5, "Z 2")
        obs.add_term(1., "X 0 X 1 X 2")
        obs.add_term(1., "Y 1")
        ans = np.array(
            [
                [.5, 0, -1j, 0, 0, 0, 0, 1],
                [0, .5, 0, -1j, 0, 0, 1, 0],
                [1j, 0, .5, 0, 0, 1, 0, 0],
                [0, 1j, 0, .5, 1, 0, 0, 0],
                [0, 0, 0, 1, -.5, 0, -1j, 0],
                [0, 0, 1, 0, 0, -.5, 0, -1j],
                [0, 1, 0, 0, 1j, 0, -.5, 0],
                [1, 0, 0, 0, 0, 1j, 0, -.5],
            ], dtype=np.complex128
        )
        self.assertLessEqual(np.linalg.norm(
            ans-obs.get_matrix().todense()), 1e-6)
        obs = qulacs.GeneralQuantumOperator(n_qubits)
        obs.add_term(.5j, "Z 2")
        obs.add_term(1., "X 0 X 1 X 2")
        obs.add_term(1., "Y 1")
        ans = np.array(
            [
                [.5j, 0, -1j, 0, 0, 0, 0, 1],
                [0, .5j, 0, -1j, 0, 0, 1, 0],
                [1j, 0, .5j, 0, 0, 1, 0, 0],
                [0, 1j, 0, .5j, 1, 0, 0, 0],
                [0, 0, 0, 1, -.5j, 0, -1j, 0],
                [0, 0, 1, 0, 0, -.5j, 0, -1j],
                [0, 1, 0, 0, 1j, 0, -.5j, 0],
                [1, 0, 0, 0, 0, 1j, 0, -.5j],
            ], dtype=np.complex128
        )
        self.assertLessEqual(np.linalg.norm(
            ans-obs.get_matrix().todense()), 1e-6)
    """


class TestPointerHandling(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pointer_del(self):
        qc = qulacs.QuantumCircuit(1)
        gate = qulacs.gate.X(0)
        qc.add_gate(gate)
        del gate
        del qc

    def test_internal_return_value_of_get_gate_is_valid(self):

        def func():
            def copy_circuit(c):
                ret = qulacs.QuantumCircuit(2)
                for i in range(c.get_gate_count()):
                    gate = c.get_gate(i)
                    ret.add_gate(gate)
                return ret

            circuit = qulacs.QuantumCircuit(2)
            circuit.add_gate(qulacs.gate.X(0))
            circuit.add_gate(qulacs.gate.Y(1))
            copied = copy_circuit(circuit)
            return copied

        def func2():
            qs = qulacs.StateVector(2)
            circuit = func()
            circuit.update_quantum_state(qs)

        func2()

    """
    def test_circuit_add_gate(self):
        from qulacs_osaka.gate import Identity, X, Y, Z, H, S, Sdag, T, Tdag, sqrtX, sqrtXdag, sqrtY, sqrtYdag
        from qulacs_osaka.gate import P0, P1, RX, RY, RZ, CNOT, CZ, SWAP, TOFFOLI, FREDKIN, Pauli, PauliRotation
        # from qulacs_osaka.gate import U1, U2, U3
        from qulacs_osaka.gate import DenseMatrix, SparseMatrix, DiagonalMatrix, RandomUnitary, ReversibleBoolean, StateReflection
        from qulacs_osaka.gate import BitFlipNoise, DephasingNoise, IndependentXZNoise, DepolarizingNoise, TwoQubitDepolarizingNoise, AmplitudeDampingNoise, Measurement
        from qulacs_osaka.gate import merge, add, to_matrix_gate, Probabilistic, CPTP, Instrument, Adaptive
        qc = qulacs.QuantumCircuit(3)
        qs = qulacs.StateVector(3)
        ref = qulacs.StateVector(3)
        sparse_mat = lil_matrix((4, 4))
        sparse_mat[0, 0] = 1
        sparse_mat[1, 1] = 1

        def func(v, d):
            return (v + 1) % d

        def adap(v):
            return True

        gates = [
            Identity(0), X(0), Y(0), Z(0), H(0), S(0), Sdag(0), T(
                0), Tdag(0), sqrtX(0), sqrtXdag(0), sqrtY(0), sqrtYdag(0),
            Probabilistic([X(0), Y(0)], [0.5, 0.5]), CPTP(
                [P0(0), P1(0)]), Instrument([P0(0), P1(0)], 1), Adaptive(X(0), adap),
            CNOT(0, 1), CZ(0, 1), SWAP(0, 1), TOFFOLI(0, 1, 2), FREDKIN(
                0, 1, 2), Pauli([0, 1], [1, 2]), PauliRotation([0, 1], [1, 2], 0.1),
            DenseMatrix(0, np.eye(2)), DenseMatrix(
                [0, 1], np.eye(4)), SparseMatrix([0, 1], sparse_mat),
            DiagonalMatrix([0, 1], np.ones(4)), RandomUnitary(
                [0, 1]), ReversibleBoolean([0, 1], func), StateReflection(ref),
            BitFlipNoise(0, 0.1), DephasingNoise(0, 0.1), IndependentXZNoise(
                0, 0.1), DepolarizingNoise(0, 0.1), TwoQubitDepolarizingNoise(0, 1, 0.1),
            AmplitudeDampingNoise(0, 0.1), Measurement(0, 1), merge(
                X(0), Y(1)), add(X(0), Y(1)), to_matrix_gate(X(0)),
            P0(0), P1(0), RX(0, 0.), RY(0, 0.), RZ(0, 0.),
        ]
        # U1(0, 0.), U2(0, 0., 0.), U3(0, 0., 0., 0.)
        gates.append(merge(gates[0], gates[1]))
        gates.append(add(gates[0], gates[1]))

        ref = None
        for gate in gates:
            qc.add_gate(gate)

        for gate in gates:
            qc.add_gate(gate)

        qc.update_quantum_state(qs)
        qc = None
        qs = None
        for gate in gates:
            gate = None

        gates = None
        parametric_gates = None

    def test_circuit_add_parametric_gate(self):
        from qulacs_osaka.gate import Identity, X, Y, Z, H, S, Sdag, T, Tdag, sqrtX, sqrtXdag, sqrtY, sqrtYdag
        from qulacs_osaka.gate import P0, P1, RX, RY, RZ, CNOT, CZ, SWAP, TOFFOLI, FREDKIN, Pauli, PauliRotation
        # U1, U2, U3
        from qulacs_osaka.gate import DenseMatrix, SparseMatrix, DiagonalMatrix, RandomUnitary, ReversibleBoolean, StateReflection
        from qulacs_osaka.gate import BitFlipNoise, DephasingNoise, IndependentXZNoise, DepolarizingNoise, TwoQubitDepolarizingNoise, AmplitudeDampingNoise, Measurement
        from qulacs_osaka.gate import merge, add, to_matrix_gate, Probabilistic, CPTP, Instrument, Adaptive
        from qulacs_osaka.gate import ParametricRX, ParametricRY, ParametricRZ, ParametricPauliRotation
        qc = qulacs.QuantumCircuit(3)
        qs = qulacs.StateVector(3)
        ref = qulacs.StateVector(3)
        sparse_mat = lil_matrix((4, 4))
        sparse_mat[0, 0] = 1
        sparse_mat[1, 1] = 1

        def func(v, d):
            return (v + 1) % d

        def adap(v):
            return True

        gates = [
            Identity(0), X(0), Y(0), Z(0), H(0), S(0), Sdag(0), T(
                0), Tdag(0), sqrtX(0), sqrtXdag(0), sqrtY(0), sqrtYdag(0),
            Probabilistic([X(0), Y(0)], [0.5, 0.5]), CPTP(
                [P0(0), P1(0)]), Instrument([P0(0), P1(0)], 1), Adaptive(X(0), adap),
            CNOT(0, 1), CZ(0, 1), SWAP(0, 1), TOFFOLI(0, 1, 2), FREDKIN(
                0, 1, 2), Pauli([0, 1], [1, 2]), PauliRotation([0, 1], [1, 2], 0.1),
            DenseMatrix(0, np.eye(2)), DenseMatrix(
                [0, 1], np.eye(4)), SparseMatrix([0, 1], sparse_mat),
            DiagonalMatrix([0, 1], np.ones(4)), RandomUnitary(
                [0, 1]), ReversibleBoolean([0, 1], func), StateReflection(ref),
            BitFlipNoise(0, 0.1), DephasingNoise(0, 0.1), IndependentXZNoise(
                0, 0.1), DepolarizingNoise(0, 0.1), TwoQubitDepolarizingNoise(0, 1, 0.1),
            AmplitudeDampingNoise(0, 0.1), Measurement(0, 1), merge(
                X(0), Y(1)), add(X(0), Y(1)), to_matrix_gate(X(0)),
            P0(0), P1(0), RX(0, 0.), RY(0, 0.), RZ(0, 0.),
        ]
        # U1(0, 0.), U2(0, 0., 0.), U3(0, 0., 0., 0.)
        gates.append(merge(gates[0], gates[1]))
        gates.append(add(gates[0], gates[1]))

        parametric_gates = [
            ParametricRX(0, 0.1), ParametricRY(0, 0.1), ParametricRZ(
                0, 0.1), ParametricPauliRotation([0, 1], [1, 1], 0.1)
        ]

        ref = None
        for gate in gates:
            qc.add_gate(gate)

        for gate in gates:
            qc.add_gate(gate)

        for pgate in parametric_gates:
            qc.add_parametric_gate(pgate)

        for pgate in parametric_gates:
            qc.add_parametric_gate(pgate)

        qc.update_quantum_state(qs)
        qc = None
        qs = None
        for gate in gates:
            gate = None
        for pgate in parametric_gates:
            gate = None

        gates = None
        parametric_gates = None
    """
    def test_add_same_gate_multiple_time(self):
        from qulacs_osaka.gate import X, DepolarizingNoise, DephasingNoise, Probabilistic, RX
        state = qulacs.StateVector(1)
        circuit = qulacs.QuantumCircuit(1)
        noise = DepolarizingNoise(0, 0)
        circuit.add_gate(noise)
        circuit.add_gate(noise.copy())
        circuit.add_gate(DephasingNoise(0, 0))
        circuit.add_gate(Probabilistic([RX(0, 0)], [0.1]))
        gate = RX(0, 0)
        circuit.add_gate(gate)
        circuit.add_gate(gate)
        circuit.add_gate(gate)
        circuit.add_gate(gate)
        circuit.add_gate(gate)
        del gate
        circuit.update_quantum_state(state)
        circuit.update_quantum_state(state)
        circuit.update_quantum_state(state)
        circuit.update_quantum_state(state)
        circuit.update_quantum_state(state)
        circuit.update_quantum_state(state)
        circuit.update_quantum_state(state)
        circuit.to_string()
        del circuit
        del state

    def test_observable(self):
        obs = qulacs.Observable()
        obs.add_term(1.0, "X 0")
        term = obs.get_term(0)
        del term

    def test_add_gate(self):
        circuit = qulacs.QuantumCircuit(1)
        gate = qulacs.gate.X(0)
        circuit.add_gate(gate)
        del gate
        s = circuit.to_string()
        del circuit

    def test_add_gate_in_parametric_circuit(self):
        circuit = qulacs.QuantumCircuit(1)
        gate = qulacs.gate.X(0)
        circuit.add_gate(gate)
        del gate
        s = circuit.to_string()
        del circuit

    """
    def test_state_reflection(self):
        n = 5
        s1 = qulacs.StateVector(n)

        def gen_gate():
            s2 = qulacs.StateVector(n)
            gate = qulacs.gate.StateReflection(s2)
            del s2
            return gate
        gate = gen_gate()
        gate.update_quantum_state(s1)
        del gate
        del s1
    """

    def test_sparse_matrix(self):
        n = 5
        state = qulacs.StateVector(n)
        matrix = lil_matrix((4, 4), dtype=np.complex128)
        matrix[0, 0] = 1 + 1.j
        matrix[1, 1] = 1. + 1.j
        gate = qulacs.gate.SparseMatrix([0, 1], matrix)
        gate.update_quantum_state(state)
        del gate
        del state

    def test_random_unitary(self):
        n = 3
        state = qulacs.StateVector(n)
        gate = qulacs.gate.RandomUnitary([0,1], 0)
        gate.update_quantum_state(state)
        matrix = gate.get_matrix()
        self.assertTrue(np.allclose(matrix@matrix.T.conj(), np.eye(4)))
        del state
        del gate

    """
    def test_copied_parametric_gate(self):

        def f():
            circuit = qulacs.QuantumCircuit(1)
            gate = qulacs.gate.ParametricRX(0, 0.1)
            circuit.add_parametric_gate(gate)
            circuit.add_parametric_gate(gate)
            circuit.add_gate(gate)
            gate.set_parameter_value(0.2)
            circuit.add_parametric_gate(gate)
            circuit.add_parametric_RX_gate(0, 0.3)
            gate2 = gate.copy()
            gate2.set_parameter_value(0.4)
            gate.set_parameter_value(1.0)
            del gate
            circuit.add_parametric_gate(gate2)
            circuit.remove_gate(1)
            del gate2
            return circuit

        c = f()
        for gc in range(c.get_parameter_count()):
            val = c.get_parameter(gc)
            c.set_parameter(gc, val + 1.0)
            self.assertAlmostEqual(val, gc * 0.1 + 0.1,
                                   msg="check vector size")

        d = c.copy()
        del c
        for gc in range(d.get_parameter_count()):
            val = d.get_parameter(gc)
            d.set_parameter(gc, val + 10)
            val = d.get_parameter(gc)
            self.assertAlmostEqual(val, 11.1 + gc * 0.1,
                                   msg="check vector size")

        qs = qulacs.StateVector(1)
        d.update_quantum_state(qs)
        del d
        del qs

    def test_parametric_gate_position(self):

        def check(pqc, idlist):
            cnt = pqc.get_parameter_count()
            self.assertEqual(cnt, len(idlist))
            for ind in range(cnt):
                pos = pqc.get_parametric_gate_position(ind)
                self.assertEqual(pos, idlist[ind])

        pqc = qulacs.QuantumCircuit(1)
        gate = qulacs.gate.ParametricRX(0, 0.1)
        pqc.add_parametric_gate(gate)  # [0]
        check(pqc, [0])
        pqc.add_parametric_gate(gate)  # [0, 1]
        check(pqc, [0, 1])
        pqc.add_gate(gate)  # [0, 1, *]
        check(pqc, [0, 1])
        pqc.add_parametric_gate(gate, 0)  # [2, 0, 1, *]
        check(pqc, [1, 2, 0])
        pqc.add_gate(gate, 0)  # [*, 2, 0, 1, *]
        check(pqc, [2, 3, 1])
        pqc.add_parametric_gate(gate, 0)  # [3, *, 2, 0, 1, *]
        check(pqc, [3, 4, 2, 0])
        pqc.remove_gate(4)  # [2, *, 1, 0, *]
        check(pqc, [3, 2, 0])
        pqc.remove_gate(1)  # [2, 1, 0, *]
        check(pqc, [2, 1, 0])
        pqc.add_parametric_gate(gate)  # [2, 1, 0, *, 3]
        check(pqc, [2, 1, 0, 4])
        pqc.add_parametric_gate(gate, 2)  # [2, 1, 4, 0, *, 3]
        check(pqc, [3, 1, 0, 5, 2])
        pqc.remove_gate(3)  # [1, 0, 3, *, 2]
        check(pqc, [1, 0, 4, 2])
    """

class TestUtils(unittest.TestCase):
    def setUp(self):
        # suppress warning from openfermion/cirq
        warnings.simplefilter('ignore', category=DeprecationWarning)

    def tearDown(self):
        pass

    """
    def test_convert_openfermion_op(self):
        from qulacs.utils import convert_openfermion_op
        from openfermion import QubitOperator
        openfermion_op = QubitOperator()
        openfermion_op += 1. * QubitOperator("X0")
        openfermion_op += 2. * QubitOperator("Z0 Y1")
        openfermion_op += 1. * QubitOperator("Z0 Y3")

        qulacs_op = convert_openfermion_op(openfermion_op)
        str_qulacs_op = str(qulacs_op)
        # operator ordering in openfermion may differ sometimes so we have to do this
        str_qulacs_op = str_qulacs_op.replace("(1,0) X 0", "")
        str_qulacs_op = str_qulacs_op.replace("(2,0) Z 0 Y 1", "")
        str_qulacs_op = str_qulacs_op.replace("(1,0) Z 0 Y 3", "")
        self.assertEqual(str_qulacs_op, " +  + ")
    """

class TestDensityMatrixHandling(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_density_matrix(self):
        num_qubit = 5
        sv = qulacs.StateVector(num_qubit)
        dm = qulacs.DensityMatrix(num_qubit)
        sv.set_Haar_random_state(seed=0)
        dm.load(sv)
        svv = np.atleast_2d(sv.get_vector()).T
        mat = np.dot(svv, svv.T.conj())
        self.assertTrue(np.allclose(dm.get_matrix(), mat), msg="check pure matrix to density matrix")
        

    def test_tensor_product_sv(self):
        num_qubit = 4
        sv1 = qulacs.StateVector(num_qubit)
        sv2 = qulacs.StateVector(num_qubit)
        sv1.set_Haar_random_state(seed=0)
        sv2.set_Haar_random_state(seed=1)
        sv3 = qulacs.state.tensor_product(sv1, sv2)
        sv3_test = np.kron(sv1.get_vector(), sv2.get_vector())
        self.assertTrue(np.allclose(sv3_test, sv3.get_vector()), msg="check pure state tensor product")
        del sv1
        del sv2
        del sv3

    def test_tensor_product_dm(self):
        num_qubit = 4
        dm1 = qulacs.DensityMatrix(num_qubit)
        dm2 = qulacs.DensityMatrix(num_qubit)
        dm1.set_Haar_random_state(seed=0)
        dm2.set_Haar_random_state(seed=1)
        dm3 = qulacs.state.tensor_product(dm1, dm2)
        dm3_test = np.kron(dm1.get_matrix(), dm2.get_matrix())
        self.assertTrue(np.allclose(dm3_test, dm3.get_matrix()), msg="check density matrix tensor product")
        del dm1
        del dm2
        del dm3

    def test_permutate_qubit_sv(self):
        num_qubit = 8
        sv = qulacs.StateVector(num_qubit)
        sv.set_Haar_random_state(seed=0)
        order = np.arange(num_qubit)
        np.random.shuffle(order)

        arr = []
        for ind in range(2**num_qubit):
            s = format(ind, "0{}b".format(num_qubit))
            s = np.array(list(s[::-1]))
            v = np.array(["*"]*num_qubit)
            for ind in range(len(s)):
                v[order[ind]] = s[ind]
            s = ("".join(v))[::-1]
            arr.append(int(s, 2))

        sv_perm = qulacs.state.permutate_qubit(sv, order)
        self.assertTrue(np.allclose(sv.get_vector()[arr], sv_perm.get_vector()), msg="check pure state permutation")
        del sv_perm
        del sv

    def test_permutate_qubit_dm(self):
        num_qubit = 3
        dm = qulacs.DensityMatrix(num_qubit)
        dm.set_Haar_random_state(seed=0)
        order = np.arange(num_qubit)
        np.random.shuffle(order)

        arr = []
        for ind in range(2**num_qubit):
            s = format(ind, "0{}b".format(num_qubit))
            s = np.array(list(s[::-1]))
            v = np.array(["*"]*num_qubit)
            for ind in range(len(s)):
                v[order[ind]] = s[ind]
            s = ("".join(v))[::-1]
            arr.append(int(s, 2))

        dm_perm = qulacs.state.permutate_qubit(dm, order)
        dm_perm_test = dm.get_matrix()
        dm_perm_test = dm_perm_test[arr, :]
        dm_perm_test = dm_perm_test[:, arr]
        self.assertTrue(np.allclose(dm_perm_test, dm_perm.get_matrix()), msg="check density matrix permutation")
        del dm_perm
        del dm

    def test_partial_trace_dm(self):
        num_qubit = 5
        num_traceout = 2
        dm = qulacs.DensityMatrix(num_qubit)
        dm.set_Haar_random_state(seed=0)
        mat = dm.get_matrix()

        target = np.arange(num_qubit)
        np.random.shuffle(target)
        target = target[:num_traceout]
        target_cor = [num_qubit-1-i for i in target]
        target_cor.sort()

        dmt = mat.reshape([2,2]*num_qubit)
        for cnt,val in enumerate(target_cor):
            ofs = num_qubit - cnt
            dmt = np.trace(dmt, axis1=val-cnt, axis2=ofs+val-cnt)
        dmt = dmt.reshape([2**(num_qubit-num_traceout),2**(num_qubit-num_traceout)])
        
        pdm = qulacs.state.partial_trace(dm, target)
        self.assertTrue(np.allclose(pdm.get_matrix(), dmt), msg="check density matrix partial trace")
        del dm,pdm

    def test_partial_trace_sv(self):
        num_qubit = 6
        num_traceout = 4
        sv = qulacs.StateVector(num_qubit)
        sv.set_Haar_random_state(seed=0)
        svv = np.atleast_2d(sv.get_vector()).T
        mat = np.dot(svv, svv.T.conj())

        target = np.arange(num_qubit)
        np.random.shuffle(target)
        target = target[:num_traceout]
        target_cor = [num_qubit-1-i for i in target]
        target_cor.sort()

        dmt = mat.reshape([2,2]*num_qubit)
        for cnt,val in enumerate(target_cor):
            ofs = num_qubit - cnt
            dmt = np.trace(dmt, axis1=val-cnt, axis2=ofs+val-cnt)
        dmt = dmt.reshape([2**(num_qubit-num_traceout),2**(num_qubit-num_traceout)])
        
        pdm = qulacs.state.partial_trace(sv, target)
        self.assertTrue(np.allclose(pdm.get_matrix(), dmt), msg="check pure state partial trace")

if __name__ == "__main__":
    unittest.main()