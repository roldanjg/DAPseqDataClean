from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    checkMD5isCorrect,
    checkFastaQLenght,
    performTrimGalore,
    qualityCheckTrimGalore,
    performBowtie2,
    getBamAndDeleteSam,
    performGEM
)

with cd('../data/tfs/'):
    targetFolder = 'MYC3/amplified/6/Mock'
    print(('hola'))
    controlfold = '6/Mock'
    performGEM(targetFolder, controlfold)
