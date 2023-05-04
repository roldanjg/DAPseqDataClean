from cdmanager import cd
from pathlib import Path
from utilpipeline import (
    performGEMmultipleReplicateSpecialcase
)
from pathlib import Path


information_case = [
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/E/1/bHLH19E1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/E/2/bHLH19E2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/Input/Input/bHLH19InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH19-E'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/WT/1/bHLH19WT1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/WT/2/bHLH19WT2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/Input/Input/bHLH19InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH19-WT'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/S/1/bHLH19S1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/S/2/bHLH19S2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/Input/Input/bHLH19InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH19-S'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/K/1/bHLH19K1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/K/2/bHLH19K2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/Input/Input/bHLH19InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH19-K'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/F/1/bHLH19F1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/F/2/bHLH19F2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH19/Input/Input/bHLH19InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH19-F'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/WT/1/bHLH25WT1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/WT/2/bHLH25WT2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/Input/Input/bHLH25InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH25-WT'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/G/1/bHLH25G1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/G/2/bHLH25G2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/Input/Input/bHLH25InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH25-G'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/Q/1/bHLH25Q1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/Q/2/bHLH25Q2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/Input/Input/bHLH25InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH25-Q'],
    ['/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/R/1/bHLH25R1sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/R/2/bHLH25R2sorted.bam','/home/joaquin/projects/methylation/data/data_muts_bHLH25_bHLH19/bHLH25/Input/Input/bHLH25InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_gemdoble_muts_bHLH25_bHLH19/bHLH25-R']
]

for information in [information_case]:
    for sample1Path,sample2Path, inputControlpath, outputPaht in information:
        print(sample1Path,sample2Path, inputControlpath, outputPaht)
        Path(outputPaht).mkdir(parents=True, exist_ok=True)
        performGEMmultipleReplicateSpecialcase(sample1Path,sample2Path, inputControlpath, outputPaht)
