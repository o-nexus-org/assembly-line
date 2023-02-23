#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import subprocess
import sys
import os
import time
from src.utils import run_bash


def extract_and_format_mac_from_str(line: str) -> str:
    """ extract mac from string like MAC: b8:d6:1a:a4:92:a4"""
    mac = line.split('MAC')[1]
    return (mac
            .replace(" ", '')
            .replace(":", "")
            .strip().upper()
            )


def extract_mac_from_stream(command: str) -> str:
    command = command.split(" ")
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = process.stdout.readline()
    while True:
        output = process.stdout.readline()
        output = output.decode("utf-8").strip().replace('\n', '')
        print(output)
        if output.startswith('MAC'):
            mac = extract_and_format_mac_from_str(line=output)
            print('mac found, exiting')
            break
    return mac


if __name__ == '__main__':
    
    check = "ls /dev | grep ttyUSB"
    out_check = run_bash(check)
    print(out_check)
    if out_check == '':
        print('no device found')
    else:    
        command = '''esptool.py --chip esp32 --port /dev/ttyUSB0 \
                                --baud 460800 --before default_reset \
                                --after hard_reset write_flash \
                                --erase-all -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 firmware/bootloader.bin 0x8000 firmware/partitions.bin 0xd68000 firmware/spiffs.bin 0x20000 testing/data/firmwarev62.bin
                                '''
        # extract_mac_from_stream(command)