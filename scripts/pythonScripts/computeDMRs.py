import os
import subprocess
import re
 

working_folder = '/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2_rep3/finalreps'
rscript = '/home/joaquin/projects/methylation/scripts/rscripts/computeDMRs.r'

experimentsClasification = {}
for root, dirs, files in os.walk(working_folder):

    for file in files:
        if 'CX_report.txt.gz' in file:
            replicate, hour, condition =root.strip().split('/')[-3:]
            experimentName = hour+condition
            experimentsClasification.setdefault(experimentName, {})
            targetMetFilename = root+'/'+file
#             movetofolderallthefiles(targetMetFilename, finalnamedestination)
            outputfile = targetMetFilename[:-3] + 'peakMets.tsv'
            experimentsClasification[experimentName][replicate]=targetMetFilename
#             print(outputfile)
#             mapMethytilatedCitosine(targetMetFilename,intersection_file,outputfile)


for experiment in experimentsClasification:
    if not 'Mock' in experiment:
        regular = re.findall(r'(\d+)', experiment)
        tm = regular[0]
        sourceFilesControl = f'{experimentsClasification[tm+"Mock"]["rep1"]} {experimentsClasification[tm+"Mock"]["rep2"]} {experimentsClasification[tm+"Mock"]["rep3"]}'
        filename=f"{experiment}CMcoverage.jpg"
        sourceFilesSample = f'{experimentsClasification[experiment]["rep1"]} {experimentsClasification[experiment]["rep2"]} {experimentsClasification[experiment]["rep3"]}'
        print('{} {} {} {}'.format(rscript,sourceFilesControl,sourceFilesSample, experiment))
        endProcess = subprocess.run(
                    '{} {} {} {}'.format(rscript,sourceFilesControl,sourceFilesSample, experiment),
                    shell=True,
                    capture_output=True
                )
                # first check if the subcommand has the standar err empty, whith mean it has run correct.
        print(endProcess.stderr,endProcess.stdout)
        # if endProcess.stderr.decode('ascii') == '':
        
    # else:
    #     print('there is an error related with bedtools')