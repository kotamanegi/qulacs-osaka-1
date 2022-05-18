from code import interact
from typing import Dict

from qulacs import QuantumGateBase, QuantumState
from qulacs.gate import SWAP


class AdaptiveQuantumState:

  qubitname_to_qubititr_mapping: Dict[int,int] 
  qubititr_to_qubitname_mapping: Dict[int,int] 
  internal_state: QuantumState
  
  def __init__(self):
    self.qubitname_to_qubititr_mapping = dict()
    self.qubititr_to_qubitname_mapping = dict()
    self.internal_state = QuantumState(0)
  
  def add_qubit(self, qubit_name: int):
    if qubit_name in  self.qubitname_to_qubititr_mapping:
      raise RuntimeError("AdaptiveQuantumState already have qubit named with " + str(qubit_name))
    next_qubit_itr = self.internal_state.get_qubit_count()
    self.qubitname_to_qubititr_mapping[qubit_name] = next_qubit_itr
    self.qubititr_to_qubitname_mapping[next_qubit_itr] = qubit_name
    self.internal_state.push_qubit()


  def swap_qubit(self, qubit_name1:int, qubit_name2:int):
    qubit_itr1 = self.qubitname_to_qubititr_mapping[qubit_name1]
    qubit_itr2 = self.qubitname_to_qubititr_mapping[qubit_name2]
    if qubit_itr1 != qubit_itr2:
      gate = SWAP(qubit_itr1, qubit_itr2)
      gate.update_quantum_state(self.internal_state)
      qubit_itr1,qubit_itr2 = qubit_itr2,qubit_itr1
      qubit_name1,qubit_name2 = qubit_name1,qubit_name2
      self.qubititr_to_qubitname_mapping[qubit_itr1] = qubit_name1
      self.qubititr_to_qubitname_mapping[qubit_itr2] = qubit_name2
      self.qubitname_to_qubititr_mapping[qubit_name1] = qubit_itr1
      self.qubitname_to_qubititr_mapping[qubit_name2] = qubit_itr2
    
  def delete_qubit(self, qubit_name: int):
    if qubit_name not in self.qubitname_to_qubititr_mapping:
      raise RuntimeError("AdaptiveQuantumState don't have qubit named with " + str(qubit_name))
    
    elimination_qubit_itr = self.internal_state.get_qubit_count() - 1
    elimination_qubit_name =  self.qubititr_to_qubitname_mapping[elimination_qubit_itr]
    target_qubit_name =  qubit_name

    self.swap_qubit(target_qubit_name,elimination_qubit_name)
    elimination_qubit_name = self.qubititr_to_qubitname_mapping[elimination_qubit_itr]

    self.qubititr_to_qubitname_mapping.pop(elimination_qubit_itr)
    self.qubitname_to_qubititr_mapping.pop(elimination_qubit_name)
    self.internal_state = QuantumState(elimination_qubit_itr)
