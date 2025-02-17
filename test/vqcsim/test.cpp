#include <gtest/gtest.h>

#include <cppsim/exception.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/state_dm.hpp>
#include <vqcsim/GradCalculator.hpp>
#include <vqcsim/causalcone_simulator.hpp>
#include <vqcsim/parametric_circuit_builder.hpp>
#include <vqcsim/parametric_gate_factory.hpp>
#include <vqcsim/problem.hpp>
#include <vqcsim/solver.hpp>

TEST(ParametricCircuit, GateApply) {
    const UINT n = 3;
    const UINT depth = 10;
    ParametricQuantumCircuit* circuit = new ParametricQuantumCircuit(n);
    Random random;
    for (UINT d = 0; d < depth; ++d) {
        for (UINT i = 0; i < n; ++i) {
            circuit->add_parametric_RX_gate(i, random.uniform());
            circuit->add_parametric_RY_gate(i, random.uniform());
            circuit->add_parametric_RZ_gate(i, random.uniform());
        }
        for (UINT i = d % 2; i + 1 < n; i += 2) {
            circuit->add_parametric_multi_Pauli_rotation_gate(
                {i, i + 1}, {3, 3}, random.uniform());
        }
    }

    UINT param_count = circuit->get_parameter_count();
    for (UINT p = 0; p < param_count; ++p) {
        double current_angle = circuit->get_parameter(p);
        circuit->set_parameter(p, current_angle + random.uniform());
    }

    QuantumState state(n);
    circuit->update_quantum_state(&state);
    // std::cout << state << std::endl;
    // std::cout << circuit << std::endl;
    delete circuit;
}

TEST(ParametricCircuit, GateApplyDM) {
    const UINT n = 3;
    const UINT depth = 10;
    ParametricQuantumCircuit* circuit = new ParametricQuantumCircuit(n);
    Random random;
    for (UINT d = 0; d < depth; ++d) {
        for (UINT i = 0; i < n; ++i) {
            circuit->add_parametric_RX_gate(i, random.uniform());
            circuit->add_parametric_RY_gate(i, random.uniform());
            circuit->add_parametric_RZ_gate(i, random.uniform());
        }
        for (UINT i = d % 2; i + 1 < n; i += 2) {
            circuit->add_parametric_multi_Pauli_rotation_gate(
                {i, i + 1}, {3, 3}, random.uniform());
        }
    }

    UINT param_count = circuit->get_parameter_count();
    for (UINT p = 0; p < param_count; ++p) {
        double current_angle = circuit->get_parameter(p);
        circuit->set_parameter(p, current_angle + random.uniform());
    }

    DensityMatrix state(n);
    circuit->update_quantum_state(&state);
    // std::cout << state << std::endl;
    // std::cout << circuit << std::endl;
    delete circuit;
}

class MyRandomCircuit : public ParametricCircuitBuilder {
    ParametricQuantumCircuit* create_circuit(
        UINT output_dim, UINT param_count) const override {
        ParametricQuantumCircuit* circuit =
            new ParametricQuantumCircuit(output_dim);
        UINT depth = param_count / output_dim;
        if (param_count % output_dim > 0) depth++;
        UINT param_index = 0;
        for (UINT d = 0; d < depth; ++d) {
            for (UINT i = 0; i < output_dim; ++i) {
                if (param_index < param_count) {
                    circuit->add_parametric_gate(gate::ParametricRX(i, 0.));
                    param_index++;
                } else {
                    circuit->add_gate(gate::RX(i, 0.0));
                }
            }
            for (UINT i = depth % 2; i + 1 < output_dim; ++i) {
                circuit->add_gate(gate::CNOT(0, 1));
            }
        }
        return circuit;
    }
};

TEST(EnergyMinimization, SingleQubitClassical) {
    const UINT n = 1;

    // define quantum circuit as prediction model
    std::function<ParametricQuantumCircuit*(UINT, UINT)> func =
        [](unsigned int qubit_count,
            unsigned int param_count) -> ParametricQuantumCircuit* {
        ParametricQuantumCircuit* circuit =
            new ParametricQuantumCircuit(qubit_count);
        for (unsigned int i = 0; i < qubit_count; ++i) {
            circuit->add_parametric_gate(gate::ParametricRX(i));
        }
        return circuit;
    };

    Observable* observable = new Observable(n);
    observable->add_operator(1.0, "Z 0");

    EnergyMinimizationProblem* emp = new EnergyMinimizationProblem(observable);

    QuantumCircuitEnergyMinimizationSolver qcems(&func, 0);
    qcems.solve(emp, 1000, "GD");
    double qc_loss = qcems.get_loss();

    DiagonalizationEnergyMinimizationSolver dems;
    dems.solve(emp);
    double diag_loss = dems.get_loss();

    EXPECT_NEAR(qc_loss, diag_loss, 1e-2);
}

TEST(EnergyMinimization, SingleQubitComplex) {
    const UINT n = 1;

    // define quantum circuit as prediction model
    std::function<ParametricQuantumCircuit*(UINT, UINT)> func =
        [](unsigned int qubit_count,
            unsigned int param_count) -> ParametricQuantumCircuit* {
        ParametricQuantumCircuit* circuit =
            new ParametricQuantumCircuit(qubit_count);
        for (unsigned int i = 0; i < qubit_count; ++i) {
            circuit->add_parametric_gate(gate::ParametricRX(i));
            circuit->add_parametric_gate(gate::ParametricRY(i));
            circuit->add_parametric_gate(gate::ParametricRX(i));
        }
        return circuit;
    };

    Observable* observable = new Observable(n);
    observable->add_operator(1.0, "Z 0");
    observable->add_operator(1.0, "X 0");
    observable->add_operator(1.0, "Y 0");

    EnergyMinimizationProblem* emp = new EnergyMinimizationProblem(observable);

    QuantumCircuitEnergyMinimizationSolver qcems(&func, 0);
    qcems.solve(emp, 1000, "GD");
    double qc_loss = qcems.get_loss();

    DiagonalizationEnergyMinimizationSolver dems;
    dems.solve(emp);
    double diag_loss = dems.get_loss();

    EXPECT_NEAR(qc_loss, diag_loss, 1e-2);
}

TEST(EnergyMinimization, MultiQubit) {
    const UINT n = 2;

    // define quantum circuit as prediction model
    std::function<ParametricQuantumCircuit*(UINT, UINT)> func =
        [](unsigned int qubit_count,
            unsigned int param_count) -> ParametricQuantumCircuit* {
        ParametricQuantumCircuit* circuit =
            new ParametricQuantumCircuit(qubit_count);
        for (unsigned int i = 0; i < qubit_count; ++i) {
            circuit->add_parametric_gate(gate::ParametricRX(i));
            circuit->add_parametric_gate(gate::ParametricRY(i));
            circuit->add_parametric_gate(gate::ParametricRX(i));
        }
        for (unsigned int i = 0; i + 1 < qubit_count; i += 2) {
            circuit->add_CNOT_gate(i, i + 1);
        }
        for (unsigned int i = 0; i < qubit_count; ++i) {
            circuit->add_parametric_gate(gate::ParametricRX(i));
            circuit->add_parametric_gate(gate::ParametricRY(i));
            circuit->add_parametric_gate(gate::ParametricRX(i));
        }
        return circuit;
    };

    Observable* observable = new Observable(n);
    observable->add_operator(1.0, "Z 0 X 1");
    observable->add_operator(-1.0, "Z 0 Y 1");
    observable->add_operator(0.2, "Y 0 Y 1");

    EnergyMinimizationProblem* emp = new EnergyMinimizationProblem(observable);

    QuantumCircuitEnergyMinimizationSolver qcems(&func, 0);
    qcems.solve(emp, 1000, "GD");
    double qc_loss = qcems.get_loss();

    DiagonalizationEnergyMinimizationSolver dems;
    dems.solve(emp);
    double diag_loss = dems.get_loss();
    // std::cout << qc_loss << " " << diag_loss << std::endl;
    ASSERT_GT(qc_loss, diag_loss);
    EXPECT_NEAR(qc_loss, diag_loss, 1e-1);
}

TEST(ParametricGate, DuplicateIndex) {
    auto gate1 = gate::ParametricPauliRotation(
        {0, 1, 2, 3, 4, 5, 6}, {0, 0, 0, 0, 0, 0, 0}, 0.0);
    EXPECT_TRUE(gate1 != NULL);
    delete gate1;
    auto gate2 = gate::ParametricPauliRotation(
        {2, 1, 0, 3, 7, 9, 4}, {0, 0, 0, 0, 0, 0, 0}, 0.0);
    EXPECT_TRUE(gate2 != NULL);
    delete gate2;
    ASSERT_THROW(
        {
            auto gate3 = gate::ParametricPauliRotation(
                {0, 1, 3, 1, 5, 6, 2}, {0, 0, 0, 0, 0, 0, 0}, 0.0);
        },
        DuplicatedQubitIndexException);
    ASSERT_THROW(
        {
            auto gate4 = gate::ParametricPauliRotation(
                {0, 3, 5, 2, 5, 6, 2}, {0, 0, 0, 0, 0, 0, 0}, 0.0);
        },
        DuplicatedQubitIndexException);
}

TEST(GradCalculator, BasicCheck) {
    Random rnd;
    unsigned int n = 5;
    Observable observable(n);
    std::string Pauli_string = "";
    for (int i = 0; i < n; ++i) {
        double coef = rnd.uniform();
        std::string Pauli_string = "Z ";
        Pauli_string += std::to_string(i);
        observable.add_operator(coef, Pauli_string.c_str());
    }

    ParametricQuantumCircuit circuit(n);
    int cnter_parametric_gate = 0;
    for (int depth = 0; depth < 2; ++depth) {
        for (int i = 0; i < n; ++i) {
            circuit.add_parametric_RX_gate(i, 0);
            circuit.add_parametric_RZ_gate(i, 0);
            cnter_parametric_gate += 2;
        }

        for (int i = 0; i + 1 < n; i += 2) {
            circuit.add_CNOT_gate(i, i + 1);
        }

        for (int i = 1; i + 1 < n; i += 2) {
            circuit.add_CNOT_gate(i, i + 1);
        }
    }

    // Calculate using GradCalculator
    GradCalculator hoge;
    std::vector<double> theta;
    for (int i = 0; i < cnter_parametric_gate; ++i) {
        theta.push_back(rnd.uniform() * 5.0);
    }
    auto GradCalculator_ans_theta_specified =
        hoge.calculate_grad(circuit, observable, theta);

    for (UINT i = 0; i < cnter_parametric_gate; ++i) {
        ASSERT_EQ(circuit.get_parameter(i), 0);
        circuit.set_parameter(i, theta[i]);
    }
    auto GradCalculator_ans_without_theta =
        hoge.calculate_grad(circuit, observable);

    // Calculate using normal Greedy.
    std::vector<std::complex<double>> Greedy_ans;
    {
        for (int i = 0; i < circuit.get_parameter_count(); ++i) {
            std::complex<double> y, z;
            {
                for (int q = 0; q < circuit.get_parameter_count(); ++q) {
                    float diff = 0;
                    if (i == q) {
                        diff = 0.001;
                    }
                    circuit.set_parameter(q, theta[q] + diff);
                }
                CausalConeSimulator cone(circuit, observable);
                y = cone.get_expectation_value();
            }
            {
                for (int q = 0; q < circuit.get_parameter_count(); ++q) {
                    float diff = 0;
                    if (i == q) {
                        diff = 0.001;
                    }
                    circuit.set_parameter(q, theta[q] - diff);
                }
                CausalConeSimulator cone(circuit, observable);
                z = cone.get_expectation_value();
            }
            Greedy_ans.push_back((y - z) / 0.002);
        }
    }
    for (int i = 0; i < GradCalculator_ans_without_theta.size(); ++i) {
        ASSERT_LT(abs(GradCalculator_ans_theta_specified[i] - Greedy_ans[i]),
            1e-6);  // Difference should be lower than 1e-7
        ASSERT_LT(abs(GradCalculator_ans_without_theta[i] - Greedy_ans[i]),
            1e-6);  // Difference should be lower than 1e-7
    }
}
