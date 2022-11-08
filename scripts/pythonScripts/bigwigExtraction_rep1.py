import pandas as pd
import os

compressedMethylomeDataFrame = pd.read_csv('/home/joaquin/projects/gwasmet/averquepasa.bed', sep='\t', 
                names=[
'chrm','start','end','width',
'strand','V4','context','mets','total','V8',
'annotation','geneChr','geneStart',
'geneEnd','geneLength','geneStrand','geneId','transcriptId','distanceToTSS'
                ],usecols = ['chrm','start','end','strand','context','mets', 'total','annotation'], skiprows=1) #, usecols=['seqnames','start','end','width',
print(compressedMethylomeDataFrame.head)