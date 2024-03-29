import os
import re
from functools import reduce
from os.path import exists, join

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
        print(experimentReplicatesDict)

        experimentNameBase = join(resultsFolder, experiment)
        bigwigReplicatesAnalisys(experimentReplicatesDict, experimentNameBase)

        tsvFileFromMultiBigwigSummary = experimentNameBase + '.tab'
        os.remove(experimentNameBase + '.npz')
        dataframesampdir.append(getTheMeanValueFromBigWigReplicates(tsvFileFromMultiBigwigSummary,metState))

    bedgraphFilePath = os.path.join(resultsFolder,experiment + '.bedgraph')
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['chr','start','end'],
                                                    how='outer'), dataframesampdir).fillna(0)
    df_merged.to_csv(bedgraphFilePath, sep='\t', index=False, header=False)
    bedgraphToBwFromMean(bedgraphFilePath, speciesIndexChrSize)


