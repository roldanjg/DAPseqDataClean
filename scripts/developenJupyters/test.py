import json
import os
import shutil
import subprocess
import time
import glob
import pandas as pd
from time import time,ctime

commonpeaksfile = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/allThePossiblePeaksnine.bed'

metadata = '/home/joaquin/projects/methylation/data/commonData/ids_data_allReplicates_methylation.json'
basePathDataFolder = '/home/joaquin/projects/methylation/data'
narrowPeakLocationFolders = ['tfs_rep_1','tfs_rep_3_input_from_rep_2', 'tfs_rep_2', 'tfs_rep_4']
specificPathsSumary = {}

def performIntersect(folder, intersectFile):
    
    sortedBamFile = glob.glob(f'{folder}/*orted.bam')
    
    if len(sortedBamFile) != 1:
        return print(folder, ' has a problem selecting File')
    else:
        sortedBamFile = sortedBamFile[0]
    
    outputFile = intersectFile.strip().split('/')[-1][:-4]+'_'+sortedBamFile.split('/')[-1][:-10]+'.bed'
    outputFilePath = os.path.join(folder,outputFile)
    print(outputFilePath)
    
    if os.path.isfile(outputFilePath) and os.path.isfile(outputFilePath[:-4] + '_boxtotals.csv'):
        print(outputFilePath,outputFilePath[:-4] + '_boxtotals.csv')
        return print('already done')
    
    print(outputFilePath,'hola',outputFilePath[:-4] + '_boxtotals.csv')
    subprocess.call(
        'samtools' + ' view -q1 -b ' + sortedBamFile + ' | ' +
        'bedtools' + ' intersect -abam stdin -b ' + intersectFile + ' -bed -wb -f 0.5 ' +
        '> ' + outputFilePath , shell=True
    )
    
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


with open(metadata) as jsonMetadata:
    experimentsClasification = json.load(jsonMetadata)['experiments']
for experiment in experimentsClasification:
    specificPathsSumary[experiment['condition']] = {}
    for metState in ['direct', 'amplified']:
        specificPathsSumary[experiment['condition']][metState] = {}
        for exptype in ['sample', 'input']:
            specificPathsSumary[experiment['condition']][metState][exptype] = {}
            for replicate, number in zip(
                experiment[metState],
                ['replicate1','replicate2', 'replicate3']
            ):
            
                expeId, expPath = replicate[number][0][exptype].strip().split(',')
        # if it is a missing experiment dont continue with the analisys
                if 'MISSING' in expeId:
                    print(number, expPath, expeId)
                    continue
                for possiblenarrowPeakFolder in narrowPeakLocationFolders:
                    narrowPeakFolder = None
                    path = os.path.join(basePathDataFolder,possiblenarrowPeakFolder,expPath)
        # make a list of the files in each posible directory. Try and continue if the experiment was not 
        # done for the replicate. 
                    try:
                        filesInFolder = os.listdir(path)
                    except FileNotFoundError:
                        continue
        # search for the specific experiment id inside the folder in the names to check if it is the correct folder
        # and stop searching if it is inside

                    for file in filesInFolder:
                        if 'html' in file:
                            fileid=file
    #                 print(fileid)
    #                 print(expeId)
                    if fileid.startswith(expeId):
                        narrowPeakFolder = possiblenarrowPeakFolder
                        break

                narrowpeakFileOriginalPath = os.path.join(
                    basePathDataFolder,narrowPeakFolder,expPath
                )
    #             specificPathsSumary[experiment['condition']][metState].append((narrowPeakFolder,narrowpeakFileOriginalPath))
                specificPathsSumary[experiment['condition']][metState][exptype][number] = narrowpeakFileOriginalPath 

global_start_time = time()
for experiment in specificPathsSumary:
    for metState in specificPathsSumary[experiment]:
        for exptype in specificPathsSumary[experiment][metState]:
            for replicate in specificPathsSumary[experiment][metState][exptype]:
                workingFolder = specificPathsSumary[experiment][metState][exptype][replicate]
                print("*" * 50)
                print(ctime(time()))
                start_time = time()
                performIntersect(workingFolder, commonpeaksfile)
                end_time = time()
                print(ctime(time()))
                print("Duration : ", str(end_time - start_time))
                print("*" * 50)

global_end_time = time()
print("Total Duration : ", str(global_end_time - global_start_time))