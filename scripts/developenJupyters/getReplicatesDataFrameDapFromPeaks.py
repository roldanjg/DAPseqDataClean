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


def generateReplicatesOrder():
    commonpeaksfile = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/allThePossiblePeaksnine.bed'

    metadata = '/home/joaquin/projects/methylation/data/commonData/ids_data_allReplicates_methylation.json'
    basePathDataFolder = '/home/joaquin/projects/methylation/data'
    narrowPeakLocationFolders = ['tfs_rep_1','tfs_rep_3_input_from_rep_2', 'tfs_rep_2', 'tfs_rep_4']
    specificPathsSumary = {}


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
    return specificPathsSumary


def generateDfandNormaliceDataTPMs(folder,dataColName):
    csvFile = glob.glob(f'{folder}/allThePossiblePeaksnine*.csv')
    
    if len(csvFile) != 1:
        return print(folder, ' has a problem selecting File')
    else:
        csvFilePath = csvFile[0]

    fileDf = pd.read_csv(csvFilePath,header=0, names=['chr','star','end','id',dataColName])
    totalReads = fileDf[dataColName].sum()

    scalingFactor = totalReads/1000000

    fileDf[dataColName] = fileDf[dataColName].apply(lambda x: x/scalingFactor)

    return fileDf

# reduce new function https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
def generateMeanReplicatesDf(tf, specificPathsSumary):
    allNormalizedreplicates = []
    for experiment in specificPathsSumary:
        if tf in experiment:
            for metState in specificPathsSumary[experiment]:
                for exptype in specificPathsSumary[experiment][metState]:
                    listofdfs = []
                    datacolnames = []
                    for replicate in specificPathsSumary[experiment][metState][exptype]:
                        workingFolder = specificPathsSumary[experiment][metState][exptype][replicate]
                        datacolname = '{}{}{}{}'.format(experiment,metState,exptype,replicate)
                        listofdfs.append(generateDfandNormaliceDataTPMs(workingFolder,datacolname))
                        datacolnames.append(datacolname)
        #             los valores que no estan en una de las replicas los completo con un 0
                    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['chr','star','end','id'],
                                                    how='outer'), listofdfs).fillna(0)
    #                 print(df_merged)
                    mean_col_name = '{}{}{}'.format(experiment,metState,exptype)
                    df_merged[mean_col_name] = df_merged[datacolnames].mean(axis=1)
                    df_merged = df_merged.drop(columns=datacolnames)
                    if not 'input' in mean_col_name:
                        allNormalizedreplicates.append(df_merged)

    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['chr','star','end','id'],
                                                    how='outer'), allNormalizedreplicates).fillna(0)
    return df_merged


