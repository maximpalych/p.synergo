# SynergoMSVKTOOLS
# version 1.0
from update_check import isUpToDate
VERSION = 1.0

if __name__ == "__main__":

    if isUpToDate(__file__, "https://raw.githubusercontent.com/maximpalych/p.synergo/main/test_update.py"):
        print('new version found!')
