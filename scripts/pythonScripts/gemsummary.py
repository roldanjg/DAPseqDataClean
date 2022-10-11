from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    calculationGemSummary
)

with open('/home/joaquin/projects/methylation/data/commonData/ids_data_dobles_JM15.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type', 'crazy', 'cinco'])

with cd('/home/joaquin/projects/methylation/data/data_dobles_JM15'):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.type), str(id.crazy), str(id.cinco))
        if not id.tf == 'Input':
            calculationGemSummary(targetFolder)
