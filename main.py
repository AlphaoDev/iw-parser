#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import re
from tabulate import tabulate
from termcolor import colored

def iw_parsing():
    ''' 
    Function that create a wifi scan process 
    to get some informations and display them 
    in a table via the tabulate module.
    '''

    # Launch process to get result of iw bash command
    res = subprocess.check_output(['iw', 'dev', 'wlan0', 'scan']).decode(sys.stdout.encoding)

    # Create lists sorting results
    scan_ssid, scan_signal, scan_freq, scan_quality, scan_bss, best_signal = ([] for _ in range(6))

    # Process line by line the scan
    while True:
        cnt=0
        for line in res.splitlines():
            line = str(line)
            pattern = re.search('(?:[0-9a-fA-F]:?){12}', line)

            # Get BSS line
            if "BSS " in line and pattern:
                scan_bss.append(pattern.group(0))

            # Get frequency line
            elif "freq:" in line:
                scan_freq.append(line.replace(" ","").replace("freq:","") + "MHz")

            # Get signal line
            elif "signal:" in line.strip():
                # Get signal and calculate quality
                signal = line.replace(" ","").replace("signal:","")
                quality_str = signal.replace("dBm","").replace("\t","")
                quality_calc = round((float(quality_str) + 110) * 10 / 7,2)

                if quality_calc >= 100:
                    quality_calc = 100

                # Check the best signal
                if cnt == 0:
                    best_signal.insert(0, quality_calc)
                    best_signal.insert(1, cnt)

                elif best_signal[0] < quality_calc:
                    best_signal.insert(0, quality_calc)
                    best_signal.insert(1, cnt)
                scan_signal.append(signal)
                scan_quality.append(str(quality_calc) + "%")
                cnt += 1

            # Get SSID line
            elif "SSID:" in line:
                line = line.replace(" ","").replace("SSID:","")
                scan_ssid.append(line)

        break

    # Create table to have a better design
    table = zip(scan_ssid, scan_signal, scan_freq, scan_quality, scan_bss)
    print_best_signal = scan_ssid[best_signal[1]].strip()
    print_best_freq = scan_freq[best_signal[1]].strip()

    # Print informations
    print(colored(f"\nInformations about iw scanning :\n", "red"))
    print(tabulate(table, headers=[colored('SSID','yellow'),
                                   colored('SIGNAL','yellow'),
                                   colored('FREQUENCY','yellow'),
                                   colored('QUALITY','yellow'),
                                   colored('BSS','yellow')])+"\n")
    print(colored("\nNumber of SSIDs scanned : {}".format(len(scan_ssid)), "yellow"))
    print(colored("The best signal is : {} - {}\n".format(print_best_signal, print_best_freq), "yellow"))

if __name__ == "__main__":
    # Launch iw_parsing function
    iw_parsing()