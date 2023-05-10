from Modules.Functions.OT import kOutOfN
from Modules.Utils.classes import Sender, Receiver

sender = Sender(mList=[1 , 2 , 3 , 4 , 5 , 6 , 7 , 8])
receiver = Receiver(choices=[3 , 5 , 8])

result_OT = kOutOfN(sender, receiver , True)
print(result_OT)