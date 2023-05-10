import random
import timeit
import time
from tqdm import tqdm
from colorama import Fore, Style
from Modules.Functions.OT import *
from Modules.Utils.paillier import *
from Modules.Utils.classes import *
from Modules.Functions.VOLE_Paillier import *
import numpy as np

import matplotlib.pyplot as plt

# We first create the setup for both functions


def setup():
    q = 2**7
    sender = OLE_Sender(random.randint(1, q))
    receiver = OLE_Receiver(random.randint(1, q), random.randint(1, q))
    return sender, receiver, q

def setup_simplest_OT():
    q = 2**7
    sender = Sender(random.randint(1, q) , random.randint(1, q))
    receiver = Receiver(random.randint(0, 1))
    return sender, receiver

def setup_vectors():
    q = 2**7
    x_vector = [random.randint(1, q) for _ in range(100)]
    a_vector = [random.randint(1, q) for _ in range(100)]
    b_vector = [random.randint(1, q) for _ in range(100)]
    
    return x_vector, a_vector, b_vector, q
    


# CASE 1: SINGLE OPERATION


def single_operation_VOLE():
    sender, receiver, q = setup()
    return compute_vole_HE(sender, receiver, q)


def single_operation_OT():
    sender, receiver, q = setup()
    return VOLE(sender, receiver, q, False)

def simplest_OT_benchmark():
    sender, receiver= setup_simplest_OT()
    return SimplestOT_1OutOf2(sender, receiver, False, True)


def VOLE_OT_with_vectors():
    x , a , b, q = setup_vectors()
    cum_time = 0
    failed_iterations = 0
    for i in range(len(x)):
        sender = OLE_Sender(x[i])
        receiver = OLE_Receiver(a[i], b[i])
        start_time = time.monotonic()
        result = VOLE(sender, receiver, q, False)
        if result is None:
            failed_iterations +=1
            pass
        else:
            stop_time = time.monotonic()
            cum_time += (stop_time - start_time)
    return cum_time / len(x) , failed_iterations  
        
def VOLE_Paillier_with_vectors():
    x,a,b,q = setup_vectors()
    cum_time = 0
    for i in range(len(x)):
        
        sender = OLE_Sender(x[i])
        receiver = OLE_Receiver(a[i], b[i])
        start_time = time.monotonic()
        compute_vole_HE(sender, receiver, q)
        stop_time = time.monotonic()
        cum_time += (stop_time - start_time)
        
    return cum_time / len(x)


# Define color for progress bars
green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
blue = Fore.BLUE
reset = Style.RESET_ALL

iterations = 1000

bar_format_vole = (
    f"{green}Benchmarking VOLE{reset} "
    + "{bar}"
    + " {percentage:3.0f}% | "
    + "{n_fmt}/{total_fmt} [{elapsed}<{remaining}, "
    + "Paillier VOLE: {postfix}]"
)

bar_format_ot = (
    f"{yellow}Benchmarking OT{reset} "
    + "{bar}"
    + " {percentage:3.0f}% | "
    + "{n_fmt}/{total_fmt} [{elapsed}<{remaining}, "
    + "OT VOLE: {postfix}]"
)

bar_format_OT_BM = (
    f"{red}Benchmarking OT{reset} "
    + "{bar}"
    + " {percentage:3.0f}% | "
    + "{n_fmt}/{total_fmt} [{elapsed}<{remaining}, "
    + "Crypto time: {postfix}]"
)

bar_format_OT_BM = (
    f"{blue}Benchmarking OT{reset} "
    + "{bar}"
    + " {percentage:3.0f}% | "
    + "{n_fmt}/{total_fmt} [{elapsed}<{remaining}, "
    + "Crypto time Paillier: {postfix}]"
)


# Use color in progress bars

user = input("Press 0 if you want to compare VOLE\nPress 1 if you want to benchmark OT\nPress 2 if you wanna compare VOLE with vectors\n"
             "Press 3 if you wanna benchmark VOLE with Paillier crypto operation\n")

"""Comparison single operation"""
if user == "0":
    total_time_VOLE = 0

    with tqdm(total=iterations, bar_format=bar_format_vole) as pbar1:
        for i in range(iterations):
            
            start_time = time.monotonic()
            single_operation_VOLE()
            end_time = time.monotonic()
            total_time_VOLE += end_time - start_time
            pbar1.update(1)
            time.sleep(0.01)
    average_time_VOLE = total_time_VOLE / iterations


    # Run the OT operation and calculate the average time taken
    total_time_OT = 0
    iterations_reached_limit = 0
    iterations_failed = 0
    with tqdm(total=iterations, bar_format=bar_format_ot) as pbar2:
        
            for i in range(iterations):
                
                start_time = time.monotonic()
                try:
                    result = single_operation_OT()
                except TypeError:
                    #print("Impossible to decompose b_i")
                    iterations_failed += 1
                    pass
                end_time = time.monotonic()
                pbar2.update(1)
                time.sleep(0.01)
                if result is None:
                    iterations_reached_limit += 1
                else:
                    total_time_OT += end_time - start_time
        
            

    average_time_OT = total_time_OT / iterations

    print(
        f"------- VOLE BENCHMARKING -------\n"
        f"Paillier VOLE average time: {average_time_VOLE*100:.6f} seconds\n"
        f"OT VOLE average time: {average_time_OT*100:.6f} seconds\n"
        f"Iterations reached limit: {iterations_reached_limit}\n"
        f"Iterations failed: {iterations_failed}"
    )
    
# OT crypto time benchmarking       
elif user == "1":
    Benchmark_times = []
    results = []
    means_of_means = []
    cumulative_time = 0
    with tqdm(total=iterations*10, bar_format=bar_format_OT_BM) as pbar3:
        for _ in range(10):
            for i in range(iterations):
                result, benchmark_time = simplest_OT_benchmark()
                results.append(result)
                Benchmark_times.append(benchmark_time)
                cumulative_time += benchmark_time
                pbar3.update(1)
                time.sleep(0.01)

            mean = np.mean(Benchmark_times)
            means_of_means.append(mean)
        
    print(f"------- OT BENCHMARKING -------\n"
        f"OT crypto average time: {cumulative_time/iterations *100:.6f} seconds\n"
        f"Mean of means: {np.mean(means_of_means) * 100:.6f} seconds")


# Comparison with vectors
elif user == "2":
    
    tot_time_vector_vole = 0
    avg_per_number = []

    with tqdm(total=iterations, bar_format=bar_format_vole) as pbar1:
        for i in range(iterations):
            single_element_avg_time = VOLE_Paillier_with_vectors()
            tot_time_vector_vole += single_element_avg_time
            avg_per_number.append(single_element_avg_time)
            pbar1.update(1)
            time.sleep(0.01)

    average_time_VOLE = tot_time_vector_vole / iterations
    mean_of_means = sum(avg_per_number) / len(avg_per_number)

    # Run the OT operation and calculate the average time taken
    avg_per_number = []
    iterations_failed_per_number = []
    single_element_avg_time = 0
    total_time_OT = 0
    iterations_reached_limit = 0
    iterations_failed = 0

    with tqdm(total=iterations, bar_format=bar_format_ot) as pbar2:
        for i in range(iterations):
            single_element_avg_time, failed = VOLE_OT_with_vectors()
            total_time_OT += single_element_avg_time
            avg_per_number.append(single_element_avg_time)
            iterations_failed_per_number.append(failed)
            pbar2.update(1)
            time.sleep(0.01)

    average_time_OT = total_time_OT / iterations
    mean_of_means_OT_times = sum(avg_per_number) / len(avg_per_number)
    avg_iterations_failed = sum(iterations_failed_per_number) / len(iterations_failed_per_number)
    print(iterations_failed_per_number)

    print(
        f"------- VOLE BENCHMARKING -------\n"
        f"Paillier VOLE average time: {average_time_VOLE:.6f} seconds\n"
        f"OT VOLE average time: {average_time_OT:.6f} seconds\n"
        f"Iterations failed avg: {avg_iterations_failed}"
    )

    # Plot the evolution of average times taken by the VOLE-Paillier and VOLE-OT algorithms
    plt.plot(np.arange(iterations), avg_per_number)
    plt.plot(np.arange(iterations), [mean_of_means] * iterations, 'r--', label=f"Mean of means: {mean_of_means:.6f} seconds")
    plt.plot(np.arange(iterations), [mean_of_means_OT_times] * iterations, 'g--', label=f"Mean of OT means: {mean_of_means_OT_times:.6f} seconds")
    plt.xlabel('Iterations')
    plt.ylabel('Time (seconds)')
    plt.title('VOLE Benchmark times evolution')
    plt.legend()
    plt.show()

#Paillier crypto time benchmarking
elif user == "3":
    Benchmark_times = []
    means_of_means = []
    with tqdm(total=iterations*10, bar_format=bar_format_OT_BM) as pbar3:
        for _ in range(10):
            for i in range(iterations):
                sender , receiver , q = setup()
                crypto_time = compute_vole_HE(sender , receiver , q , benchmark=True)
                Benchmark_times.append(crypto_time)
                pbar3.update(1)
                time.sleep(0.01)
            means_of_means.append(np.mean(Benchmark_times))

    print(np.mean(means_of_means))        
        
    
    
