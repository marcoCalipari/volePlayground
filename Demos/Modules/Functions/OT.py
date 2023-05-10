
import hashlib
import random
import math
import time

from Modules.Utils.classes import *
from Modules.Utils.helpers import *



def SimplestOT_1OutOf2(sender, receiver, multi=False , benchmark = False):
    
    """
    execute the simplest 1 out of 2 OT protocol (based on this paper https://eprint.iacr.org/2015/267.pdf).
    
    Parameters
    ----------------
    sender : object:Sender
        The sender of the OT protocol. (Who holds the messages)
    receiver : object:Receiver
        The receiver of the OT protocol. (Who chooses which message to receive)
        
    multi: bool
        Since the one 1-out-of-N and the N-out-of-K are based on the 1 out of 2 protocol, this parameter will take care of distinguishing in case
        we are executing just a 1-out-of-2 or a multi OT protocol.
    
    Returns
    ----------------
        if multi = False: the message chosen by the receiver
        if multi = True: It will not return anything, but it will append the message chosen by the receiver to the receiver's receiver_keys list
        (To be modified later)
    
    
    Function Logic    
    ----------------
    
    we follow the steps of the paper, and we use the functions defined in the helpers.py file to make the code more readable.
    1) A setup phase in which we generate the prime p, the generator g, and the random numbers a and b.
    2) The parameters A,B are calculated and then sent
    3) A key derivation phase in which we compute the keys needed for the encryption and decryption
    4) A final transmission phase in which we encrypt the messages with the keys derived in the previous step and send them to the receiver, which will be able to decrypt only one
    
    """
    
    
    initialization_vector = bytearray("J78GffvFmoNLixum".encode())
    prime_p = generate_prime_with_digits(3)
    generator = find_multiplicative_generator(prime_p)
    while generator is None:
        prime_p = generate_prime_with_digits(3)
        generator = find_multiplicative_generator(prime_p)

    a, b = generate_random_a_b(prime_p)
    calculate_public_keys(sender, receiver, generator, a, b, prime_p) #We calculate A and B for the protocol
    derive_shared_keys(sender, receiver, a, b, prime_p) # we compute the keys
    start_time = time.monotonic()
    result = process_encryption_decryption(sender, receiver, initialization_vector)
    stop_time = time.monotonic()

    if multi:
        receiver.receiver_keys.append(int(result.decode()))
        #TODO: MODIFY THE CLASSES SUCH THAT WE CAN RETURN A LIST DIRECTELY
     
    if not benchmark:
           
        return int(result.decode())
    else: 
        crypto_time = stop_time - start_time
        return int(result.decode()) , crypto_time

def oneOtOfNOT(sender, receiver , verbose = False):
    """
    Function perfroming the 1-out-of-N OT protocol. It is based on the 1-out-of-2 protocol, and it is based on the paper: https://dl.acm.org/doi/pdf/10.1145/301250.301312
    
    Parameters
    ----------------
    
    sender : object:Sender
        The sender of the OT protocol. (Who holds the messages). In this case the sendeer will hold a vector(list) of messages
    
    receiver : object:Receiver
        The receiver of the OT protocol. (Who chooses which message to receive). In this case the receiver will choose a number between 1 and N, 
        where N is the length of the sender's message vector. The number will indicate the INDEX of the message that the receiver wants to observe.
    
    Returns
    ----------------
    reult : int
        Message chosen by the receiver
    
    
    """
    
    
    sender.Y = []
    
    l = round(math.sqrt(len(sender.mLlist))) #the l based on the paper
    
    #Listst holding the key pairs generated for the protocol and the xor combinations of the keys
    key_pairs = []
    xored_key_list = []

    # As a PRF we use HMAC with a random key generated with sha256
    hmac_key = hashlib.sha256(f"{random.randint(1, 2**8)}".encode()).digest()

    for _ in range(int(l)):
        key_pairs.append(generate_OT_keys(hmac_key))
        
        
    # This portion of code is responsable of generating the xor combinations of the keys.
    # The keys are combined in a "truth table" fashion.
    
    # for example if we have N = 4 messages, then l = 2, and the key pairs will be:
    #                   key_pairs = [[k1_0,k1_1], [k2_0,k2_1]]
    # Then the corresponding key combinations of the indexes will be:
    # 
    #   Index   I_0    I_1      key_combination(xor)  
    #  ------- ------ ------ ------------------------ 
    #       0      0      0      k1_0^k2_0            
    #       1      0      1      k1_0^k2_1            
    #       2      1      0      k1_1^k2_0            
    #       3      1      1      k1_1^k2_1            
    
    # So the bit decomposition of the indexes will determine the combination of the keys.
    
    # Another way to consider this is by imagining a matrix of keys.
    

    # Discalmer: While talking about indexes we will use the 1 based counting, but for all the coding the 0 base counting has been considered
    # 
    # 
    # ##
        
    ex_bin = {}
    for ex in range(len(sender.mLlist)):
        ex_bin[ex] = pad_list(int_to_bits(ex) , len(int_to_bits(len(sender.mLlist) - 1)))
        
# this looks correct. It does all the xor combinations
    for key in ex_bin.keys():
        I = 0
        temp = []
        for elem in ex_bin[key]:
            
            temp.append(key_pairs[I][elem])
            I += 1
        temp_xor = 0
        for n in temp:
            temp_xor ^= n                
        xored_key_list.append(temp_xor)
                 

    #Here we generate the Y vector, where each value is compute as:
    
    #  Y_i = X_i ^ K_i (from the xored key list)
    for i in range(len(sender.mLlist)):
        sender.Y.append(sender.mLlist[i] ^ xored_key_list[i])

    
    
    # In this section we prepare to engage in the 1-out-of-2 OT protocol.
    # For this specific protocol we will need to perfom l rounds of it. 
    # Since the receiver already knows the index of the message he wants to receive,
    # It will be just necessary for it to bit decompose it in l bits, and then use those bits as choice bits for the 1-out-of-2 protocol.
    #
    # for example: 
    #       If the receiver wants to receive the 2nd message:
    #       
    #       (2)_10 = (1 , 0)_2
    
    #       first OT round: choice bit = 1
    #       second OT round: choice bit = 0
    #       
    #       In this way we can ensure that the key combination at the receiver side is the same used from the sendeer while prepping
    # ##
    
    
    receiver.receiver_bits = int_to_bits(receiver.choice_bit - 1)
    pad_receiver_choice_bits(receiver, sender)

    for index in range(round(int(l))):
        #this is the other problem
        sender.m0 = str(key_pairs[index][0])
        sender.m1 = str(key_pairs[index][1])
        
        receiver.choice_bit = receiver.receiver_bits[index]
        SimplestOT_1OutOf2(sender, receiver, True)

    receiver_xored_keys = 0

    # Here we reconstruct the original message at the given index
    for m in receiver.receiver_keys:
        receiver_xored_keys ^= m
        
    
    if verbose:
        
        print(f"message vector {sender.get_message_list()}\nThe receiver wants to observe the message at index {receiver.get_choice_bit()}\n"
              f"The keypairs are : {key_pairs}"
              f"The resulting message is {sender.Y[receiver.placeHolder - 1] ^ receiver_xored_keys}")

    return (sender.Y[receiver.placeHolder - 1] ^ receiver_xored_keys)

def kOutOfN(sender: Sender, receiver: Receiver , verbose = False):
    """
    Function that perfroms the k-out-of-N OT protocol based on multiple iterations of the 1-out-of-N OT protocol.
    
    Parameters:
    ----------------
    sender: Sender
        The sender object that holds the sender's data.
        
    receiver: Receiver
        The receiver object that holds the receiver's data.
        
    Returns:
    ----------------
    
    receiver.result: list
        List with the values that the sender wanted to observe, based on the chosen index
    
    """
    for choice in receiver.choices:
        r = Receiver(choice)
        t = oneOtOfNOT(sender, r)
        receiver.result.append(t)

    if verbose:
        print(f"message vector {sender.get_message_list()}\nThe receiver wants to observe the message at index {receiver.get_choices()}\n"
              f"The resulting message is {receiver.result}")
    return receiver.result

def VOLE(Alice: OLE_Sender, Bob: OLE_Receiver, q: int , verbose = False , Benchmark = False):
    
    """
    Function performing VOLE based on the presentation in: https://youtu.be/ZfdXY_oLhSo?t=1667

    Alice and Bob wants to evaluate the expression y = b + x*a 
    where:
        Alice holds the value of x in Z_p
        Bob holds the values of a(secret) and b, both in Z_p

    The evaluation goes as follows:
        1) Alice will bit decompose x and Bob will decompose b in coefficents b_i. 
        The decomposition of b is done as follows:
            b_i is randomly sampled from Z_p such that b = sum(b_i * 2**i) mod q 
        
        2) Alice and Bob then will engage in a series of 1-out-of-2 OT protocols, where:
            choice bit = x_i
            m0 = b_i
            m1 = b_i + a mod q
            
        3) After all the OT protocols are done, Alice will compute the following expression:
            y = sum(y_i * 2**i) mod q
    """
    
    x_bin = int_to_bits(Alice.x)
    #We perform the coefficient decomposition
    b_decomposed = mock_decomposition(Bob.b , q , len(x_bin))
    
    if verbose:        
        print(f"x = {Alice.x} and x_bin = {x_bin} ,\nb = {Bob.b} and b_decomposed = {b_decomposed}, \na = {Bob.a}")
    
    #now we can engage in a 1-2 OT protocol for each element of the bit decomposition
    OLE_y = []
    #second attempt is to use a but bit decomposed
    "If we were not able to continue with the decomposition then we return"
    if b_decomposed is None:
        return None
        
    for i in range(len(x_bin)):
        
        OT_sender = Sender(m0=b_decomposed[i] , m1=((b_decomposed[i]+Bob.a)%q))
        OT_receiver = Receiver(choice_bit=x_bin[i])
        if not Benchmark:
            OLE_y.append(SimplestOT_1OutOf2(OT_sender , OT_receiver))
        else:
            r, time = SimplestOT_1OutOf2(OT_sender , OT_receiver , benchmark=Benchmark)
            return time
        
    if verbose:
        print(f"result in binary: {OLE_y} = {VOLE_Reconstruction(reverse_binary_list(OLE_y))%q} modulo {q}")
        print(f"expected result: b + x*a = {Bob.b} + {Alice.x} * {Bob.a} modulo {q} = {(Bob.b +( Alice.x*Bob.a))%q}")
    
    result = VOLE_Reconstruction(reverse_binary_list(OLE_y))%q
    return result
    
    


