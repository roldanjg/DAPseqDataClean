import subprocess
import os
import pandas as pd
import shutil
from pathlib import Path
from cdmanager import cd
import filecmp
import re


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
                        '--cores', '2', '--paired', readOne, readTwo])


def performTrimGaloreFourFiles(folder):
    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if '1_1.fq.gz' in file:
                readOneOne = file
            if '1_2.fq.gz' in file:
                readOneTwo = file
            if '3_1.fq.gz' in file:
                readTwoOne = file
            if '3_2.fq.gz' in file:
                readTwoTwo = file

        subprocess.run(['trim_galore', '--phred33', '--fastqc', '--suppress_warn',
                        '--cores', '2', '--paired', readOneOne, readOneTwo, readTwoOne, readTwoTwo])
        subprocess.run(['trim_galore', '--phred33', '--fastqc', '--suppress_warn',
                        '--cores', '2', '--paired', readTwoOne, readTwoTwo])



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
            if '3_1_val_1_fastqc.zip' in file:
                subprocess.run(['unzip', file])
                readonefolder = file[:-4]
                with open(readonefolder + '/fastqc_data.txt', 'r') as report:
                    for line in report:
                        if re.match(r'^>>Per base sequence quality\tpass', line):
                            readOneOnepass = True

            if '3_2_val_2_fastqc.zip' in file:
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
     --path_to_aligner /home/bgp01/anaconda3/envs/metilation/bin/ \
      --verbose /home/bgp01/methylation/data/commonData/at/"""
    bismark = '/home/bgp01/methylation/programs/Bismark-0.22.3/bismark'
    genomeFolder = '/home/bgp01/methylation/data/commonData/at'


    with cd(folder):
        bis11 = None
        bis12 = None
        bis21 = None
        bis22 = None
        file_names = os.listdir()
        for file in file_names:
            if '1_1_val_1_fastqc.zip' in file:
                bis11 = file
            if '1_2_val_2_fastqc.zip' in file:
                bis12 = file
            if '3_1_val_1_fastqc.zip' in file:
                bis21 = file
            if '3_2_val_2_fastqc.zip' in file:
                bis22 = file

        subprocess.call(
                bismark + ' --genome_folder ' + genomeFolder +
                ' -1 ' + bis11 + ' ' + bis21 +
                ' -2 ' + bis12 + ' ' + bis22,
                shell=True
                        )
# TODO steps 2 y 3 bismark

def performBowtie2(folder, bowtie2mode, samOutputName):
    """ Before running this function, you must had run bowtie2-build <genome name>.fa genome_index
    in your common files folder and specify here the path to that document"""

    genomeIndex = '/home/bgp01/methylation/data/commonData/genome_index'

    with cd(folder):
        readOne = False
        readTwo = False
        file_names = os.listdir()
        for file in file_names:

            if 'val_1.fq.gz' in file:
                readOne = file

            if 'val_2.fq.gz' in file:
                readTwo = file

        bowtie2stats = subprocess.run('bowtie2 --phred33 ' + bowtie2mode + ' -t -p 10 -x ' + genomeIndex + ' -1 ' +
                                      readOne + ' -2 ' + readTwo + ' -S ' + samOutputName,
                                      shell=True, capture_output=True)
        print('Bowtie2 summary: ' + str(bowtie2stats.stdout))
        print('Bowtie2 errors if any: ' + str(bowtie2stats.stderr))
        with open('bowtie2stats.txt', 'w') as metrics:
            metrics.write(str(bowtie2stats))


def getBamAndDeleteSam(folder):
    samtools = '/home/bgp01/webproyect/programs/samtools-1.10/samtools'

    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if '.sam' in file:
                samfile = file
        subprocess.call([samtools, 'view', '-bh', samfile, '-o', samfile[:-4] + '.bam'])
        os.remove(samfile)


def performGEM(folder, inputSpecification, working_folder_name):  # inputSpecification = f'{id.time}/{id.tratement}'

    """ Before running this function, you must had run
    cat ../genome.fa |  awk -v RS=">" '{ print RS $0 > "<name>" substr($1,1)}'
    in your common files folder and specify here the path to that document"""

    genomeIndex = '/home/bgp01/methylation/data/commonData/Athchrs/'
    genomeSizes = '/home/bgp01/methylation/data/commonData/genome.index.txt'
    GEM = '/home/bgp01/methylation/programs/gem/gem.jar'
    Read_Distribution_default = '/home/bgp01/methylation/programs/gem/Read_Distribution_default.txt'
    inputControlpath = os.path.join(
        '/home/bgp01/methylation/data', working_folder_name, 'Input/amplified', inputSpecification
    )
    outputFolder = os.path.join('/home/bgp01/methylation/data', working_folder_name, folder, 'GEMout')

    with cd(inputControlpath):
        file_names = os.listdir()
        for file in file_names:
            if '.bam' in file:
                inputControl = os.path.join(inputControlpath, file)

    with cd(folder):
        Path(outputFolder).mkdir(parents=True, exist_ok=True)
        bamfile = False
        file_names = os.listdir()
        for file in file_names:

            if '.bam' in file:
                bamfile = file

        subprocess.call(
            ['java', '-jar', GEM, '--d', Read_Distribution_default,
             '--g', genomeSizes, '--genome', genomeIndex, '--s', '150000000',
             '--expt', bamfile, '--ctrl', inputControl,
             '--out', outputFolder, '--f', 'SAM', '--outNP', '--excluded_fraction', '0', '--range', '200',
             '--smooth', '0', '--mrc', '1', '--fold', '2', '--q', '1.301029996',
             '--k_min', '6', '--k_max', '20', '--k_seqs', '600', '--k_neg_dinu_shuffle',
             '--pp_nmotifs', '1', '--t', '10'], stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)


def sortBedFiles(folder):
    with cd(folder):
        samtools = '/home/bgp01/webproyect/programs/samtools-1.10/samtools'
        file_names = os.listdir()
        for file in file_names:
            if '.bam' in file:
                bamfile = file
        subprocess.call(samtools + ' sort -l 9 -m 2GiB -o ' + bamfile[:-4] + 'sorted.bam -O sam -@2 ' + bamfile,
                        shell=True
                        )


def performIntersect(folder, ExperimentTarget):
    """ as the program dont allow to obtain the results in a summary of total hits per box analyced, we do it """
    with cd(folder):
        samtools = '/home/bgp01/webproyect/programs/samtools-1.10/samtools'
        bedtools = '/home/bgp01/webproyect/programs/bedtools2/bedtools'
        if ExperimentTarget == 'MYCs':
            boxpath = {
                'Gbox': '/home/bgp01/methylation/data/commonData/intersect/G_box.bed',
                'PBE': '/home/bgp01/methylation/data/commonData/intersect/PBE_box.bed',
                'TG': '/home/bgp01/methylation/data/commonData/intersect/TG_box.bed',
            }
        elif ExperimentTarget == 'ERFs':
            boxpath = {
                'GAC': '/home/bgp01/methylation/data/commonData/intersect/GAC_box.bed',
                'GCC': '/home/bgp01/methylation/data/commonData/intersect/GCC_box.bed',
            }
        elif ExperimentTarget == 'Inputs':
            boxpath = {
                'Gbox': '/home/bgp01/methylation/data/commonData/intersect/G_box.bed',
                'PBE': '/home/bgp01/methylation/data/commonData/intersect/PBE_box.bed',
                'TG': '/home/bgp01/methylation/data/commonData/intersect/TG_box.bed',
                'GAC': '/home/bgp01/methylation/data/commonData/intersect/GAC_box.bed',
                'GCC': '/home/bgp01/methylation/data/commonData/intersect/GCC_box.bed',
            }
        file_names = os.listdir()
        for file in file_names:
            if 'sorted.bam' in file:
                bamsorted = file
        for boxfile in boxpath:
            subprocess.call(
                samtools + ' view -q1 -b ' + bamsorted + ' | ' +
                bedtools + ' intersect -abam stdin -b ' + boxpath[boxfile] + ' -bed -wb ' +
                '> ' + boxfile + '_' + bamsorted[:-10] + '.bed', shell=True
            )
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
                elcsv.write('chr,start,end,boxname,{}.total\n'.format(bamsorted[:-10]))
                for name, recount in totalForBox.items():
                    elcsv.write('{},{}\n'.format(name, recount))


def manageFolderLocationIntersects(destinationFolder, originFolder):
    with cd(originFolder):
        file_names = os.listdir()
    for file in file_names:
        if '_boxtotals.csv' in file:
            print(file)
            originalFile = os.path.join(originFolder, file)
            shutil.move(originalFile, destinationFolder)


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
                mergedDf = experiment1df.merge(experiment2df, on=['chr', 'start', 'end', 'boxname'], how='outer')
                mergedDf.to_csv(box + '_merged_intersect.csv', index=False)
                os.remove(boxfiles[0])
                os.remove(boxfiles[1])


def performBigWigextraction(folder):
    with cd(folder):
        file_names = os.listdir()
        for file in file_names:
            if 'sorted.bam' in file:
                samsorted = file
                bamsorted = str(samsorted[:-10]) + 'Sorted.bam'
                bigw = str(samsorted[:-10]) + 'coverage.bw'
                print(samsorted, bamsorted, bigw)

        subprocess.call('samtools view -bh -@6 ' + samsorted + ' -o ' + bamsorted, shell=True)
        os.remove(samsorted)
        subprocess.call('samtools index ' + bamsorted, shell=True)
        subprocess.call('bamCoverage -b ' + bamsorted +
                        ' -o ' + bigw +
                        ' --normalizeUsing BPM --binSize 10 --numberOfProcessors 6', shell=True)


def calculationGemSummary(folder):
    with cd(folder):
        print('-------------' + folder + '-------------')
        significant = None

        try:
            with open('GEM_Log.txt', 'r') as logGem:
                for line in logGem:
                    # if '_IP' in line:
                    #    print(line)
                    # if '_CTRL' in line:
                    #    print(line)
                    if 'Significant:' in line:
                        significant = line
                    # if 'Insignificant:' in line:
                    #    ins = line
                    # if 'Filtered:' in line:
                    #    fil = line
            print(significant)
        except:
            print('no gem done')
