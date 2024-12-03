from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_serverless import get_arguments, save_result, distribute_task, get
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit
from qiskit_ibm_catalog import QiskitServerless, QiskitFunction
from qiskit_ibm_catalog import QiskitFunctionsCatalog
from qiskit_ibm_catalog import QiskitServerless




'''distibute_task is a decorator,
wraps around this function and modifies its behavior, before and after it runs'''
@distribute_task(target={"cpu": 1})
def transpile_remote(circuit, optimization_level, backend_name):
    
    
    backend = service.backend(backend_name)
    print(backend)
    pass_manager = generate_preset_pass_manager(
        optimization_level=optimization_level,
        backend=backend
    )
    return pass_manager.run(circuit)

 
# Get program arguments
arguments = get_arguments()
circuits = arguments.get("circuits")
backend_name = arguments.get("backend_name")
optimization_level = arguments.get("optimization_level")

service = QiskitRuntimeService(channel="ibm_quantum")
backend = "ibm_brisbane" #can be replaced with service.least_busy(operational=True, simulator=False)


#Circuit to be transpiled
circuit_1 = QuantumCircuit(2)
circuit_1.h(0)  
circuit_1.cx(0, 1)  

#logic for 3 parallel circuits with different optimizations
opt_lev=[0,1,2]

transpile_worker_references = [
        transpile_remote(circuit_1, level, backend)
        for level in opt_lev
    ]
result = get(transpile_worker_references)
save_result(result)
for i in range(3):
    print(result[i].depth())





#For uploading onto Serverless
catalog = QiskitFunctionsCatalog()
print(catalog)
'''Gives error-Needs to be resolved-API authentication issue, works for QiskitRuntimeService, not for this
##Tried passing instance and channel values into .save_Account()which gets saved, 
#but gives an error when catalog() is called, 
#and therefore gives an error while instantiating serverless as well'''
#   Doesn't work, API not being authenticated
serverless = QiskitServerless()
print(serverless.list())


transpile_remote_demo = QiskitFunction(
    title="transpile_remote_serverless",
    entrypoint="transpile_remote.py",
    working_dir="./source_files/",
)
serverless.upload(transpile_remote_demo)
