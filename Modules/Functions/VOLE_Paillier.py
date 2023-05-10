
from Modules.Utils.paillier import *
from Modules.Utils.classes import *

def compute_vole_HE(sender:OLE_Sender , receiver:OLE_Receiver , q:int , verbose:bool = False):
    
    p = q
    if verbose:
        
        print(f"a = {receiver.a} , b= {receiver.b} , x = {sender.x}")
    #Now We do the paillier encryption
    
    priv,pub = generate_keypair(128)
    
    enc_x = encrypt(pub, sender.x)
    enc_b = encrypt(pub, receiver.b)
    
    operation = (e_add(pub=pub , a=enc_b , b=e_mul_const(pub , enc_x , receiver.a)))
    sender.y.append(decrypt(priv , pub , operation))
    if verbose:
        print(f"expected result = {((sender.x*receiver.a)+receiver.b) % p} , our result = {sender.y[0] % p}")
    result = sender.y[0] % p
    return result