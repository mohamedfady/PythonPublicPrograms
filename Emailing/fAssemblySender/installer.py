import os
try:
    os.system('pip install psutil')
except:
    pass

import psutil

def pip_os():
    if psutil.MACOS == True or psutil.LINUX == True : return 'pip3'
    if psutil.WINDOWS == True : return 'pip'


def libs_installer():
    libs = ['urllib3','requests','colorama','termcolor','bs4']
    for lib in libs:
        os.system(pip_os() + ' install ' + lib)
    return "Installed"


if __name__ == '__main__':
    # update pip
    os.system(pip_os() + ' install --upgrade pip')
    # install libs
    print('Requirements : ' + libs_installer())
