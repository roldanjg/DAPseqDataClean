from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    checkMD5isCorrect,
    checkFastaQLenght,
    performTrimGaloreFourFilesBisulfite,
    qualityCheckTrimGaloreFourFiles,
    performBismark,
    deduplicateBismark,
    methylationExtractionBismark,
    reportBismark
)

ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_check_goodshit.csv'
working_folder = '/home/joaquin/projects/methylation/data/bisulfite_quick_and_dirty_rep1_rep2'
raw_folder = '/home/joaquin/projects/methylation/data/AllRawData/raw_bisulfite_rep1_rep2_rep3'
execution_reports = '/home/joaquin/projects/methylation/execution_reports/ids_bisulfite_test_case_two_execution_report.txt'

mate_number = str(3)

def burn_to_report(message):
    with open(execution_reports, 'a') as repor_something:
        repor_something.write(message)


with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'rep', 'time', 'treatment'])

with cd(working_folder):
    for index, id in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(str(id.rep), str(id.time), id.treatment)
        Path(targetFolder).mkdir(parents=True, exist_ok=True)
        originalfolder = os.path.join(raw_folder, id.id)
        file_names = os.listdir(originalfolder)
        
        message = '------------- Processing ' + id.id + '-------------' +' \n'
        print(message)
        burn_to_report(message)
        if len(file_names) >= 2:
            message = 'The number of files is correct, checking MD5 from ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
        else:
            message = 'ERROR: THERE ARE NOT ENOUGHT FILES FOR ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
            continue
            #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends, more if divided long files
        if checkMD5isCorrect(originalfolder):
            message = ' MD5 correct. Checking Fastaq lengths from ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
        else:
            message = 'ERROR: MD5 ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
            continue

        if checkFastaQLenght(originalfolder):
            message = 'FastQ lenght correct. Doing Trim galore in ' + targetFolder + ' from ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
        else:
            message = 'ERROR: FastaQ Lenght in ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
            continue

        # mv files to the folder where the analisys will be made
        for fileInside in file_names:
            if 'gz' in fileInside:
                gzs.append((fileInside))
                originalFile = os.path.join(originalfolder, fileInside)
                shutil.move(originalFile, targetFolder)
        
        performTrimGaloreFourFilesBisulfite(targetFolder, mate_number)
        
        for file in gzs:
            destinationFile = os.path.join(targetFolder, file)
            shutil.move(destinationFile, originalfolder)


        if qualityCheckTrimGaloreFourFiles(targetFolder,mate_number):
            message = 'Quality Check TrimGalore FourFiles correct. Doing Bismark in ' + targetFolder + ' from ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
        else:
            message = 'ERROR: qualityCheck TrimGalore Four Files ' + id.id + ' \n'
            print(message)
            burn_to_report(message)
            continue

        print('Doing bismark in ' + targetFolder + ' from ' + id.id)
        performBismark(targetFolder, mate_number)
        print('deduplicate bismark in ' + targetFolder + ' from ' + id.id)
        deduplicateBismark(targetFolder, mate_number)
        print('methylationExtraction bismark in ' + targetFolder + ' from ' + id.id)
        methylationExtractionBismark(targetFolder)
        print('report bismark in ' + targetFolder + ' from ' + id.id)
        reportBismark(targetFolder)
        
        
            
        
            

