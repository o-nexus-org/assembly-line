import subprocess
import sys
import os
import time
from typing import Union, Tuple
from pathlib import Path
    
from src.utils import run_bash



def esp_is_connected() -> bool:
    """Checks if the ESP32 is connected"""
    out = run_bash('ls /dev/tty* | grep USB0')
    if out == "":
        return False
    return True


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


def find_mac_in_log() -> Union[str, None]:
    with open('temp_/flashing_log.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.startswith('MAC'):
                mac = extract_and_format_mac_from_str(line=line)
                return mac
    return None


def find_error_in_log() -> Union[str, None]:
    with open('temp_/flashing_log.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.__contains__('error'):
                return line
    return None


def flash_esp() -> Tuple[Union[str, None], Union[str, None]]:
    Path('temp_/flashing_log.txt').unlink(missing_ok=True)
    cmd = """ esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 --before default_reset --after hard_reset write_flash --erase-all -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 firmware/bootloader.bin 0x8000 firmware/partitions.bin 0xd68000 firmware/spiffs.bin 0x20000 testing/data/firmware.bin > temp_/flashing_log.txt"""
    # out = run_bash(cmd)
    # print(out)
    process = subprocess.run(cmd, shell=True,
                             check=False,
                             capture_output=True)
    print('launched flashing')
    
    start_time = time.time()
    timeout = 5
    mac_found = False
    err = None
    while time_left := (time.time() - start_time) < timeout:
        
        if not mac_found:
            print(f'waiting for mac, {timeout - time_left} seconds left')
            mac = find_mac_in_log()
            if mac:
                print(f'mac found: {mac}')
                mac_found = True

        if err:= find_error_in_log():
            print('error found', err)
            return None, err
        time.sleep(1)
    print('finished')
    return mac, None


if __name__ == "__main__":
    # print(esp_is_connected())
    # print(find_mac_in_log())
    flash_esp()


