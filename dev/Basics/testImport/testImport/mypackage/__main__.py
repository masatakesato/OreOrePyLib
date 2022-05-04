# https://stackoverflow.com/questions/44977227/how-to-configure-main-py-init-py-and-setup-py-for-a-basic-package


###############################################################################################

# for 'python mypackage' execution without pip install
import sys
import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
print( str(current_dir) + '/../' )
sys.path.append( str(current_dir) + '/../' )

###############################################################################################

from mypackage import *


def main():
    func_sub()
    func_same()


if __name__ == '__main__':
    main()