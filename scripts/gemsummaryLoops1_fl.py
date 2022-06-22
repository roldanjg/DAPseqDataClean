from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    calculationGemSummary
)

with open('../data/commonData/ids_data_loops_fl_2.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type'])

with cd('../data/data_loops_fl_2'):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.type))
        if not id.tf == 'Input':
            calculationGemSummary(targetFolder)