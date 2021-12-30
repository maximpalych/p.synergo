# SynergoMSVKTOOLS
# version 1.0
from update_check import checkForUpdates
VERSION = 1.0
RAW_PATH = "https://raw.githubusercontent.com/maximpalych/p.synergo/main/test_update.py"

if __name__ == "__main__":
    checkForUpdates(__file__, RAW_PATH)
