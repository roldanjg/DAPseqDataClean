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
        experimentNameBase = join(resultsFolder, experiment+metState)

        bedgraphFilePath = os.path.join(experimentNameBase + '.bedgraph')
   
        bedgraphToBwFromMean(bedgraphFilePath, speciesIndexChrSize)
    