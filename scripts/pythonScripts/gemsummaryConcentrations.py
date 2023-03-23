from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
from utilpipeline import (
    calculationGemSummary
)
 

with open('/home/joaquin/projects/methylation/data/commonData/ids_concentraciones_round2.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf',  'time', 'concentration'])

with cd('/home/joaquin/projects/methylation/data/data_concentraciones_round2/'):
    currentTime = None
    currentTf = None
    concentrations = []
    peaksCount = []
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.time), id.concentration)
        if not id.concentration == 'Input':
            with open('significantPeaksGemSumRound2.tsv', 'a+') as sumfile:
                peaks = calculationGemSummary(targetFolder)
                sumfile.write('{}\t{}\n'.format(targetFolder, peaks))
            if currentTime == str(id.time) or currentTime == None:
                currentTime = str(id.time)
                if currentTf == str(id.tf) or currentTf == None:
                    currentTf = str(id.tf)
                    peaksCount.append(peaks)
                    concentrations.append(int(id.concentration[:-2]))
                else:
                    print('1',currentTime)
                    plt.plot(concentrations, peaksCount, '-', label='{}'.format(currentTf))
                    currentTf = str(id.tf)
                    concentrations = [int(id.concentration[:-2])]
                    peaksCount = [peaks]
                    
            else:
                print('2',currentTime)
                plt.plot(concentrations, peaksCount, '-', label='{}'.format(currentTf))
                concentrations = [int(id.concentration[:-2])]
                peaksCount = [peaks]

                plt.legend()
                plt.xlabel("Concetrations")
                plt.ylabel("S Peaks")
                plt.savefig('concentrationsComparation{}minsRound2.jpg'.format(currentTime),
                            dpi=300, bbox_inches='tight')  # _500x10 cbust5000AUC
                plt.clf()
                currentTime = str(id.time)
                currentTf = id.tf
    print('3',currentTime)
    plt.plot(concentrations, peaksCount, '-', label='{}'.format(currentTf))
    plt.legend()
    plt.xlabel("Concetrations(ng)")
    plt.ylabel("S Peaks")
    plt.savefig('concentrationsComparation{}minsRound2.jpg'.format(currentTime),
                dpi=300, bbox_inches='tight')  # _500x10 cbust5000AUC
    plt.clf()




#     sns.distplot(
#         peaksCount,
#         hist=False,
#         kde=True,
#         kde_kws={"linewidth": 3},
#         label=condition,
#     )

# plt.legend(prop={"size": 16}, title="Cases")
# plt.title("SScores")
# plt.xlabel("SScore")
# plt.ylabel("Density")

# plt.savefig(
#     "../data/graphs/negatives10000.jpg",
#     dpi=300,
#     bbox_inches="tight",
# )