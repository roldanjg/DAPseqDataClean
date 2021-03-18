import subprocess
import os
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


def performBowtie2(folder, samOutputName):
    """ Before runing this function, you must had run bowtie2-build <genome name>.fa genome_index
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

        bowtie2stats = subprocess.run('bowtie2 --phred33 --sensitive-local -t -p 10 -x ' + genomeIndex + ' -1 ' +
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
        #sort!!
        os.remove(samfile)


def performGEM(folder, inputSpecification):  # f'{id.time}/{id.tratement}'

    """ Before runing this function, you must had run
    cat ../genome.fa |  awk -v RS=">" '{ print RS $0 > "<name>" substr($1,1)}'
    in your common files folder and specify here the path to that document"""

    genomeIndex = '/home/bgp01/methylation/data/commonData/Athchrs/'
    genomeSizes = '/home/bgp01/methylation/data/commonData/genome.index.txt'
    GEM = '/home/bgp01/methylation/programs/gem/gem.jar'
    Read_Distribution_default = '/home/bgp01/methylation/programs/gem/Read_Distribution_default.txt'
    inputControlpath = f'/home/bgp01/methylation/data/tfs/Input/amplified/{inputSpecification}/'
    outputFolder = os.path.join('/home/bgp01/methylation/data/tfs', folder, 'GEMout')

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

        printed = subprocess.call(
            ['java', '-jar', GEM, '--d', Read_Distribution_default,
             '--g', genomeSizes, '--genome', genomeIndex, '--s', '150000000',
             '--expt', bamfile, '--ctrl', inputControl,
             '--out', outputFolder, '--f', 'SAM', '--outNP', '--range', '200',
             '--smooth', '0', '--mrc', '1', '--fold', '2', '--q', '1.301029996',
             '--k_min', '6', '--k_max', '20', '--k_seqs', '600', '--k_neg_dinu_shuffle',
             '--pp_nmotifs', '1', '--t', '10'], stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
