from ntpath import join
import subprocess
import os
import pandas as pd
import shutil
from pathlib import Path
from cdmanager import cd
import filecmp
import re
import gzip
import csv
import json

from constants import genomeIndex, gemIndex, genomeSizes

def checkMD5isCorrect(folder):
    with cd(folder):
        subprocess.call('md5sum *gz >check.txt', shell=True)
        if filecmp.cmp('MD5.txt', 'check.txt', shallow=False):
            # os.remove("MD5.txt")
            return True
        else:
            print('Files in ' + folder + 'are corrupted by MD5 annalisys')


def checkFastaQLenght(folder):
    with cd(folder):
        totalLinesInGzs = subprocess.run('zcat *gz | wc -l', shell=True, capture_output=True)
        if not totalLinesInGzs.stderr:
            if int(totalLinesInGzs.stdout) % 4 == 0:
                return True
            else:
                print('There is an error running int(onshell.stdout) % 4 == 0 in' + folder)

        else:
            print('There is an error running the command zcat *gz | wc -l in this directory' + folder)


def performTrimGalore(folder):
    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if '1.fq.gz' in file:
                readOne = file
            if '2.fq.gz' in file:
                readTwo = file

        subprocess.run(['trim_galore', '--phred33', '--fastqc', '--suppress_warn',
                        '--cores', '6', '--paired', readOne, readTwo])


def performTrimGaloreFourFilesBisulfite(folder):
    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if '1_1.fq.gz' in file:
                readOneOne = file
            if '1_2.fq.gz' in file:
                readOneTwo = file
            if '4_1.fq.gz' in file:
                readTwoOne = file
            if '4_2.fq.gz' in file:
                readTwoTwo = file

         # every time this subprocess run you should change the adapter to match the one used in sequencing
        subprocess.call('trim_galore --phred33 --fastqc --suppress_warn --cores 4' +
                      ' --clip_R1 10 --clip_R2 10 --stringency 1 ' +
                      '-a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT ' +
                      '-a2 GATCGGAAGAGCACACGTCTGAACTCCAGTCACGGATGACTATCTCGTATGCCGTCTTCTGCTTG ' +
                      '--paired ' + readOneOne + ' ' + readOneTwo, shell=True)
        subprocess.call('trim_galore --phred33 --fastqc --suppress_warn --cores 4' +
                      ' --clip_R1 10 --clip_R2 10 --stringency 1 ' +
                      '-a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT ' +
                      '-a2 GATCGGAAGAGCACACGTCTGAACTCCAGTCACGGATGACTATCTCGTATGCCGTCTTCTGCTTG ' +
                      '--paired ' + readTwoOne + ' ' + readTwoTwo, shell=True)
        # subprocess.run(['trim_galore', '--phred33', '--fastqc', '--suppress_warn',
        #                 '--cores', '4', '--paired', readOneOne, readOneTwo])
        # subprocess.run(['trim_galore', '--phred33', '--fastqc', '--suppress_warn',
        #                 '--cores', '4', '--paired', readTwoOne, readTwoTwo])

       ## every time this subprocess run you should change the adapter to match the one used in sequencing
    #    this are the adapters from replicate one and two
       #subprocess.call('trim_galore --phred33 --fastqc --suppress_warn --cores 2' +
       #                ' --clip_R1 10 --clip_R2 10 --stringency 1 ' +
       #                '-a AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT ' +
       #                '-a2 GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGATCTCGTATGCCGTCTTCTGCTTG ' +
       #                '--paired ' + readOneOne + ' ' + readOneTwo, shell=True)
       #subprocess.call('trim_galore --phred33 --fastqc --suppress_warn --cores 2' +
       #                ' --clip_R1 10 --clip_R2 10 --stringency 1 ' +
       #                '-a AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT ' +
       #                '-a2 GATCGGAAGAGCACACGTCTGAACTCCAGTCACATCACGATCTCGTATGCCGTCTTCTGCTTG ' +
       #                '--paired ' + readTwoOne + ' ' + readTwoTwo, shell=True)



def qualityCheckTrimGaloreFourFiles(folder):
    with cd(folder):
        readOnepass = False
        readTwopass = False
        readTwoTwopass = False
        readOneOnepass = False
        file_names = os.listdir()
        for file in file_names:

            if '1_1_val_1_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readonefolder = file[:-4]
                with open(readonefolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readOnepass = True

            if '1_2_val_2_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readtwofolder = file[:-4]
                with open(readtwofolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readTwopass = True

            if '4_1_val_1_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readonefolder = file[:-4]
                with open(readonefolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readOneOnepass = True

            if '4_2_val_2_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readtwofolder = file[:-4]
                with open(readtwofolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readTwoTwopass = True

        if readOnepass and readTwopass and readTwoTwopass and readOneOnepass:
            return True
        else:
            print('Per base sequence quality did not pass the fastqc test. For read one:' + str(readOnepass) +
                  ' and for read two: ' + str(readTwopass))
            return False

def qualityCheckTrimGalore(folder):
    with cd(folder):
        readOnepass = False
        readTwopass = False
        file_names = os.listdir()
        for file in file_names:

            if 'val_1_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readonefolder = file[:-4]
                with open(readonefolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readOnepass = True

            if 'val_2_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readtwofolder = file[:-4]
                with open(readtwofolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readTwopass = True

        if readOnepass and readTwopass:
            return True
        else:
            print('Per base sequence quality did not pass the fastqc test. For read one:' + str(readOnepass) +
                  ' and for read two: ' + str(readTwopass))
            return False

def performBismark(folder):

    """"Previous to this step you must have run
     bismark_genome_preparation \
     --path_to_aligner /home/joaquin/projects/anaconda3/envs/metilation/bin/ \
      --verbose /home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/at/"""
    bismark = '/home/joaquin/projects/methylation/programs/Bismark-0.22.3/bismark'
    genomeFolder = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/at'


    with cd(folder):
        bis11 = None
        bis12 = None
        bis21 = None
        bis22 = None
        file_names = os.listdir()
        for file in file_names:
            if 'L1_1_val_1.fq.gz' in file:
                bis11 = file
            if 'L1_2_val_2.fq.gz' in file:
                bis12 = file
            if 'L4_1_val_1.fq.gz' in file:
                bis21 = file
            if 'L4_2_val_2.fq.gz' in file:
                bis22 = file
        #  --parallel 6
        subprocess.call(
                bismark + ' --non_directional --genome_folder ' + genomeFolder +
                ' -1 ' + bis11 + ',' + bis21 +
                ' -2 ' + bis12 + ',' + bis22 + ' >totalBismark.txt 2>&1',
                shell=True
                        )

def performBowtie2fourfiles(folder, bowtie2mode, samOutputName):
    """ Before running this function, you must had run bowtie2-build <genome name>.fa genome_index
    in your common files folder and specify here the path to that document"""

    with cd(folder):
        readOneOne = None
        readOneTwo = None
        readTwoOne = None
        readTwoTwo = None
        file_names = os.listdir()
        for file in file_names:
            if 'L2_1_val_1.fq.gz' in file:
                readOneOne = file
            if 'L2_2_val_2.fq.gz' in file:
                readOneTwo = file
            if 'L4_1_val_1.fq.gz' in file:
                readTwoOne = file
            if 'L4_2_val_2.fq.gz' in file:
                readTwoTwo = file

        bowtie2stats = subprocess.run('bowtie2 --phred33 ' + bowtie2mode + ' -t -p 10 -x ' + genomeIndex +
                                      ' -1 ' + readOneOne + ' , ' + readTwoOne +
                                      ' -2 ' + readOneTwo + ' , ' + readTwoTwo +
                                      ' -S ' + samOutputName,
                                      shell=True, capture_output=True)
        print('Bowtie2 summary: ' + str(bowtie2stats.stdout))
        print('Bowtie2 errors if any: ' + str(bowtie2stats.stderr))
        with open('bowtie2stats.txt', 'w') as metrics:
            metrics.write(str(bowtie2stats))


def deduplicateBismark(folder):

    deduplicate = '/home/joaquin/projects/methylation/programs/Bismark-0.22.3/deduplicate_bismark'

    with cd(folder):
        bisDone1 = None
        bisDone2 = None

        file_names = os.listdir()
        for file in file_names:
            if 'L1_1_val_1_bismark_bt2_pe.bam' in file:
                bisDone1 = file
            if 'L4_1_val_1_bismark_bt2_pe.bam' in file:
                bisDone2 = file

        subprocess.call(
            deduplicate + ' --multiple -p --bam ' + bisDone1 + ' ' + bisDone2 + ' >totalDeduplicate.txt 2>&1',
            shell=True
        )


def methylationExtractionBismark(folder):

    methylationExtraction = '/home/joaquin/projects/methylation/programs/Bismark-0.22.3/bismark_methylation_extractor'
    genomeFolder = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/at'

    with cd(folder):
        bisDeduplicated = None
        file_names = os.listdir()
        for file in file_names:
            if 'multiple.deduplicated.bam' in file:
                bisDeduplicated = file

        subprocess.call(
            methylationExtraction +
            ' -p --gzip --parallel 5 --comprehensive --bedGraph --zero_based --CX_context ' +
            '--cytosine_report --genome_folder ' + genomeFolder + ' --zero_based --CX_context '
            + bisDeduplicated + ' >totalMetExtraction.txt 2>&1',
            shell=True
        )

def reportBismark(folder):
    
    reportBismarkpath = '/home/joaquin/projects/methylation/programs/Bismark-0.22.3/bismark2report'
    with cd(folder):
        subprocess.call(
            'mkdir report',
            shell=True
        )
        subprocess.call(
            reportBismarkpath + ' --dir report/',
            shell=True
        )


def performBowtie2(folder, bowtie2mode, samOutputName):
    """ Before running this function, you must had run bowtie2-build <genome name>.fa genome_index
    in your common files folder and specify here the path to that document""" 

    with cd(folder):
        readOne = False
        readTwo = False
        file_names = os.listdir()
        for file in file_names:

            if 'val_1.fq.gz' in file:
                readOne = file

            if 'val_2.fq.gz' in file:
                readTwo = file

        bowtie2stats = subprocess.run(
            'bowtie2 --phred33 ' + bowtie2mode + ' -t -p 30 -x ' + genomeIndex + ' -1 ' +
            readOne + ' -2 ' + readTwo + ' -S ' + samOutputName,
            shell=True, capture_output=True
            )
        print('Bowtie2 summary: ' + str(bowtie2stats.stdout))
        print('Bowtie2 errors if any: ' + str(bowtie2stats.stderr))
        with open('bowtie2stats.txt', 'w') as metrics:
            metrics.write(str(bowtie2stats))


def getBamAndDeleteSam(folder):
    # samtools = '/home/joaquin/projects/webproyect/programs/samtools-1.10/samtools'

    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if '.sam' in file:
                samfile = file
        subprocess.call(['samtools', 'view', '-bh', samfile, '-o', samfile[:-4] + '.bam'])
        os.remove(samfile)


def performGEM(folder, inputControlpath, working_folder_name):  # inputSpecification = f'{id.time}/{id.tratement}'

    """ Before running this function, you must had run
    cat <path_to_genome.fasta> |  awk -v RS=">" '{ print RS $0 > substr($1,1) ".fa"}''
    in your common files folder and specify here the path to that document
    
    WARNING TAKE CARE WITH MULTIPROCESSING IN GEM, GIVES PROBLEMS (LUIS ORDUÑA SAID) WITH MULTIPLOCESSING
    """

    
    GEM = '/home/joaquin/projects/methylation/programs/gem/gem.jar'
    Read_Distribution_default = '/home/joaquin/projects/methylation/programs/gem/Read_Distribution_default.txt'
    #inputControlpath = os.path.join(
    #    '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/amplified', inputSpecification
    #)
    outputFolder = os.path.join('/home/joaquin/projects/methylation/data', working_folder_name, folder, 'GEMout')

    with cd(inputControlpath):
        file_names = os.listdir()
        for file in file_names:
            if file.endswith('orted.bam'):
                inputControl = os.path.join(inputControlpath, file)

    with cd(folder):
        Path(outputFolder).mkdir(parents=True, exist_ok=True)
        bamfile = False
        file_names = os.listdir()
        for file in file_names:

            if file.endswith('orted.bam'):
                bamfile = file

        subprocess.call(
                ['java', '-jar', GEM, '--d', Read_Distribution_default,
                 '--g', genomeSizes, '--genome', gemIndex, '--s', '150000000',
                 '--expt', bamfile, '--ctrl', inputControl,
                 '--out', outputFolder, '--f', 'SAM', '--outNP', '--excluded_fraction', '0', '--range', '200',
                 '--smooth', '0', '--mrc', '1', '--fold', '2', '--q', '1.301029996',
                 '--k_min', '6', '--k_max', '20', '--k_seqs', '600', '--k_neg_dinu_shuffle',
                 '--pp_nmotifs', '1', '--t', '1'],
                 stdout=subprocess.DEVNULL,
                 stderr=subprocess.STDOUT
            )

def performGEMfree(samplePath, inputControlpath, outputPaht):  # inputSpecification = f'{id.time}/{id.tratement}'

    """ Before running this function, you must had run
    cat <path_to_genome.fasta> |  awk -v RS=">" '{ print RS $0 > substr($1,1) ".fa"}''
    in your common files folder and specify here the path to that document"""

    
    GEM = '/home/joaquin/projects/methylation/programs/gem/gem.jar'
    Read_Distribution_default = '/home/joaquin/projects/methylation/programs/gem/Read_Distribution_default.txt'
    #inputControlpath = os.path.join(
    #    '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/amplified', inputSpecification
    #)
    subprocess.call(
            ['java', '-jar', GEM, '--d', Read_Distribution_default,
                '--g', genomeSizes, '--genome', gemIndex, '--s', '150000000',
                '--expt', samplePath, '--ctrl', inputControlpath,
                '--out', outputPaht, '--f', 'SAM', '--outNP', '--excluded_fraction', '0', '--range', '200',
                '--smooth', '0', '--mrc', '1', '--fold', '2', '--q', '1.301029996',
                '--k_min', '6', '--k_max', '20', '--k_seqs', '600', '--k_neg_dinu_shuffle',
                '--pp_nmotifs', '1', '--t', '1'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
        )

def performGEMmultipleReplicate(folder, inputControlpath, working_folder_name):  # inputSpecification = f'{id.time}/{id.tratement}'

    """ Before running this function, you must had run
    cat <path_to_genome.fasta> |  awk -v RS=">" '{ print RS $0 > substr($1,1) ".fa"}''
    in your common files folder and specify here the path to that document"""

    
    GEM = '/home/joaquin/projects/methylation/programs/gem/gem.jar'
    Read_Distribution_default = '/home/joaquin/projects/methylation/programs/gem/Read_Distribution_default.txt'
    #inputControlpath = os.path.join(
    #    '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/amplified', inputSpecification
    #)
    outputFolder = os.path.join('/home/joaquin/projects/methylation/data', working_folder_name, folder, 'GEMout')

    with cd(inputControlpath):
        file_names = os.listdir()
        for file in file_names:
            if file.endswith('orted.bam'):
                inputControl = os.path.join(inputControlpath, file)

    with cd(folder):
        Path(outputFolder).mkdir(parents=True, exist_ok=True)
        bamfile = False
        file_names = os.listdir()
        for file in file_names:

            if file.endswith('orted.bam'):
                bamfile = file

        # subprocess.call(
        #         ['java', '-jar', GEM, '--d', Read_Distribution_default,
        #          '--g', genomeSizes, '--genome', gemIndex, '--s', '150000000',
        #          '--expt1', bamfileOne, '--expt2', bamfileTwo, '--ctrl1', inputControlOne, '--ctrl2', inputControlTwo,
        #          '--out', outputFolder, '--f', 'SAM', '--outNP', '--excluded_fraction', '0', '--range', '200',
        #          '--smooth', '0', '--mrc', '1', '--fold', '2', '--q', '1.301029996',
        #          '--k_min', '6', '--k_max', '20', '--k_seqs', '600', '--k_neg_dinu_shuffle',
        #          '--pp_nmotifs', '1', '--t', '1'],
        #          stdout=subprocess.DEVNULL,
        #          stderr=subprocess.STDOUT
        #     )
            


def sortBamFiles(folder):
    with cd(folder):
        # samtools = '/home/joaquin/projects/webproyect/programs/samtools-1.10/samtools'
        file_names = os.listdir()
        for file in file_names:
            if '.bam' in file:
                bamfile = file
        subprocess.call('samtools' + ' sort -l 9 -m 4GiB -o ' + bamfile[:-4] + 'sorted.bam -O bam -@40 ' + bamfile,
                        shell=True
                        )


def performIntersect(folder, ExperimentTarget):

    """ as the program dont allow to obtain the results in a summary of total hits per box analyced, we do it """

    with cd(folder):
        # samtools = '/home/joaquin/projects/webproyect/programs/samtools-1.10/samtools'
        # bedtools = '/home/joaquin/projects/webproyect/programs/bedtools2/bedtools'
        if ExperimentTarget == 'MYCs':
            boxpath = {
                'Gbox': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/G_box.bed',
                'PBE': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/PBE_box.bed',
                'TG': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/TG_box.bed',
            }
            
        elif ExperimentTarget == 'ERFs':
            boxpath = {
                'GAC': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/GAC_box.bed',
                'GCC': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/GCC_box.bed',
            }
        elif ExperimentTarget == 'Inputs':
            boxpath = {
                'Gbox': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/G_box.bed',
                'PBE': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/PBE_box.bed',
                'TG': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/TG_box.bed',
                'GAC': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/GAC_box.bed',
                'GCC': '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/GCC_box.bed',
            }
        file_names = os.listdir()
        for file in file_names:
            if file.endswith('orted.bam'):
                bamsorted = file
        for boxfile in boxpath:
            # firs we check if its already done, to skipt the generation process
            if not os.path.isfile(boxfile + '_' + bamsorted[:-10] + '.bed'):
                
                subprocess.call(
                    'samtools' + ' view -q1 -b ' + bamsorted + ' | ' +
                    'bedtools' + ' intersect -abam stdin -b ' + boxpath[boxfile] + ' -bed -wb ' +
                    '> ' + boxfile + '_' + bamsorted[:-10] + '.bed', shell=True
                )
            else:
                print(boxfile + '_' + bamsorted[:-10] + '.bed is already done')
            # this part of the scrip is always done
            totalForBox = {}
            with open(boxfile + '_' + bamsorted[:-10] + '.bed', 'r') as intersectOut:
                intersectDf = pd.read_csv(
                    intersectOut, sep='\t', usecols=[3, 12, 13, 14, 15],
                    names=['intersected', 'chr', 'start', 'end', 'boxname'],
                )
            for index, ip in intersectDf.iterrows():
                intersectOcurrence = str(ip.intersected.split('/')[0])
                box = ','.join([str(ip.chr), str(ip.start), str(ip.end), ip.boxname])
                if box in totalForBox:
                    totalForBox[box].add(intersectOcurrence)
                else:
                    totalForBox[box] = {intersectOcurrence}

            for box in totalForBox:
                boxlen = len(totalForBox[box])
                totalForBox[box] = boxlen

            with open(boxfile + '_' + bamsorted[:-10] + '_boxtotals.csv', 'w') as elcsv:
                elcsv.write('chr,start,end,boxname,{}\n'.format(bamsorted[:-10]))
                for name, recount in totalForBox.items():
                    elcsv.write('{},{}\n'.format(name, recount))


def manageFolderLocationIntersects(destinationFolder, originFolder):
    with cd(originFolder):
        file_names = os.listdir()
    for file in file_names:
        if '_boxtotals.csv' in file:
            print(file)
            originalFile = os.path.join(originFolder, file)
            shutil.copy(originalFile, destinationFolder)


def renameGemFolders(working_folder,destination_folder):
    with cd(working_folder):
        for root, dirs, files in os.walk('./'):
            #print(dirs)
            if 'GEMout' in dirs:
                namedir = str(root.replace('./', ''))
                originalfolder = os.path.join(
                    namedir,
                    'GEMout'
                )
                finalFolder = os.path.join(
                    destination_folder,
                    str(root).replace('/', '').replace('.', '')+'GEMout'
                )
                print(originalfolder, finalFolder)
                shutil.copytree(originalfolder, finalFolder)


def performIntersectLoops(folder):
    with cd(folder):
        boxpath = {
                'TAIRdoublets':'/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/TAIRdoublets.bed',
                'AllPeaks250bp':'/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/AllPeaks250bp.bed',
                
            }
        
        # TODO THIS WAS THE ORIGINAL FOR COVERAGE COMPUTATION LOOPS
        # boxpath = {
        #         'Gbox':'/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/G_box.bed',
        #         'PBE':'/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/PBE_box.bed',
        #         'G_PBE':'/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/G_PBE_box.bed',
        #     }

        file_names = os.listdir()
        for file in file_names:
            if file.endswith('orted.bam'):
                bamsorted = file
        for boxfile in boxpath:
            # firs we check if its already done, to skipt the generation process
            if not os.path.isfile(boxfile + '_' + bamsorted[:-10] + '.bed'):
                
                subprocess.call(
                    'samtools' + ' view -q1 -b ' + bamsorted + ' | ' +
                    'bedtools' + ' intersect -abam stdin -b ' + boxpath[boxfile] + ' -bed -wb ' +
                    '> ' + boxfile + '_' + bamsorted[:-10] + '.bed', shell=True
                )
            # this part of the scrip is always done
            totalForBox = {}
            with open(boxfile + '_' + bamsorted[:-10] + '.bed', 'r') as intersectOut:
                intersectDf = pd.read_csv(
                    intersectOut, sep='\t', usecols=[3, 12, 13, 14, 15],
                    names=['intersected', 'chr', 'start', 'end', 'boxname'],
                )
            for index, ip in intersectDf.iterrows():
                intersectOcurrence = str(ip.intersected.split('/')[0])
                box = ','.join([str(ip.chr), str(ip.start), str(ip.end), ip.boxname])
                if box in totalForBox:
                    totalForBox[box].add(intersectOcurrence)
                else:
                    totalForBox[box] = {intersectOcurrence}

            for box in totalForBox:
                boxlen = len(totalForBox[box])
                totalForBox[box] = boxlen

            with open(boxfile + '_' + bamsorted[:-10] + '_boxtotals.csv', 'w') as elcsv:
                elcsv.write('chr,start,end,boxname,{}\n'.format(bamsorted[:-10]))
                for name, recount in totalForBox.items():
                    elcsv.write('{},{}\n'.format(name, recount))


def mergeResultsAmplifiedDirect(folder, ExperimentTarget):
    with cd(folder):
        if ExperimentTarget == 'MYCs':
            boxpath = {'Gbox', 'PBE', 'TG'}
        elif ExperimentTarget == 'ERFs':
            boxpath = {'GAC', 'GCC'}
        elif ExperimentTarget == 'Inputs':
            boxpath = {'Gbox', 'PBE', 'TG', 'GAC', 'GCC'}
        file_names = os.listdir()
        for box in boxpath:
            boxfiles = []
            for file in file_names:
                if box in file:
                    if '_merged_intersect.csv' not in file:
                        boxfiles.append(file)

            if box + '_merged_intersect.csv' in file_names:
                experiment1df = pd.read_csv(box + '_merged_intersect.csv')
                experiment2df = pd.read_csv(boxfiles[0])
                mergedDf = experiment1df.merge(experiment2df, on=['chr', 'start', 'end', 'boxname'], how='outer')
                mergedDf.to_csv(box + '_merged_intersect.csv', index=False)
                os.remove(boxfiles[0])
            elif len(boxfiles) == 2:
                experiment1df = pd.read_csv(boxfiles[0])
                experiment2df = pd.read_csv(boxfiles[1])
                mergedDf = experiment2df.merge(experiment1df, on=['chr', 'start', 'end', 'boxname'], how='outer')
                mergedDf.to_csv(box + '_merged_intersect.csv', index=False)
                os.remove(boxfiles[0])
                os.remove(boxfiles[1])

def mergeResultsloop(folder):
    with cd(folder):
        boxpath = {'TAIRdoublets', 'AllPeaks250bp'}
        # TODO THIS WAS THE ORIGINAL FOR COVERAGE COMPUTATION LOOPS boxpath = {'Gbox', 'PBE', 'G_PBE'}
        file_names = os.listdir()
        for box in boxpath:
            boxfiles = []
            for file in file_names:
                if file.startswith(box):
                    if '_merged_intersect.csv' not in file:
                        boxfiles.append(file)

            if box + '_merged_intersect.csv' in file_names:
                experiment1df = pd.read_csv(box + '_merged_intersect.csv')
                experiment2df = pd.read_csv(boxfiles[0])
                mergedDf = experiment1df.merge(experiment2df, on=['chr', 'start', 'end', 'boxname'], how='outer')
                mergedDf.to_csv(box + '_merged_intersect.csv', index=False)
                os.remove(boxfiles[0])
            elif len(boxfiles) == 2:
                experiment1df = pd.read_csv(boxfiles[0])
                experiment2df = pd.read_csv(boxfiles[1])
                mergedDf = experiment1df.merge(experiment2df, on=['chr', 'start', 'end', 'boxname'], how='outer')
                mergedDf.to_csv(box + '_merged_intersect.csv', index=False)
                os.remove(boxfiles[0])
                os.remove(boxfiles[1])

def extractBoxRegionAndMetType(folder,headname):
    destination = '/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2/reports/'
    with cd(folder):
        file_names = os.listdir()
        print() 
        csPosibilities = ['CG', 'CHG', 'CHH']
        for file in file_names:
            if '_box.mets.tsv' in file:
                bxdf = pd.read_csv(
                    file,
                    sep='\t', 
                    names=['chr', 'position', 'strand', 'mets', 'nomets', 'context', 'boxID', 'side'],
                    usecols=['chr', 'position', 'strand', 'boxID','mets', 'nomets', 'context', 'side']
                        )
                for cContext in csPosibilities:
                    bxdfCX = bxdf[(bxdf['context'] == cContext)]
                    filesidename = '{}.{}.{}.{}.tsv'.format(file[:-4],headname,'motifSide', cContext)
                    bxdfCX.to_csv(
                        filesidename, 
                        columns=['chr', 'position', 'strand', 'boxID','mets', 'nomets'],
                        index=False, 
                        header=['chr', 'position', 'strand','boxID','mets{}'.format(filesidename[:-4]), 'nomets{}'.format(filesidename[:-4])]
                        )
                    originalFile = os.path.join(folder, filesidename)
                    shutil.move(filesidename, destination)
                    bxdfCX = bxdfCX[bxdfCX['side'] == 'box']
                    filesidename = '{}.{}.{}.{}.tsv'.format(file[:-4],headname,'motif', cContext)
                    bxdfCX.to_csv(
                        filesidename,
                        columns=['chr', 'position', 'strand','boxID','mets', 'nomets'],
                        index=False, 
                        header=['chr', 'position', 'strand','boxID','mets{}'.format(filesidename[:-4]), 'nomets{}'.format(filesidename[:-4])]
                        )
                    # originalFile = os.path.join(folder, filesidename)
                    shutil.move(filesidename, destination)

def mergeResultsMets(folder):
    with cd('/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2/reports/'):
        file_names = os.listdir()
        for rep in ['rep1', 'rep2']:
            for side in ['.motif.', 'motifSide']:
                for metcontex in ['CG', 'CHG', 'CHH']:
                    for box in ['G_box', 'GAC_box', 'PBE_box', 'GCC_box', 'TG_box']:
                        boxfiles = []
                        for file in file_names:
                            # print(file_names)
                            # print('hello')
                            if rep in file and side in file and metcontex in file and file.startswith(box):
                                # print('hello')
                                if '_merged_intersect.csv' not in file:
                                    boxfiles.append(file)
                        # print(boxfiles)
                        
                        if box + rep + side + metcontex + '_merged_intersect.csv' in file_names:
                            experiment1df = pd.read_csv(box + rep + side + metcontex + '_merged_intersect.csv')
                            experiment2df = pd.read_csv(boxfiles[0])
                            mergedDf = experiment1df.merge(experiment2df, on=['chr', 'position', 'strand','boxID'], how='outer')
                            mergedDf.to_csv(box + rep + side + metcontex + '_merged_intersect.csv', index=False)
                            os.remove(boxfiles[0])
                        elif len(boxfiles) == 2:
                            # print('hello')
                            experiment1df = pd.read_csv(boxfiles[0])
                            experiment2df = pd.read_csv(boxfiles[1])
                            # print(experiment1df)
                            mergedDf = experiment1df.merge(experiment2df, on=['chr', 'position', 'strand','boxID'], how='outer')
                            mergedDf.to_csv(box + rep + side + metcontex + '_merged_intersect.csv', index=False)
                            os.remove(boxfiles[0])
                            os.remove(boxfiles[1])



def performBigWigextraction(folder):
    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if file.endswith('orted.bam'):
                # samsorted = file
                bamsorted = file
                bigw = str(bamsorted[:-10]) + 'coverage.bw'

        subprocess.call('samtools index ' + bamsorted, shell=True)
        subprocess.call('bamCoverage -b ' + bamsorted +
                        ' -o ' + bigw + 
                        '--normalizeUsing BPM --binSize 10 --numberOfProcessors 40', shell=True)

def performBedGraphextraction(folder):
    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if file.endswith('orted.bam'):
                # samsorted = file
                bamsorted = file
                bigw = str(bamsorted[:-10]) + 'coverage.bedgraph'
        # subprocess.call('samtools index ' + bamsorted, shell=True)
        subprocess.call('bamCoverage -b ' + bamsorted +
                        ' -o ' + bigw + 
                        ' -of bedgraph --normalizeUsing BPM --binSize 10 --numberOfProcessors 40', shell=True)

def renameAndMoveBigWig(targetFolder,bigWigFolder):
    with cd(targetFolder):
        file_names = os.listdir()
        for file in file_names:
            if 'coverage.bw' in file:
                bigw = file
                originalfolder = os.path.join(
                    targetFolder, bigw
                )
                print(originalfolder, bigWigFolder)
                shutil.copy2(bigw, bigWigFolder)


def calculationGemSummary(folder):
    with cd(folder):

        significant = None

        try:
            with open('GEM_Log.txt', 'r') as logGem:
                for line in logGem:
                    # if '_IP' in line:
                    #    print(line)
                    # if '_CTRL' in line:
                    #    print(line)
                    if 'Significant:' in line:
                        print(line)
                        significant = int(line.split('\t')[1])
                    # if 'Insignificant:' in line:
                    #    ins = line
                    # if 'Filtered:' in line:
                    #    fil = line
            if significant == None:
                return 'No significant Peaks'
            return significant
        except:
            print('no gem done')
filename = '/home/joaquin/projects/methylation/data/data_medicago/Input/Medicago/bowtie2stats.txt'

def calculationBowtieSummary(filepath):
    filename = os.path.join(filepath,'bowtie2stats.txt')
    with open(filename, 'r') as bowstats:
        for line in bowstats:
            reads = re.search(r'([\d]+) reads; of these:',line)
            regular = re.search(r'([\d,\.]+)% overall alignment rate',line)

        return reads.group(1),regular.group(1)

def mapMethytilatedCitosine(folder):

    intersection_path = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/'

    with cd(folder):
        current_folder = os.listdir()
        for file in current_folder:
            if 'CX_report.txt.gz' in file:
                metfile = file

        chrs_data = {}
        with gzip.open(metfile, 'rt') as f:
            for line in f:
                chr_index = line.split('\t')[0]
                coordinate_index = int(line.split('\t')[1])
                try:
                    chrs_data[chr_index][coordinate_index] = line[:-5]
                except:
                    chrs_data[chr_index] = {coordinate_index:line[:-5]}

        file_names = os.listdir(intersection_path)

        for file in file_names:
            with open(intersection_path + file) as f:
                reader = csv.reader(f, delimiter='\t')
                data = list(reader)

            with open(file[:-3] + 'mets.tsv', 'a+') as whateverBox:
                for each_box in data:
                    box_areas = {}
                    box_start = int(each_box[1])
                    box_end = int(each_box[2])
                    chr_location = each_box[0]
                    sequence_identifier = each_box[3]
                    # tenemos que aplicar rango desde una posicion inicial porque es un archivo 0 based, si fuese 1 based el rango estaría mal y tendria que restarle
                    # uno al archivo al box start
                    box_areas['box'] = list(range(box_start, box_end))
                    box_areas['box_right'] = list(range(box_start - 7, box_start))
                    box_areas['box_left'] = list(range(box_end, box_end + 7))

                    for boxarea in box_areas:
                        for coordinate in box_areas[boxarea]:
                            matchline = chrs_data[chr_location].get(coordinate, False)
                            if matchline:
                                whateverBox.write('{}\t{}\t{}\n'.format(matchline, sequence_identifier, boxarea))


def bigwigReplicatesAnalisys(experimentDic, experimentNameBase):
    print(' '.join(experimentDic.values()))
    subprocess.call(
            'multiBigwigSummary bins -bs 10 -b ' + ' '.join(experimentDic.values()) + '  --labels ' + ' '.join(experimentDic.keys()) +
            ' -p 40 -o '+ experimentNameBase + '.npz' +' --outRawCounts ' + experimentNameBase + '.tab',
            shell=True
        )
    
def getTheMeanValueFromBigWigReplicates(tsvFromMultiBigwigSummary, metstate):

    with open(tsvFromMultiBigwigSummary) as f:
        first_line = f.readline()
    lineDiferenPartListRaw =first_line.strip().split('\t')[3:]


    lineBasePartList = ['chr','start','end']
    lineDiferenPartList = [rep[1:-1] for rep in lineDiferenPartListRaw]
    lineBasePartList.extend(lineDiferenPartList)

    meansummaryDf = pd.read_csv(tsvFromMultiBigwigSummary, sep='\t', header=0, names=lineBasePartList, dtype={'chr':str})
    meansummaryDf.drop(meansummaryDf[(meansummaryDf.chr == 'Mt') | (meansummaryDf.chr == 'Pt')].index, inplace=True)
    meansummaryDf[metstate] = meansummaryDf[lineDiferenPartList].mean(axis=1)
    meansummaryDf.drop(columns=lineDiferenPartList, inplace=True)
    meansummaryDf['chr'] = pd.to_numeric(meansummaryDf['chr'])
    meansummaryDf = meansummaryDf.sort_values(['chr','start'])
    meansummaryDf.to_csv(tsvFromMultiBigwigSummary[:-4] + '.bedgraph', sep='\t', index=False, header=False)
    return meansummaryDf

def bedgraphToBwFromMean(bedgraphFilePath, speciesIndexChrSize):
    subprocess.call('bedGraphToBigWig ' + bedgraphFilePath + ' ' + speciesIndexChrSize + ' ' + bedgraphFilePath[:-8]+'bw',
            shell=True)


def generateReplicatesOrder(pattern):

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
                        bw = "None"
                        for file in filesInFolder:
                            if 'html' in file:
                                fileid=file
                            elif pattern in file:
                                bw = file
        #                 print(fileid)
        #                 print(expeId)
                        if fileid.startswith(expeId):
                            narrowPeakFolder = possiblenarrowPeakFolder
                            break

                    narrowpeakFileOriginalPath = os.path.join(
                        basePathDataFolder,narrowPeakFolder,expPath,bw
                    )
        #             specificPathsSumary[experiment['condition']][metState].append((narrowPeakFolder,narrowpeakFileOriginalPath))
                    specificPathsSumary[experiment['condition']][metState][exptype][number] = narrowpeakFileOriginalPath 
    return specificPathsSumary
# destination = '/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2/reports/'
#     with cd(folder):
#         file_names = os.listdir()
#         csPosibilities = ['CG', 'CHG', 'CHH']
#         for file in file_names:
#             if '_box.mets.tsv' in file:
#                 bxdf = pd.read_csv(
#                     file,
#                     sep='\t', 
#                     names=['chr', 'position', 'strand', 'mets', 'nomets', 'context', 'boxID', 'side'],
#                     usecols=[ 'boxID','mets', 'nomets', 'context', 'side']
#                         )
#                 for cContext in csPosibilities:
#                     bxdfCX = bxdf[(bxdf['context'] == cContext)]
#                     regions = bxdfCX.groupby('boxID').sum()
#                     regions['result'] = regions['mets'] / (regions['nomets'] + regions['mets'])
#                     regions.reset_index(level=0, inplace=True)
#                     filesidename = '{}{}{}{}.tsv'.format(file[:-9],headname,'motifAndSides', cContext)
#                     regions.to_csv(
#                         filesidename,
#                         sep = '\t',
#                         columns=['boxID','result'],
#                         index=False, 
#                         header=['boxID',filesidename[:-4]]
#                         )
#                     originalFile = os.path.join(folder, filesidename)
#                     shutil.move(filesidename, destination)
#                     bxdfCX = bxdfCX[bxdfCX['side'] == 'box']
#                     regions = bxdfCX.groupby('boxID').sum()
#                     regions['result'] = regions['mets'] / (regions['nomets'] + regions['mets'])
#                     regions.reset_index(level=0, inplace=True)
#                     filesidename = '{}{}{}{}.tsv'.format(file[:-9],headname,'motifOnly', cContext)
#                     regions.to_csv(
#                         filesidename,
#                         sep = '\t',
#                         columns=['boxID','result'],
#                         index=False, 
#                         header=['boxID',filesidename[:-4]]
#                         )
#                     # 'mets', 'nomets' header=['boxID','mets{}'.format(filesidename[:-4]), 'nomets{}'.format(filesidename[:-4]),filesidename[:-4]]
#                     # originalFile = os.path.join(folder, filesidename)
#                     shutil.move(filesidename, destination)


# def mergeResultsMets(folder,headname):
#     with cd('/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2/reports/'):
#         file_names = os.listdir()

#         for side in ['motifOnly', 'motifAndSides']:
#             for metcontex in ['CG', 'CHG', 'CHH']:
#                 for box in ['G_box', 'GAC_box', 'PBE_box', 'GCC_box', 'TG_box']:
#                     boxfiles = []
#                     for file in file_names:
#                         # print(file_names)
#                         # print('hello')
#                         if side in file and metcontex in file and file.startswith(box):
#                             # print('hello')
#                             if '_merged_intersect.csv' not in file:
#                                 boxfiles.append(file)
#                     # print(boxfiles)
                    
#                     if box + side + metcontex + '_merged_intersect.csv' in file_names:
#                         experiment1df = pd.read_csv(box + side + metcontex + '_merged_intersect.csv', sep = '\t' )
#                         experiment2df = pd.read_csv(boxfiles[0], sep = '\t')
#                         mergedDf = experiment1df.merge(experiment2df, on=['boxID'], how='outer')
#                         if 'rep2' in boxfiles[0]:
#                             secondColumnName = '{}{}{}{}{}'.format(box,'rep1',headname,side,metcontex)
#                             mergedDf[headname] = (mergedDf[boxfiles[0][:-4]] + mergedDf[secondColumnName])/ 2
#                             del mergedDf[boxfiles[0][:-4]]
#                             del mergedDf[secondColumnName]
#                         mergedDf.to_csv(box + side + metcontex + '_merged_intersect.csv',sep = '\t', index=False)
#                         os.remove(boxfiles[0])
#                     elif len(boxfiles) == 2:
#                         # print('hello')
#                         experiment1df = pd.read_csv(boxfiles[0], sep = '\t')
#                         experiment2df = pd.read_csv(boxfiles[1], sep = '\t')
#                         # print(experiment1df)
#                         mergedDf = experiment2df.merge(experiment1df, on=['boxID'], how='outer')
#                         mergedDf[headname] = (mergedDf[boxfiles[0][:-4]] + mergedDf[boxfiles[1][:-4]])/ 2
#                         del mergedDf[boxfiles[0][:-4]]
#                         del mergedDf[boxfiles[1][:-4]]
#                         mergedDf.to_csv(box + side + metcontex + '_merged_intersect.csv',sep = '\t', index=False)
#                         os.remove(boxfiles[0])
#                         os.remove(boxfiles[1])
