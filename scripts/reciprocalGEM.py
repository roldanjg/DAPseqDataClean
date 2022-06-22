from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
from utilpipeline import (
    performGEMfree
)


information = [
    ['/home/joaquin/projects/methylation/data/data_allEcotipe_singleInput_N0/IP/3/IP3sorted.bam','/home/joaquin/projects/methylation/data/data_concentraciones/CTAB/7/50ng/CTAB750ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/IP3-N06'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones/CTAB/7/50ng/CTAB750ngsorted.bam','/home/joaquin/projects/methylation/data/data_allEcotipe_singleInput_N0/IP/3/IP3sorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/N06-IP3'],
    ['/home/joaquin/projects/methylation/data/data_allEcotipe_singleInput_N0/IP/4/IP4sorted.bam','/home/joaquin/projects/methylation/data/data_concentraciones/CTAB/7/50ng/CTAB750ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/IP4-N06'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones/CTAB/7/50ng/CTAB750ngsorted.bam','/home/joaquin/projects/methylation/data/data_allEcotipe_singleInput_N0/IP/4/IP4sorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/N06-IP4'],
    ['','',''],
]



for samplePath, inputControlpath, outputPaht in information:
    # print(samplePath, inputControlpath, outputPaht)

    performGEMfree(samplePath, inputControlpath, outputPaht)

