from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    calculationGemSummary
)

with open('../data/commonData/ids_data_sophie.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type', 'crazy'])

with cd('../data/data_sophie/'):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.type), str(id.crazy))
        if not id.tf == 'Input':
            calculationGemSummary(targetFolder)
