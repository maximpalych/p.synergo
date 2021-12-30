# SynergoMSVKTOOLS
# version 2.0
from update_check import isUpToDate
VERSION = 2.0

if __name__ == "__main__":

    if isUpToDate(__file__, "https://github.com/maximpalych/p.synergo/blob/main/test_update.py"):
        print('new version not found!')
        
