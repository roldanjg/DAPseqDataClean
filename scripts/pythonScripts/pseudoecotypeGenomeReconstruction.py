
import os
from pathlib import Path
import subprocess
import pandas as pd
import shutil
from pathlib import Path
import glob
from utilpipeline import (
    performBowtie2,
    getBamAndDeleteSam,
    sortBamFiles,

)

ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_arabidopsis_ecotypes_IP_pseudogenomesget.csv'
working_folder = '/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP'
resultFolder = '/home/joaquin/projects/methylation/data/pseudogenomesAt'
working_folder_name = 'data_arabidopsis_ecotypes_IP'
bowtie2mode = '--sensitive'
peaks = '/home/joaquin/projects/methylation/data/pseudogenomesAt/peaks.fa'


# create bigwig folder
Path(resultFolder).mkdir(parents=True, exist_ok=True)


with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['rawindex', 'tf', 'inputid','replicatenumber'])


for index, attri in idsDf.iterrows():
    inputControlpath = os.path.join(
                    '/home/joaquin/projects/methylation/data', working_folder_name,
                    'Input',str(attri.inputid), 'Input'
                    )
    targetFolder = os.path.join(
        '/home/joaquin/projects/methylation/data', working_folder_name,
        attri.tf, str(attri.inputid),str(attri.replicatenumber)
        )
    resultFolderIP = os.path.join(
        resultFolder,
        attri.tf+str(attri.inputid)
        )
    Path(resultFolderIP).mkdir(parents=True, exist_ok=True)
    
##### performconcat ###########################################
    for val in ['val_1.fq.gz','val_2.fq.gz']:
        inputfq = glob.glob(f'{inputControlpath}/*{val}')
        ipfq = glob.glob(f'{targetFolder}/*{val}')
        outputip = os.path.join(resultFolderIP,f'{attri.tf}{attri.inputid}_{val}')

        concatfilestats = subprocess.run(
                f'cat {inputfq[0]} {ipfq[0]} > {outputip}',
                shell=True, capture_output=True
                )
        concatfilestatsfile = os.path.join(resultFolderIP,'concatfilestats.txt')
        print('Bowtie2 summary: ' + str(concatfilestats.stdout))
        print('Bowtie2 errors if any: ' + str(concatfilestats.stderr))
        with open(concatfilestatsfile, 'a+') as metrics:
            metrics.write(str(concatfilestats))
#############################################################
    samfileexperiment = f'{attri.tf}{str(attri.inputid)}pseudogenome.sam'

    performBowtie2(
        resultFolderIP,
        bowtie2mode,
        samfileexperiment
                    )
    getBamAndDeleteSam(resultFolderIP)
    sortBamFiles(resultFolderIP)

    
##### bcftools mpileup call###########################################

    sortedbam = f'{resultFolderIP}/{attri.tf}{str(attri.inputid)}pseudogenomesorted.bam'
    pseudogenome = peaks
    resultvcf = os.path.join(resultFolderIP,f'{attri.tf}{attri.inputid}.vcf.gz')
    
    mpileup = subprocess.run(
            f'bcftools mpileup --min-MQ 5 -Ou -f {pseudogenome} {sortedbam} | bcftools call --ploidy 1 -Oz -c -v -o {resultvcf}',
            shell=True, capture_output=True
            )
    mpileupstatsfile = os.path.join(resultFolderIP,'mpileupstats.txt')
    print('mpileup summary: ' + str(mpileup.stdout))
    print('mpileup errors if any: ' + str(mpileup.stderr))
    with open(mpileupstatsfile, 'w') as metrics:
        metrics.write(str(mpileup))
#############################################################

##### bcftools consensus ###########################################
  
    pseudogenomeroot = f'{resultFolderIP}/{attri.tf}{str(attri.inputid)}peakpseudogenome.fa'
    consensus = subprocess.run(
            f'bcftools index {resultvcf}',
            shell=True, capture_output=True
            )
    consensus = subprocess.run(
            f'bcftools consensus -f {peaks} {resultvcf} > {pseudogenomeroot}',
            shell=True, capture_output=True
            )
    consensusstatsfile = os.path.join(resultFolderIP,'consensus.txt')
    print('consensus summary: ' + str(consensus.stdout))
    print('consensus errors if any: ' + str(consensus.stderr))
    with open(consensusstatsfile, 'w') as metrics:
        metrics.write(str(consensus))
