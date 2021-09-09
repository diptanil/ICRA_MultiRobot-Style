from .simulation.pseudo_simulation import PseudoSimulator
from .director.director import Director

from os import path
import sys

if __name__ == '__main__':

    error_message = "WRONG INPUT: \n"\
                    "Command to run the pseudo director code: \n" \
                    "python -m multistyle -pseu"

    if len(sys.argv) == 2 and sys.argv[1] == '-pseu':
        PseudoSimulator()
    elif len(sys.argv) == 2 and sys.argv[1] == '-dir':
        Director()
    else:
        print(error_message)