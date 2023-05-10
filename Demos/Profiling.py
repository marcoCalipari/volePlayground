import random
import time
import timeit
import cProfile
from tqdm import tqdm
from Modules.Functions.OT import *
from Modules.Utils.paillier import *
from Modules.Utils.classes import *
from Modules.Functions.VOLE_Paillier import *


# We first create the setup for both functions
def setup():
    q = 2**7
    sender = OLE_Sender(random.randint(1, q))
    receiver = OLE_Receiver(random.randint(1, q), random.randint(1, q))
    return sender, receiver, q


# CASE 1: SINGLE OPERATION
def single_operation_VOLE():
    sender, receiver, q = setup()
    return compute_vole_HE(sender, receiver, q)


def single_operation_OT():
    sender, receiver, q = setup()
    if sender is None or receiver is None or q is None:
        print(f"{sender} , {receiver} , {q}")
    return VOLE(sender, receiver, q, False)

iterations = 50


print("Profiling Single Operation VOLE OT...")
profiler2 = cProfile.Profile()
failed_attempts = 0
for i in range(iterations):
    profiler2.enable()
    result = single_operation_OT() 
    profiler2.disable()
    
    if result is None:
        failed_attempts += 1
    
profiler2.print_stats()
total_attempts = iterations
success_attempts = total_attempts - failed_attempts
failed_ratio = failed_attempts / total_attempts
print(f"Failed attempts: {failed_attempts}")
print(f"Failed attempts ratio: {failed_ratio:.2f}")



print("Profiling Single Operation VOLE...")
profiler1 = cProfile.Profile()
for i in range(iterations):
    profiler1.enable()
    single_operation_VOLE()
    profiler1.disable()
profiler1.print_stats()
