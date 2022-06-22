from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    mapMethytilatedCitosine
)

ids_file = '../data/commonData/ids_bisulfite_rep1_rep2.csv'
working_folder = '../data/bisulfite_rep1_rep2/'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'rep', 'time', 'treatment'])

with cd(working_folder):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(str(id.rep), str(id.time), id.treatment)
        mapMethytilatedCitosine(targetFolder)

