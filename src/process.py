#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import subprocess
import sys
import os
import time


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

