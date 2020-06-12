# get OS info
# get python version info

import platform
import sys

info = 'OS info is \n {} \n\nPython version is {} {}'.format(
    platform.uname(), sys.version, platform.architecture())

print(info)

with open('os_info.txt', 'w') as ff1:
    ff1.write(info)