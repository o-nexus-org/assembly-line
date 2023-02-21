from time import time
import os
from src.process import (extract_mac_from_stream,
                         extract_and_format_mac_from_str
)
from pathlib import Path
print(os.getcwd())
print(os.listdir())
print("*" * 20)
test_folder = Path('testing/data')

def test_that_mac_is_properly_extracted():

    print(os.getcwd())
    print(os.listdir())
    print("*" * 20)
    filename = test_folder / 'output_flash.txt'
    with open(filename, 'r', encoding='UTF-8') as file:
        while (line := file.readline().rstrip()):
            if line.startswith('MAC'):
                mac = extract_and_format_mac_from_str(line=line)
                assert mac == 'B8D61AA492A4'


def test_that_fun_stops_when_target_found():
    command = """testing/data/file.sh"""
    # check run time max and return mac
    start = time()
    mac = extract_mac_from_stream(command=command)
    end = time()
    elapsed_s = end - start
    assert elapsed_s < 0.85  # based on file.sh
    assert mac == 'B8D61AA492A4'