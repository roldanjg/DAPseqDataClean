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
ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_data_bHLH61_full_lenght.csv'
working_folder = '/home/joaquin/projects/methylation/data/data_bHLH61_full_lenght'


with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'replicate', 'condition'])


with open('summary.tsv', 'w') as  hola:

    with cd(working_folder):
        for index, id in idsDf.iterrows():
            targetFolder = os.path.join(id.replicate, id.condition)
            Significant='not done'
            if id.replicate != 'Input':
                Significant = calculationGemSummary(targetFolder)
                print(Significant)
            reads, alingpercent = calculationBowtieSummary(targetFolder)
            print(reads,
                    alingpercent,
                    Significant)
            hola.write(
                '{}_{};{};{};{}\n'.format(
                    id.replicate, 
                    id.condition, 
                    reads,
                    alingpercent,
                    Significant
                    )
                    )
