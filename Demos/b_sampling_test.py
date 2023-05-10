"""
This script serves the purpose of testing the b-sampling algorithm in order to find on average how much time is required to find a b value
that satisfies the necessary condition for VOLE, as well as the successfull / failed ratio.

"""
import random
import time

from Modules.Utils.helpers import mock_decomposition


# We create a list of random elements:

b_list_small_numbers = []
b_list_big_numbers = []
cumulative_time = 0
failed  = 0
limit = 10000
vector_size = 8

iterations = random.randint(50 , 100)

for i in range(iterations):
    b_list_small_numbers.append(random.randint(1 , 50))
    b_list_big_numbers.append(random.randint(100 , 1000))
    
    

for elem in b_list_small_numbers:
    start_time = time.monotonic()
    result = mock_decomposition(elem , 2**7 , vector_size , limit)
    stop_time = time.monotonic()
    
    if result == None:
        failed += 1
    
    cumulative_time += (stop_time - start_time)
    
print(f"Average time for small numbers: {cumulative_time / iterations} , failed: {failed} / {iterations} with a number of max iterations: {limit} and vector size of: {vector_size}")

cumulative_time = 0
failed = 0
for elem in b_list_big_numbers:
    start_time = time.monotonic()
    result = mock_decomposition(elem , 2**7 , vector_size , limit)
    stop_time = time.monotonic()
    
    if result == None:
        failed += 1
    
    cumulative_time += (stop_time - start_time)
    
print(f"Average time for big numbers: {cumulative_time / iterations} , failed: {failed} / {iterations} , with a number of iterations: {limit} and vector size of: {vector_size}")


cumulative_time = 0
failed = 0
limit = 100000
for elem in b_list_big_numbers:
    start_time = time.monotonic()
    result = mock_decomposition(elem , 2**7 , vector_size , limit)
    stop_time = time.monotonic()
    
    if result == None:
        failed += 1
    
    cumulative_time += (stop_time - start_time)
    
print(f"Average time for big numbers: {cumulative_time / iterations} , failed: {failed} / {iterations} , with a number of iterations: {limit} and vector size of: {vector_size}")


cumulative_time = 0
failed = 0
limit = 100000
vector_size = 16
for elem in b_list_big_numbers:
    start_time = time.monotonic()
    result = mock_decomposition(elem , 2**7 , vector_size , limit)
    stop_time = time.monotonic()
    
    if result == None:
        failed += 1
    
    cumulative_time += (stop_time - start_time)
    
print(f"Average time for big numbers: {cumulative_time / iterations} , failed: {failed} / {iterations} , with a number of iterations: {limit} and vector size of: {vector_size}")
