from enum import Enum

class Station(Enum):
    SGS = "sgs"
    MTI = "mti"
    MPS = "mps"
    INS = "ins"
    KSE = "kse"
    PAR = "par"
    NSG = "nsg"
    
class Mission(Enum):
    S1 = "s1"
    S2 = "s2"
    S3 = "s3"
    

class ProcessorName(Enum):
    S1_AIO = "s1-aio"
    S1_L0ASP = "s1-l0asp"
    S1_L1 = "s1-l1"
    S1_L2 = "s1-l2"    
