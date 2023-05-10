from Modules.Functions.OT import oneOtOfNOT
from Modules.Utils.classes import Sender, Receiver

sender = Sender(mList=[1 , 2 , 3 , 4 , 5 , 6 , 7 , 8])
receiver = Receiver(choice_bit=5)

result_OT = oneOtOfNOT(sender, receiver , True)
print(result_OT)