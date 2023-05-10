import time
from Modules.Utils.paillier import *
from Modules.Utils.classes import *

def compute_vole_HE(sender:OLE_Sender , receiver:OLE_Receiver , q:int , verbose:bool = False , benchmark = False):
    
    p = q
    if verbose:
        
        print(f"a = {receiver.a} , b= {receiver.b} , x = {sender.x}")
    #Now We do the paillier encryption
    
    priv,pub = generate_keypair(128)
    
    start_time_enc_x = time.monotonic()
    enc_x = encrypt(pub, sender.x)
    stop_time_enc_x = time.monotonic()
    
    start_time_enc_b = time.monotonic()
    enc_b = encrypt(pub, receiver.b)
    stop_time_enc_b = time.monotonic()
    
    x_encTime = stop_time_enc_x - start_time_enc_x
    b_encTime = stop_time_enc_b - start_time_enc_b
    tot_enc_time = x_encTime + b_encTime
    
    
    operation = (e_add(pub=pub , a=enc_b , b=e_mul_const(pub , enc_x , receiver.a)))
    dec_time_start = time.monotonic()
    decrypted = decrypt(priv , pub , operation)
    dec_time_stop = time.monotonic()
    
    tot_dec_time = dec_time_stop - dec_time_start
    
    sender.y.append(decrypted)
    if verbose:
        print(f"expected result = {((sender.x*receiver.a)+receiver.b) % p} , our result = {sender.y[0] % p}")
        
    result = sender.y[0] % p
    if not benchmark:
        return result
    else:
        return (tot_dec_time+tot_enc_time)