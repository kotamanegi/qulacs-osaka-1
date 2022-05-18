from code import interact
from typing import List, Union

from qulacs import QuantumGateBase, QuantumState
from qulacs.AdaptiveQuantumState import AdaptiveQuantumState
from qulacs.gate import SWAP


class AdaptiveQuantumCircuit:
  
  gates: List[Union[QuantumGateBase, int]]

  def __init__(self):
    self.gates = []
  
  def add_gate(self, gate: QuantumGateBase):
    self.gates.append(gate)

  def remove_qubit(self, qu:int):
    self.gates.append(-qu - 1)

  def add_qubit(self, qu:int):
    self.gates.append(qu)
  
  def get_quantumstate(self):
    state = AdaptiveQuantumState()
    for gate in self.gates:
      if type(gate) is int:
        if gate >= 0:
          state.add_qubit(gate)
        else:
          state.delete_qubit(-gate - 1)
      else:
        state.update_quantum_state_from_gate(gate)
    return state.internal_state
