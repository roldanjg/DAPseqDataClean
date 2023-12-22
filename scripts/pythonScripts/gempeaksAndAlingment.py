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
case = 'slovenia_input_correcto'
ids_file = f'/home/joaquin/projects/methylation/data/commonData/ids_data_{case}.csv'
working_folder = f'/home/joaquin/projects/methylation/data/data_{case}/'


with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['rawindex', 'tf']) #, 'treatment', 'rep'


with open(f'/home/joaquin/projects/methylation/peaks_and_alingment/{case}_summary.tsv', 'w') as  hola:

    with cd(working_folder):
        for index, id in idsDf.iterrows():
            targetFolder = os.path.join(id.tf) #,str(id.treatment),str(id.rep)
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
                    ) #+'_'+str(id.treatment)+'_'+str(id.rep)

# names=['rawindex', 'tf', 'treatment', 'rep']
# id.tf,str(id.treatment),str(id.rep)
# id.tf+'_'+str(id.treatment)+'_'+str(id.rep)