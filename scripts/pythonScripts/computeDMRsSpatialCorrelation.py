import os
import subprocess

working_folder = '/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2_rep3/finalreps'
rscript = '/home/joaquin/projects/methylation/scripts/rscripts/computeMetsSpatialCorrelation.r'

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
    conditionsNames=f"{experiment}rep1 {experiment}rep2 {experiment}rep3"
    filename=f"{experiment}CMcoverage.jpg"
    sourceFiles = f'{experimentsClasification[experiment]["rep1"]} {experimentsClasification[experiment]["rep2"]} {experimentsClasification[experiment]["rep3"]}'
    print('{} {} {} {}'.format(rscript,conditionsNames, sourceFiles, filename))
    endProcess = subprocess.run(
                '{} {} {} {}'.format(rscript,conditionsNames, sourceFiles, filename),
                shell=True,
                capture_output=True
            )
            # first check if the subcommand has the standar err empty, whith mean it has run correct.
    print(endProcess.stderr,endProcess.stdout)
    # if endProcess.stderr.decode('ascii') == '':
        
    # else:
    #     print('there is an error related with bedtools')