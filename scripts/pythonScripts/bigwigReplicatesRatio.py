import os
import re
from functools import reduce
from os.path import exists, join
import numpy as np
import pandas as pd

from utilpipeline import (bedgraphToBwFromMean, bigwigReplicatesAnalisys,
                          generateReplicatesOrder,
                          getTheMeanValueFromBigWigReplicates)

experimentsToCheck = generateReplicatesOrder('.bw')
resultsFolder = '/home/joaquin/projects/methylation/data/bigwigs/summaryMultipleRep/methylationExperiments'
speciesIndexChrSize = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/genome.index.txt'


for experiment in experimentsToCheck:
    dataframesampdir = []
    for metState in experimentsToCheck[experiment]:
        experimentReplicatesDict = experimentsToCheck[experiment][metState]['sample']
        print(experimentReplicatesDict, experiment,metState)

        experimentNameBase = join(resultsFolder, experiment+metState)
        bigwigReplicatesAnalisys(experimentReplicatesDict, experimentNameBase)

        tsvFileFromMultiBigwigSummary = experimentNameBase + '.tab'
        os.remove(experimentNameBase + '.npz')
        dataframesampdir.append(getTheMeanValueFromBigWigReplicates(tsvFileFromMultiBigwigSummary,metState))

    bedgraphFilePath = os.path.join(resultsFolder,experiment + '.bedgraph')
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['chr','start','end'],
                                                    how='outer'), dataframesampdir).fillna(0)
    
    df_merged['ratio'] = df_merged['direct']/df_merged['amplified']
    df_merged.replace([np.inf, -np.inf], 0, inplace=True)
    df_merged.fillna(0, inplace=True)
    
    df_merged = df_merged.drop(columns=['direct','amplified'])
    df_merged.to_csv(bedgraphFilePath, sep='\t', index=False, header=False)
    bedgraphToBwFromMean(bedgraphFilePath, speciesIndexChrSize)
    