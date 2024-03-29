################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Basic example of how to perform resource estimation of a circuit from a QASM file.
WARNING: This example requires the pyscf extra. run `pip install benchq[pyscf]`
to install the extra.
"""

import os
from pathlib import Path


from orquestra.integrations.qiskit.conversions import import_from_qiskit
from qiskit.circuit import QuantumCircuit

from pprint import pprint

from benchq.decoder_modeling import DecoderModel

from benchq.algorithms.data_structures import AlgorithmImplementation, ErrorBudget
from benchq.problem_embeddings import get_program_from_circuit
from benchq.quantum_hardware_modeling import BASIC_ION_TRAP_ARCHITECTURE_MODEL, BASIC_SC_ARCHITECTURE_MODEL, DETAILED_ION_TRAP_ARCHITECTURE_MODEL, DetailedIonTrapModel
from benchq.resource_estimators.graph_estimators import (
    GraphResourceEstimator,
    create_big_graph_from_subcircuits,
    get_custom_resource_estimation,
    synthesize_clifford_t,
    transpile_to_native_gates,
)

from benchq.resource_estimators.default_estimators import (
    get_precise_graph_estimate,
    get_footprint_estimate,
    get_fast_graph_estimate
)


def main(file_name, flag = True):
    # Uncomment to see extra debug output
    # logging.getLogger().setLevel(logging.INFO)

    # We can load a circuit from a QASM file using qiskit
    qiskit_circuit = QuantumCircuit.from_qasm_file(file_name)

    # Error budget is used to define what should be the failure rate of running
    # the whole calculation. It also allows to set relative weights for different
    # parts of the calculation, such as gate synthesis or circuit generation.
    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-3)

    # algorithm implementation encapsulates the how the algorithm is implemented
    # including the program, the number of times the program must be repeated,
    # and the error budget which will be used in the circuit.
    algorithm_implementation = AlgorithmImplementation.from_circuit(
        qiskit_circuit, error_budget, 1
    )

    # Architecture model is used to define the hardware model.
    
    architecture_model = BASIC_ION_TRAP_ARCHITECTURE_MODEL

    # Here we run the resource estimation pipeline.
    # In this case before performing estimation we use the following transformers:
    # 1. Simplify rotations – it is a simple transpilation that removes redundant
    # rotations from the circuit, such as RZ(0) or RZ(2pi) and replaces RX and RY
    # gates with RZs
    # 2. Gate synthesis – replaces all RZ gates with Clifford+T gates
    # 3. Create big graph from subcircuits – this transformer is used to create
    # a graph from subcircuits. It is needed to perform resource estimation using
    # the graph resource estimator. In this case we use delayed gate synthesis, as
    # we have already performed gate synthesis in the previous step.

    if flag == True:        
        print("STARTING FOOTPRINT RESOURCE ESTIMATION WITHOUT A DECODER MODEL OR DETAILED HARDWARE MODEL")
        footprint_resource_estimates = get_footprint_estimate(algorithm_implementation=algorithm_implementation, hardware_model=architecture_model)
        pprint(footprint_resource_estimates)


    print("\n\nSTARTING RESOURCE ESTIMATION WITHOUT A DECODER MODEL OR DETAILED HARDWARE MODEL")
    gsc_resource_estimates = get_custom_resource_estimation(
        algorithm_implementation,
        estimator=GraphResourceEstimator(architecture_model),
        transformers=[
            transpile_to_native_gates,
            #synthesize_clifford_t(error_budget),
            create_big_graph_from_subcircuits(),
        ],
    )
    pprint(gsc_resource_estimates)

    print("\n\nSTARTING DETAILED RESOURCE ESTIMATION WITH A DECODER MODEL AND DETAILED HARDWARE MODEL:")

    # Load some dummy decoder data for now. Replace with your own decoder data.
    decoder_file_path =  str(os.path.dirname(__file__)) + "/sample_decoder_data.csv"
    decoder_model = DecoderModel.from_csv(decoder_file_path) 

    architecture_model2 = DETAILED_ION_TRAP_ARCHITECTURE_MODEL

    gsc_resource_estimates_pipeline = get_fast_graph_estimate(algorithm_implementation=algorithm_implementation, hardware_model=architecture_model2, decoder_model=decoder_model)
    pprint(gsc_resource_estimates_pipeline)

if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    print("\n######################## SINGLE ROTATION EXAMPLE ########################")
    main(current_directory + "/../QASM/single_rotation.qasm")
    print("\n######################## CNOT EXAMPLE ########################")
    main(current_directory + "/../QASM/cnot.qasm", flag=False)
    print("\n######################## TOFFOLI EXAMPLE ########################")
    main(current_directory + "/../QASM/toffoli.qasm")
