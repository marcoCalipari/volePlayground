class Sender:
    """
    Sender class for the OT protocol.

    ----------------

    Attributes:

    m0: int
        Message chosen by the sender to be sent to the receiver if the choice bit is 0

    m1: int
        Message chosen by the sender to be sent to the receiver if the choice bit is 1

    mLlist: list
        Contains a list representing the vector messages in case of a "multi OT" (not a 1 out of 2 OT)
        It need to be set before instanciating the OT interaction

    Y: list
        Contains the vector of messages that the sender will send to the receiver in case of a "multi OT"

    a , b , A , k0 , k1: int
        Parameters used in the 1 out of 2 OT protocol as explained in the paper "simplest OT protocol"

    ----------------

    Methods:
        None


    """

    def __init__(self, m0: int = None, m1: int = None , mList: list = None):
        self.m0 = m0
        self.m1 = m1

        # for multi ot
        self.mLlist = mList
        self.Y = []

        self.a = 0
        self.b = 0
        self.A = 0
        self.k0 = 0
        self.k1 = 0
        
    def get_message_list(self):
        return self.mLlist
    
    def get_messages(self):
        return (self.m0 , self.m1)


class Receiver:
    """
    Receiver class for the OT protocol.

    ----------------

    Attributes:

    choice_bit: int
        The choice bit chosen by the receiver to choose which message to receive from the sender

    placeHolder: int
        A puppet variable used to store the choice bit in case of a multi OT, to be changed later

    receiver_bits: list
        list representing the bit decomposition of the receiver's choice bit. Which in case of the multi OT will be the (index-1) binary decomposition

    receiver_keys: list
        The keys the receiver will store after performing the 1 out of N
    
    choices: list
        In case of a k out of N OT, this list will contain the INDEXES that the receiver wants to reveal from the sender's inputs.
        


    ----------------

    Methods:
        None


    """

    def __init__(self, choice_bit = None , choices = None):
        self.choice_bit = choice_bit

        self.B = 0
        self.kr = 0
        self.x = 0

       
 
        # for multi ot
        
        self.result = []
        self.placeHolder = choice_bit
        self.receiver_bits = []
        self.receiver_keys = []

        # for k out of n OT
        self.choices = choices
        
    def get_choice_bit(self):
        return self.placeHolder
    
    def get_choices(self):
        return self.choices


class OLE_Sender:
    """
    Sender class for the OT protocol.

    ----------------

    Attributes:

    x: int
        the value x that the Sender wants to multiply to a in a OLE istance
    
    y: list
        List containing all the y values calculated during the OLE protocol
    ----------------

    Methods:
        None


    """
    
    
    def __init__(self, x):
        self.x = x
        self.y = []


class OLE_Receiver:
    """
    Receiver class for the OT protocol.
    ----------------
    Attributes:

    a: int
        the value a that the Sender wants to multiply to x in a OLE istance
    
    b: int
        List containing all the b value we want to evaluate during the OLE protocol
    ----------------
    Methods:
        None

    """
    
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b
