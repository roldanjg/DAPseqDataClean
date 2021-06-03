from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    calculationGemSummary
)

with open('../data/commonData/ids_data_rep_1_End_to_End.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type', 'time', 'tratement'])

with cd('../data/tfs_rep_1/'):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.type), str(id.time), id.tratement)
        if not id.tf == 'Input':
            calculationGemSummary(targetFolder)
