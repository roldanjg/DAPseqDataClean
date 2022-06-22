from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    calculationGemSummary
)

with open('../data/commonData/ids_data_allEcotipe_singleInput.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type'])

with cd('../data/bigwig_allEcotipe_singleInput_N0/'):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.type))
        if not id.tf == 'Input':
            calculationGemSummary(targetFolder)
