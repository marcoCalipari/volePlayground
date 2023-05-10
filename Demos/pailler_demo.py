# https://asecuritysite.com/encryption/homomorphic
import random
from Modules.Utils.paillier import *
from Modules.Utils.classes import *

     
def compute_vole_HE():
    
    p = 2**7
    
    sender = OLE_Sender(random.randint(0 , p))
    receiver = OLE_Receiver(random.randint(0 , p) , random.randint(0 , p))
    
    print(f"a = {receiver.a} , b= {receiver.b} , x = {sender.x}")
    #Now We do the paillier encryption
    
    priv,pub = generate_keypair(128)
    
    enc_x = encrypt(pub, sender.x)
    enc_b = encrypt(pub, receiver.b)
    
    operation = (e_add(pub=pub , a=enc_b , b=e_mul_const(pub , enc_x , receiver.a)))
    sender.y.append(decrypt(priv , pub , operation))
    print(f"expected result = {((sender.x*receiver.a)+receiver.b) % p} , our result = {sender.y[0] % p}")
    
def working_demo():
    a = 5
    b = 10    
    x = 2  

    priv, pub = generate_keypair(128)

    ca, cb , cx = encrypt(pub, a), encrypt(pub, b) , encrypt(pub, x)

    print("A: ",a)
    print("B: ",b)
    print("X: ",x)
    print("Cipher(A): ",ca)
    print("Cipher(B): ",cb)
    print("Cipher(X): ",cx)


    #a should not be encrypted.

    y_enc = e_add (pub , e_mul_const(pub, cx, a) , cb)
    print(y_enc)
    print(decrypt(priv, pub, y_enc))

#working_demo()
compute_vole_HE()