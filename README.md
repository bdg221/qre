# A Survery of Quantum Resource Estimation Tools

Companion repository for the paper: A Survey of Quantum Resource Estimation Tools.

## Overview

The repository contains the code and results used in the paper, including:

### Information used for Figure 2 and Figure 3.
Azure_QRE_Shor.pdf - This file contains a PDF of the results of running Azure QRE on the ShorRE.qs file from the qsharp GitHub repository (https://github.com/microsoft/qsharp/blob/main/samples/estimation/ShorRE.qs). The results were generated using qubit_gate_ns_e3, qubit_gate_ns_e4, qubit_maj_ns_e4 + floquet_code, and qubit_maj_ns_e6 + floquet code. An error budget of 0.333 was assigned since the results of running Shor's algorithm can be verified easily.

### Information and code used for Figure 4 and 5.
BenchQ_Code_For_Figures.py is a modified version of ex_1_from_qasm.py from the examples directory in the BenchQ GitHub repository (https://github.com/zapatacomputing/benchq). This code uses a sample decoder file (BenchQ/sample_decoder_data.csv) and a QASM file for a sample circuit (QASM/example_circuit.qasm). Both of these files also came from the BenchQ GitHug repository (https://github.com/zapatacomputing/benchq/tree/main/examples/data). The code produced the results used in the figure 4 and 5 of the paper. The figure show partial results, but the complete results can be found in BnechQ_Figure4_5_Results.txt

### BenchQ Tests and Results
For the CNOT, single qubit rotation, and Toffoli tests, the code and results can be found in the BenchQ directory. The MODIFIED_FOR_TESTS_ex_1_from_qasm.py is modified code from ex_1_from_qasm.py found in the examples directory of the BenchQ GitHub repository (https://github.com/zapatacomputing/benchq). This code uses three QASM files found in the QASM directory, cnot.qasm, single_rotation.qasm, and toffoli.qasm. These tests use the get_fast_graph_estimate pipeline which does NOT transpile the circuit into Clifford+T in order to match the other tools. Also, it should be noted that the footprint estimator which is also used does not produce results for the CNOT test as it requires a T gate or Toffoli gate.

### Azure Quantum Resource Estimator Tests and Results
For the CNOT, single qubit rotation, and Toffoli tests, the code and results are found in a single Jupyter Notebook, AzureQRE_tests.ipynb. This notebook uses three QASM files found in the QASM directory, cnot.qasm, single_rotation.qasm, and toffoli.qasm. It should be noted that Azure QRE does not handle the CNOT example as a T gate or measurement is required.


## Requirements

Each tool has separate requirements.


## Azure Quantum Resource Estimator
https://learn.microsoft.com/en-us/azure/quantum/quickstart-microsoft-qiskit?tabs=tabid-ionq&pivots=platform-local#prerequisites

## BenchQ
https://github.com/zapatacomputing/benchq/tree/main
