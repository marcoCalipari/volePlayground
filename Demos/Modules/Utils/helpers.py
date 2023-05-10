import random
import hashlib
import hmac
from sympy import isprime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np
from typing import List
import time


def reverse_binary_list(binary_list):
    """Reverse a binary list.

    Parameters
    ----------
    binary_list : list
        A list of binary digits.

    Returns
    -------
    list
        The input binary list in reverse order.

    """
    return binary_list[::-1]


def binary_list_to_int(binary_list):
    """Convert a binary list to an integer.

    Parameters
    ----------
    binary_list : list
        A list of binary digits.

    Returns
    -------
    int
        The integer equivalent of the input binary list.

    """
    binary_str = "".join(str(bit) for bit in binary_list)
    decimal = int(binary_str, 2)
    return decimal


def find_multiplicative_generator(p):
    """Find a multiplicative generator for a given prime p.

    Parameters
    ----------
    p : int
        The prime for which to find a multiplicative generator.

    Returns
    -------
    int or None
        A multiplicative generator of p, or None if one was not found.

    """
    factors = set()
    phi = p - 1

    # Factorize p - 1
    for i in range(2, int(phi**0.5) + 1):
        if phi % i == 0:
            factors.add(i)
            while phi % i == 0:
                phi //= i
    if phi > 1:
        factors.add(phi)

    # Check each number in [1, p-1] until a generator is found
    for a in range(1, p):
        is_generator = True
        for factor in factors:
            if pow(a, phi // factor, p) == 1:
                is_generator = False
                break
        if is_generator:
            return a
    return None


def generate_prime_with_digits(num_digits):
    """Generate a prime number with a specified number of digits.

    Parameters
    ----------
    num_digits : int
        The number of digits the prime should have.

    Returns
    -------
    int
        A prime number with the specified number of digits.

    """
    while True:
        # Generate a random number with the specified number of digits
        p = random.randint(10 ** (num_digits - 1), 10**num_digits - 1)
        # Make sure it's odd
        if p % 2 == 0:
            p += 1
        # Test if it's prime
        if isprime(p):
            return p


def int_to_bytes(i: int) -> bytes:
    """Convert an integer to a big-endian byte string.

    Parameters
    ----------
    i : int
        The integer to convert.

    Returns
    -------
    bytes
        The byte string representation of the input integer.

    """
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder="big")


def PRF(key: bytes, x: int) -> int:
    """Pseudo-random function using HMAC-SHA256.

    Parameters
    ----------
    key : bytes
        The key to use for the HMAC function.
    x : int
        The input value to the PRF.

    Returns
    -------
    int
        The output value of the PRF.

    """
    x_bytes = int_to_bytes(x)
    h = hmac.new(key, x_bytes, hashlib.sha256)
    h_bytes = h.digest()
    return int.from_bytes(h_bytes, byteorder="big")


def int_to_bits(n: int) -> List[int]:
    """
    Convert an integer to a list of its binary digits.

    Parameters
    ----------
    n : int
        The integer to be converted to binary.

    Returns
    -------
    bits_list : List[int]
        A list of integers representing the binary digits of the input integer.

    """
    # Convert to binary string, removing the '0b' prefix
    binary_string = bin(n)[2:]

    # Convert string to list of bits (0 and 1)
    bits_list = [int(bit) for bit in binary_string]

    return bits_list


def generate_random_a_b(prime_p: int) -> tuple[int, int]:
    """
    Generate two random integers in the range [1, prime_p-1].

    Parameters
    ----------
    prime_p : int
        The prime number used for generating the public keys.

    Returns
    -------
    tuple[int, int]
        A tuple of two randomly generated integers.

    """
    return random.randint(1, prime_p - 1), random.randint(1, prime_p - 1)


def calculate_public_keys(
    sender: object, receiver: object, generator: int, a: int, b: int, prime_p: int
) -> None:
    """
    Calculate the public keys for the sender and receiver.

    Parameters
    ----------
    sender : object
        An object representing the sender.
    receiver : object
        An object representing the receiver.
    generator : int
        The generator used for generating the public keys.
    a : int
        The randomly generated integer for the sender.
    b : int
        The randomly generated integer for the receiver.
    prime_p : int
        The prime number used for generating the public keys.

    """
    sender.A = pow(generator, a, prime_p)
    receiver.B = (
        pow(generator, b, prime_p)
        if receiver.choice_bit == 0
        else sender.A * pow(generator, b, prime_p)
    )


def derive_shared_keys(
    sender: object, receiver: object, a: int, b: int, prime_p: int
) -> None:
    """
    Derive the shared keys for the sender and receiver.

    Parameters
    ----------
    sender : object
        An object representing the sender.
    receiver : object
        An object representing the receiver.
    a : int
        The randomly generated integer for the sender.
    b : int
        The randomly generated integer for the receiver.
    prime_p : int
        The prime number used for generating the public keys.

    """
    sender.k0 = hashlib.sha256(f"{pow(receiver.B, a, prime_p)}".encode()).digest()
    sender.k1 = hashlib.sha256(
        f"{pow(receiver.B // sender.A, a, prime_p)}".encode()
    ).digest()
    receiver.kr = hashlib.sha256(f"{pow(sender.A, b, prime_p)}".encode()).digest()


def process_encryption_decryption(sender, receiver, initialization_vector):
    """
    Perform encryption or decryption of the message using the AES cipher.

    Parameters
    ----------
    sender : object
        An object containing the public keys, secret keys, and messages of the sender.
    receiver : object
        An object containing the public keys and secret key of the receiver.
    initialization_vector : bytes
        The initialization vector for the AES cipher.

    Returns
    -------
    bytes
        The decrypted or encrypted message.

    """

    key = sender.k0 if receiver.choice_bit == 0 else sender.k1
    message = str(sender.m0) if receiver.choice_bit == 0 else str(sender.m1)
    
    cipher = AES.new(key, AES.MODE_CBC, iv=initialization_vector)
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    cipher_decryption = AES.new(receiver.kr, AES.MODE_CBC, iv=initialization_vector)
    return unpad(cipher_decryption.decrypt(encrypted_message), AES.block_size)


def generate_OT_keys(hmac_key):
    """
    Generate two one-time keys using the HMAC function with the given key.

    Parameters
    ----------
    hmac_key : bytes
        The key for the HMAC function.

    Returns
    -------
    tuple
        A tuple containing two one-time keys.

    """

    return PRF(hmac_key, random.randint(1, 2**8)), PRF(
        hmac_key, random.randint(1, 2**8)
    )


def pad_receiver_choice_bits(receiver, sender):
    """
    Pad the receiver's choice bits with zeros so that it matches the length of the sender's message.

    Parameters
    ----------
    receiver : object
        An object containing the public keys and secret key of the receiver.
    sender : object
        An object containing the public keys, secret keys, and messages of the sender.

    """

    pad_value = len(int_to_bits(len(sender.mLlist) - 1)) - len(receiver.receiver_bits)
    receiver.receiver_bits[:0] = [0] * pad_value


def pad_list(unpadded_list, max_bits):
    """
    Pad the list with zeros so that it has a maximum length of `max_bits`.

    Parameters
    ----------
    unpadded_list : list
        The list to be padded.
    max_bits : int
        The maximum length of the list after padding.

    Returns
    -------
    list
        The padded list.

    """

    pad_value = max_bits - len(unpadded_list)
    padded_list = [0] * pad_value + unpadded_list

    return padded_list


def mock_decomposition(b, q, max_bits , max_iterations = 10000):
    """
    Perform the mock decompositon of `b` using `q`.

    Parameters
    ----------
    b : int
        The number to be decomposed.
    q : int
        The parameter for the mock decomposition.
    max_bits : int
        The maximum number of bits in the binary representation of the decomposed number.

    Returns
    -------
    list
        The binary representation of the decomposed number.

    """

    b_decomposed = 0
    limit = 0
    
    while b_decomposed != b and limit < max_iterations:
        b_i = [random.randint(0, q) for _ in range(max_bits)]
        # Calculate b such that b = sum(2^i-1*b_i)
        b_decomposed = sum([(2**i) * b_i[i] for i in range(max_bits)]) % q
        limit += 1
        
    
    if limit == max_iterations:
        return None
    else:
        return reverse_binary_list(b_i)


def VOLE_Reconstruction(y):
    """
    Perform the VOLE reconstruction algorithm to reconstruct the number `y` from its binary representation.

    Parameters
    ----------
    y : list
        The binary representation of the number to be reconstructed.

    Returns
    -------
    int
        The reconstructed number.

    """

    result = 0
    for i in range(len(y)):
        result += y[i] * 2**i

    return result
