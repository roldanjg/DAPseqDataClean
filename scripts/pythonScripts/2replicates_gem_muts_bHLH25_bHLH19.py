from cdmanager import cd
from pathlib import Path
from utilpipeline import (
    performGEMmultipleReplicateSpecialcase
)
from pathlib import Path


information_case = [
    ['/home/joaquin/projects/methylation/data/data_potato_salome_2/ABL1/1/ABL11sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/ABL1/2/ABL12sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/Input/Input/InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2_dobles/ABL1'],
    ['/home/joaquin/projects/methylation/data/data_potato_salome_2/AREB2/1/AREB21sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/AREB2/2/AREB22sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/Input/Input/InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2_dobles/AREB2'],
    ['/home/joaquin/projects/methylation/data/data_potato_salome_2/FDL1a/1/FDL1a1sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/FDL1a/2/FDL1a2sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/Input/Input/InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2_dobles/FDL1a'],
    ['/home/joaquin/projects/methylation/data/data_potato_salome_2/FDL1c/1/FDL1c1sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/FDL1c/2/FDL1c2sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/Input/Input/InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2_dobles/FDL1c'],
    ['/home/joaquin/projects/methylation/data/data_potato_salome_2/TOC1a/1/TOC1a1sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/TOC1a/2/TOC1a2sorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2/Input/Input/InputInputsorted.bam','/home/joaquin/projects/methylation/data/data_potato_salome_2_dobles/TOC1a']
]

for information in [information_case]:
    for sample1Path,sample2Path, inputControlpath, outputPaht in information:
        print(sample1Path,sample2Path, inputControlpath, outputPaht)
        Path(outputPaht).mkdir(parents=True, exist_ok=True)
        performGEMmultipleReplicateSpecialcase(sample1Path,sample2Path, inputControlpath, outputPaht)
