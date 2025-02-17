from typing import Callable, List

from typing import overload
import numpy
import qulacs_core
import scipy.sparse

@overload
def Adaptive(gate: qulacs_core.QuantumGateBase, condition: Callable[[List[int]],bool]) -> qulacs_core.QuantumGateBase: ...
@overload
def Adaptive(gate: qulacs_core.QuantumGateBase, condition: Callable[[List[int],int],bool], id: int) -> qulacs_core.QuantumGateBase: ...
def AmplitudeDampingNoise(index: int, prob: float) -> qulacs_core.QuantumGateBase: ...
def BitFlipNoise(index: int, prob: float) -> qulacs_core.QuantumGateBase: ...
def CNOT(control: int, target: int) -> qulacs_core.QuantumGateBase: ...
def CP(kraus_list: List[qulacs_core.QuantumGateBase], state_normalize: bool, probability_normalize: bool, assign_zero_if_not_matched: bool) -> qulacs_core.QuantumGateBase: ...
def CPTP(kraus_list: List[qulacs_core.QuantumGateBase]) -> qulacs_core.QuantumGateBase: ...
def CZ(control: int, target: int) -> qulacs_core.QuantumGateBase: ...
@overload
def DenseMatrix(index: int, matrix: numpy.ndarray[numpy.complex128[m,n]]) -> qulacs_core.QuantumGateMatrix: ...
@overload
def DenseMatrix(index_list: List[int], matrix: numpy.ndarray[numpy.complex128[m,n]]) -> qulacs_core.QuantumGateMatrix: ...
def DephasingNoise(index: int, prob: float) -> qulacs_core.QuantumGateBase: ...
def DepolarizingNoise(index: int, prob: float) -> qulacs_core.QuantumGateBase: ...
def DiagonalMatrix(index_list: List[int], diagonal_element: numpy.ndarray[numpy.complex128[m,1]]) -> qulacs_core.QuantumGateBase: ...
def FREDKIN(control: int, target1: int, target2: int) -> qulacs_core.QuantumGateMatrix: ...
def H(index: int) -> qulacs_core.QuantumGateBase: ...
def Identity(index: int) -> qulacs_core.QuantumGateBase: ...
def IndependentXZNoise(index: int, prob: float) -> qulacs_core.QuantumGateBase: ...
def Instrument(kraus_list: List[qulacs_core.QuantumGateBase], register: int) -> qulacs_core.QuantumGateBase: ...
def Measurement(index: int, register: int) -> qulacs_core.QuantumGateBase: ...
def NoisyEvolution(hamiltonian: qulacs_core.Observable, c_ops: List[qulacs_core.GeneralQuantumOperator], time: float, dt: float) -> qulacs_core.QuantumGateBase: ...
def P0(index: int) -> qulacs_core.QuantumGateBase: ...
def P1(index: int) -> qulacs_core.QuantumGateBase: ...
def ParametricPauliRotation(index_list: List[int], pauli_ids: List[int], angle: float) -> qulacs_core.QuantumGate_SingleParameter: ...
def ParametricRX(index: int, angle: float) -> qulacs_core.QuantumGate_SingleParameter: ...
def ParametricRY(index: int, angle: float) -> qulacs_core.QuantumGate_SingleParameter: ...
def ParametricRZ(index: int, angle: float) -> qulacs_core.QuantumGate_SingleParameter: ...
def Pauli(index_list: List[int], pauli_ids: List[int]) -> qulacs_core.QuantumGateBase: ...
def PauliRotation(index_list: List[int], pauli_ids: List[int], angle: float) -> qulacs_core.QuantumGateBase: ...
def Probabilistic(prob_list: List[float], gate_list: List[qulacs_core.QuantumGateBase]) -> qulacs_core.QuantumGateBase: ...
def ProbabilisticInstrument(prob_list: List[float], gate_list: List[qulacs_core.QuantumGateBase], register: int) -> qulacs_core.QuantumGateBase: ...
def RX(index: int, angle: float) -> qulacs_core.QuantumGateBase: ...
def RY(index: int, angle: float) -> qulacs_core.QuantumGateBase: ...
def RZ(index: int, angle: float) -> qulacs_core.QuantumGateBase: ...
@overload
def RandomUnitary(index_list: List[int]) -> qulacs_core.QuantumGateMatrix: ...
@overload
def RandomUnitary(index_list: List[int], seed: int) -> qulacs_core.QuantumGateMatrix: ...
def ReversibleBoolean(index_list: List[int], func: Callable[[int,int],int]) -> qulacs_core.QuantumGateBase: ...
def S(index: int) -> qulacs_core.QuantumGateBase: ...
def SWAP(target1: int, target2: int) -> qulacs_core.QuantumGateBase: ...
def Sdag(index: int) -> qulacs_core.QuantumGateBase: ...
def SparseMatrix(index_list: List[int], matrix: scipy.sparse.csc_matrix[numpy.complex128]) -> qulacs_core.QuantumGateBase: ...
def StateReflection(state: qulacs_core.QuantumStateBase) -> qulacs_core.QuantumGateBase: ...
def T(index: int) -> qulacs_core.QuantumGateBase: ...
def TOFFOLI(control1: int, control2: int, target: int) -> qulacs_core.QuantumGateMatrix: ...
def Tdag(index: int) -> qulacs_core.QuantumGateBase: ...
def TwoQubitDepolarizingNoise(index1: int, index2: int, prob: float) -> qulacs_core.QuantumGateBase: ...
def U1(index: int, lambda: float) -> qulacs_core.QuantumGateBase: ...
def U2(index: int, phi: float, lambda: float) -> qulacs_core.QuantumGateBase: ...
def U3(index: int, theta: float, phi: float, lambda: float) -> qulacs_core.QuantumGateBase: ...
def X(index: int) -> qulacs_core.QuantumGateBase: ...
def Y(index: int) -> qulacs_core.QuantumGateBase: ...
def Z(index: int) -> qulacs_core.QuantumGateBase: ...
@overload
def add(gate1: qulacs_core.QuantumGateBase, gate2: qulacs_core.QuantumGateBase) -> qulacs_core.QuantumGateMatrix: ...
@overload
def add(gate_list: List[qulacs_core.QuantumGateBase]) -> qulacs_core.QuantumGateMatrix: ...
@overload
def merge(gate1: qulacs_core.QuantumGateBase, gate2: qulacs_core.QuantumGateBase) -> qulacs_core.QuantumGateMatrix: ...
@overload
def merge(gate_list: List[qulacs_core.QuantumGateBase]) -> qulacs_core.QuantumGateMatrix: ...
def sqrtX(index: int) -> qulacs_core.QuantumGateBase: ...
def sqrtXdag(index: int) -> qulacs_core.QuantumGateBase: ...
def sqrtY(index: int) -> qulacs_core.QuantumGateBase: ...
def sqrtYdag(index: int) -> qulacs_core.QuantumGateBase: ...
def to_matrix_gate(gate: qulacs_core.QuantumGateBase) -> qulacs_core.QuantumGateMatrix: ...
