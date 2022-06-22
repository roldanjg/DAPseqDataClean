from utilpipeline import (
    bedgraphToBwFromMean,
    bigwigReplicatesAnalisys,
    getTheMeanValueFromBigWigReplicates,
    bedgraphToBwFromMean
)
from os.path import exists
from os.path import join


experimentsToCheck = [
'MYC3amplified26JA',
'MYC3amplified26Mock',
'MYC3amplified26ACC', 
'MYC3amplified224Mock', 
'MYC3amplified224JA',
'MYC3amplified224ACC', 
]

    # 'MYC3direct1Mock',
    # 'MYC3amplified1Mock',
    # 'MYC3direct1JA',
    # 'MYC3amplified1JA',
    # 'MYC3direct1ACC',
    # 'MYC3amplified1ACC',
    # 'MYC3direct6Mock',
    # 'MYC3amplified26Mock',
    # 'MYC3direct6JA',
    # 'MYC3amplified26JA',
    # 'MYC3direct6ACC',
    # 'MYC3amplified26ACC',
    # 'MYC3direct24Mock',
    # 'MYC3amplified224Mock',
    # 'MYC3direct24JA',
    # 'MYC3amplified224JA',
    # 'MYC3direct24ACC',
    # 'MYC3amplified224ACC',
    # 'MYCH7direct1Mock',
    # 'MYCH7amplified1Mock',
    # 'MYCH7direct1JA',
    # 'MYCH7amplified1JA',
    # 'MYCH7direct1ACC',
    # 'MYCH7amplified1ACC',
    # 'MYCH7direct6Mock',
    # 'MYCH7amplified6Mock',
    # 'MYCH7direct6JA',
    # 'MYCH7amplified6JA',
    # 'MYCH7direct6ACC',
    # 'MYCH7amplified6ACC',
    # 'MYCH7direct24Mock',
    # 'MYCH7amplified24Mock',
    # 'MYCH7direct24JA',
    # 'MYCH7amplified24JA',
    # 'MYCH7direct24ACC',
    # 'MYCH7amplified24ACC',

replicates = [
    '/home/joaquin/projects/methylation/data/bigwigs/replicate1',
    '/home/joaquin/projects/methylation/data/bigwigs/replicate2',
    '/home/joaquin/projects/methylation/data/bigwigs/replicate3'
]

resultsFolder = '/home/joaquin/projects/methylation/data/bigwigs/summaryMultipleRep/methylationExperiments'
speciesIndexChrSize = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/genome.index.txt'


for experiment in experimentsToCheck:
    print(experiment)
    experimentReplicatesDict = {}
    for replicate in replicates:
        replicatePath = join(replicate, experiment+'coverage.bw')
        if exists(replicatePath):
            experimentReplicatesDict[replicate.split('/')[-1]] = replicatePath
        elif '2' in experiment:
            try:
                experiment = experiment.replace('amplified2', 'amplified')
                replicatePath = join(replicate, experiment+'coverage.bw')
                if exists(replicatePath):
                    experimentReplicatesDict[replicate.split('/')[-1]] = replicatePath
            except:
                print('THERE IS A PROBLEM', experiment)

    experimentNameBase = join(resultsFolder, experiment)
    bigwigReplicatesAnalisys(experimentReplicatesDict, experimentNameBase)

    tsvFileFromMultiBigwigSummary = experimentNameBase + '.tab'
    getTheMeanValueFromBigWigReplicates(tsvFileFromMultiBigwigSummary)

    bedgraphFilePath = experimentNameBase + '.bedgraph'
    bedgraphToBwFromMean(bedgraphFilePath, speciesIndexChrSize)


