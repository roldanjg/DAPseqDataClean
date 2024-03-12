#!/usr/bin/env python3
import os
import subprocess
import os
import glob
import argparse

############################################
############################################
## PARSE ARGUMENTS
############################################
############################################

Description = 'Check MD5 from Novogene raw data downloads'
Epilog = """Example usage: novogene_check_MD5.py --path_prefix <PATH_PREFIX>"""

argParser = argparse.ArgumentParser(description=Description, epilog=Epilog)

## REQUIRED PARAMETERS
argParser.add_argument(
    "-pp",
    "--path_prefix",
    type=str,
    dest="PATH_PREFIX",
    default=False,
    help="Path to the folder with all the individual folders with raw samples.",
)

args = argParser.parse_args()

class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def checkMD5isCorrect(folder):
    with cd(folder):
        if not os.path.isfile('check.txt'):
            subprocess.run('md5sum *gz >check.txt', shell=True)
        md5lines = set()
        for md5 in ['MD5.txt','check.txt']:
            len_file = 0
            with open(md5,'r') as openmd5:
                for line in openmd5:
                    md5lines.add(line.strip().split('\s\s')[0])
                    len_file +=1
        if len_file == len(md5lines):
            print('Files in ' + folder + 'are OK')
        else:
            print('Files in ' + folder + 'are corrupted by MD5 annalisys')

for selected_folder in glob.glob(f'{args.PATH_PREFIX}/*'):
    checkMD5isCorrect(selected_folder)
