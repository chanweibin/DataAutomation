from enum import Enum, unique

@unique
class InputFileType(Enum):
    csv = 1 
    xml = 2
    xls = 3
    
@unique
class OutputFileType(Enum):
    xls = 1 
    html = 2
    