from tkinter import S
from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    calculationGemSummary,
    calculationBowtieSummary
)
ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_data_MYC2_Fragaria_vesca_Franco.csv'
working_folder = '/home/joaquin/projects/methylation/data/data_MYC2_Fragaria_vesca_Franco/'


with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'inputid'])


with open(f'{working_folder}/summary.tsv', 'w') as  hola:

    with cd(working_folder):
        for index, id in idsDf.iterrows():
            targetFolder = os.path.join(id.tf, str(id.inputid))
            Significant='not done'
            if id.tf != 'Input':
                Significant = calculationGemSummary(targetFolder)
                print(Significant)
            reads, alingpercent = calculationBowtieSummary(targetFolder)
            print(reads,
                    alingpercent,
                    Significant)
            hola.write(
                '{}\t{}\t{}\t{}\n'.format(
                    id.tf, 
                    reads,
                    alingpercent,
                    Significant
                    )
                    ) 
