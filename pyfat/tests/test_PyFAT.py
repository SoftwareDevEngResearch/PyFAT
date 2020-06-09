import os, sys
from pathlib import Path

main_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(main_dir,'..'))
import PyFAT


def test_io_sorter():

    """Test for correct reading of inpout .txt file to identify input and
    output locations"""

    cwd = os.path.dirname(os.path.abspath(__file__))

    loc = Path(cwd,"inputs","example_input.txt")
    loc = str(loc)

    input_loc, output_loc = PyFAT.io_sorter(loc)

    assert input_loc == "ThisistheInputLocation!\n"
    assert output_loc == "ThisistheOutputLocation!"
