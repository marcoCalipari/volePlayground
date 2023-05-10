from Modules.Functions.OT import VOLE
from Modules.Utils.classes import OLE_Sender , OLE_Receiver

sender = OLE_Sender(16)
receiver = OLE_Receiver(27 , 4)
q = 2**7

result_OT = VOLE(sender, receiver , q  , True)
print(result_OT)