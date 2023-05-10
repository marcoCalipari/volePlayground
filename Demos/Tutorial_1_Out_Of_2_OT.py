
from Modules.Functions.OT import SimplestOT_1OutOf2
from Modules.Utils.classes import Sender, Receiver

import argparse


def main(verbose=False):
    sender = Sender(m0 = 1 , m1 = 2)
    receiver = Receiver(choice_bit=1)
    
    if verbose:
        print(f"m0 = {sender.m0} , m1 = {sender.m1} , choice_bit = {receiver.choice_bit}")

    result_OT = SimplestOT_1OutOf2(sender, receiver)
    print(result_OT)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform a simple OT 1-out-of-2 protocol.")
    parser.add_argument('-v', '--verbose', action='store_true', help="print verbose output")
    args = parser.parse_args()
    
    main(args)
