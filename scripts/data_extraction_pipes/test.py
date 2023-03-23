import json
import os
import shutil
import subprocess
import tempfile
import glob
import pandas as pd
from functools import reduce
import re
import pandas as pd
import time

# reduce new function https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes

commonpeaksfile = 'allThePossiblePeaksnine_ipinput.bed'

basePathDataFolder = '/home/joaquin/projects/methylation/data'
def performIntersect(folder, intersectFile):
    
    sortedBamFile = glob.glob(f'{folder}/*orted.bam')
    
    if len(sortedBamFile) != 1:
        return print(folder, ' has a problem selecting File')
    else:
        sortedBamFile = sortedBamFile[0]
    
    outputFile = intersectFile.strip().split('/')[-1][:-4]+'_'+sortedBamFile.split('/')[-1][:-10]+'.bed'
    outputFilePath = os.path.join(folder,outputFile)


    print(outputFilePath)
    
    if os.path.isfile(outputFilePath):
        os.remove(outputFilePath)
    if not os.path.isfile(outputFilePath):
        subprocess.call(
            'samtools' + ' view -q1 -b ' + sortedBamFile + ' | ' +
            'bedtools' + ' intersect -abam stdin -b ' + intersectFile + ' -bed -wb -f 0.5 ' +
            '> ' + outputFilePath , shell=True
        )
    else:
        print(outputFile, ' is already done')
    
    totalForBox = {}
    with open(outputFilePath, 'r') as intersectOut:
        intersectDf = pd.read_csv(
            intersectOut, sep='\t', usecols=[3, 12, 13, 14, 15],
            names=['intersected', 'chr', 'start', 'end', 'boxname'],
        )
        for index, ip in intersectDf.iterrows():
            intersectOcurrence = str(ip.intersected.split('/')[0])
            box = ','.join([str(ip.chr), str(ip.start), str(ip.end), ip.boxname])
            if box in totalForBox:
                totalForBox[box].add(intersectOcurrence)
            else:
                totalForBox[box] = {intersectOcurrence}

        for box in totalForBox:
            boxlen = len(totalForBox[box])
            totalForBox[box] = boxlen

        with open(outputFilePath[:-4] + '_boxtotals.csv', 'w') as elcsv:
            elcsv.write('chr,start,end,boxname,{}\n'.format(sortedBamFile.split('/')[-1][:-10]))
            for name, recount in totalForBox.items():
                elcsv.write('{},{}\n'.format(name, recount))

listoffolders = glob.glob('/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/*/*/*')
# parse the experiments file to get the id of each exeriment and the path to that experiment
for experiment in listoffolders:

    print(experiment)
    performIntersect(experiment, commonpeaksfile)