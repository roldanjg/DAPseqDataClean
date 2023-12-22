import os
import re
from functools import reduce
import subprocess
from os.path import exists, join

import pandas as pd
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
from scipy import stats
import itertools
import numpy as np

def performPearsonCorr(datasetone,datasettwo):
    return stats.pearsonr(datasetone,datasettwo)

files_folder = '/home/joaquin/projects/methylation/data/bigwigs/data_dap_on_atac_1'

replicates_order_dict = {
    'MEAN_MOCK_1':['MYC2M11coverage.bw','MYC2M12coverage.bw','MYC2M13coverage.bw'],
    'MEAN_JA_1_MYC2':['MYC2JA11coverage.bw','MYC2JA13coverage.bw'],
    'MEAN_MOCK_3_MYC2':['MYC2M31coverage.bw','MYC2M32coverage.bw','MYC2M33coverage.bw'],
    'MEAN_JA_3_MYC2':['MYC2JA31coverage.bw','MYC2JA32coverage.bw','MYC2JA33coverage.bw']
}

speciesIndexChrSize = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/genome.index.txt'

with open('datacorrgoodTPM100K.tsv', 'w') as datacorr:
    for experiment in replicates_order_dict:
        experimentNameBase = os.path.join(files_folder,experiment)
        experiments_paths = [os.path.join(files_folder,case) for case in replicates_order_dict[experiment]]
        # subprocess.run(
        #         'multiBigwigSummary bins -bs 10 -b ' + ' '.join(experiments_paths) + '  --labels ' + ' '.join(replicates_order_dict[experiment]) +
        #         ' -p 40 -o '+ experimentNameBase + '.npz' +' --outRawCounts ' + experimentNameBase + '.tab',
        #         shell=True
        #     )
        tsvFileFromMultiBigwigSummary = experimentNameBase + '.tab'
        # os.remove(experimentNameBase + '.npz')

        with open(tsvFileFromMultiBigwigSummary) as f:
            first_line = f.readline()
        lineDiferenPartListRaw =first_line.strip().split('\t')[3:]


        lineBasePartList = ['chr','start','end']
        lineDiferenPartList = [rep[1:-1] for rep in lineDiferenPartListRaw]
        lineBasePartList.extend(lineDiferenPartList)

        meansummaryDf = pd.read_csv(tsvFileFromMultiBigwigSummary, sep='\t', header=0, names=lineBasePartList, dtype={'chr':str})
        meansummaryDf.drop(meansummaryDf[(meansummaryDf.chr == 'Mt') | (meansummaryDf.chr == 'Pt')].index, inplace=True)
        listOfSubsets = []
        listOfSubsets.append(experiment)
        for subset in itertools.combinations(lineDiferenPartList, 2):
            corr, _ = performPearsonCorr(np.array(meansummaryDf[subset[0]]), np.array(meansummaryDf[subset[1]]))
            listOfSubsets.append(f'{subset[0]}_vs_{subset[1]}:'+str(corr))
        datacorr.write('{}\n'.format('\t'.join(listOfSubsets)))

        # meansummaryDf[experiment] = meansummaryDf[lineDiferenPartList].mean(axis=1)
        # meansummaryDf.drop(columns=lineDiferenPartList, inplace=True)
        # meansummaryDf['chr'] = pd.to_numeric(meansummaryDf['chr'])
        # meansummaryDf = meansummaryDf.sort_values(['chr','start'])
        # meansummaryDf.to_csv(tsvFileFromMultiBigwigSummary[:-4] + '.bedgraph', sep='\t', index=False, header=False)
        # bedgraphFilePath = os.path.join(tsvFileFromMultiBigwigSummary[:-4] + '.bedgraph')
        # subprocess.run('bedGraphToBigWig ' + bedgraphFilePath + ' ' + speciesIndexChrSize + ' ' + bedgraphFilePath[:-8]+'bw',
        #         shell=True)



