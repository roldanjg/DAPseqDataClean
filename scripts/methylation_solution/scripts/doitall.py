import csv
import gzip
import time
import os
import pandas as pd
import re
from numpy import where as npwhere
from functools import reduce

def mapMethytilatedCitosine(metfile,intersection_file_path,output_file_path):
    chrs_data = {}
    with gzip.open(metfile, 'rt') as f:
        for line in f:
            chr_index = line.split('\t')[0]
            coordinate_index = int(line.split('\t')[1])
            try:
                chrs_data[chr_index][coordinate_index] = line[:-5]
            except:
                chrs_data[chr_index] = {coordinate_index:line[:-5]}

    with open(intersection_file_path) as f:
        reader = csv.reader(f, delimiter='\t')
        data = list(reader)

    with open(output_file_path, 'w') as whateverBox:
        for each_box in data:
            box_areas = {}
            box_start = int(each_box[1])
            box_end = int(each_box[2])
            chr_location = each_box[0]
            sequence_identifier = each_box[3]
            # tenemos que aplicar rango desde una posicion inicial porque es un archivo 0 based, si fuese 1 based el rango estaría mal y tendria que restarle
            # uno al archivo al box start
            box_areas['box'] = list(range(box_start, box_end))

            for boxarea in box_areas:
                for coordinate in box_areas[boxarea]:
                    matchline = chrs_data[chr_location].get(coordinate, False)
                    if matchline:
                        whateverBox.write('{}\t{}\t{}\n'.format(matchline, sequence_identifier, boxarea))
                        

def loadFileRemoveMtsAndLowMetReport(replicate):
        bxdf = pd.read_csv(
            replicate,
            sep='\t', 
            names=['chr', 'position', 'strand', 'mets', 'nomets', 'context', 'boxID', 'side'],
            usecols=['chr', 'position', 'strand', 'boxID','mets', 'nomets', 'context']
                )
        bxdf.drop(bxdf[(bxdf.chr == 'Mt') | (bxdf.chr == 'Pt')].index, inplace=True)
        bxdf = bxdf[bxdf['mets'] + bxdf['nomets'] >= 4]
        return bxdf

def calculateValueAsPercentageOfMetCs(replicatedf,replicanamedf):
    replicatedf[replicanamedf] = replicatedf['mets'] / (replicatedf['nomets'] + replicatedf['mets'])
    replicatedf = replicatedf.drop(columns=['mets','nomets'])
    return replicatedf

working_folder = '/home/joaquin/projects/methylation/data/bisulfite_rep1_rep2_rep3/finalreps'
intersection_file = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/intersect/allThePossiblePeaksnine.bed'
basedmrfolder = '/home/joaquin/projects/methylation/methylation_jose/met_site'
experimentsClasification = {}
for root, dirs, files in os.walk(working_folder):

    for file in files:
        if file.endswith('CX_report.txt.gz'):
            replicate, hour, condition =root.strip().split('/')[-3:]
            experimentName = hour+condition
            experimentsClasification.setdefault(experimentName, [])
            targetMetFilename = root+'/'+file
            finalnamedestination = '/home/joaquin/projects/methylation/scripts/methylation_solution/data'+'/'+experimentName+replicate+'allThePossiblePeaksnine.tsv'
            outputfile = finalnamedestination
            experimentsClasification[experimentName].append(outputfile)
            print(outputfile)
            mapMethytilatedCitosine(targetMetFilename,intersection_file,outputfile)


# allthedata = []
# for experimentCondition in experimentsClasification:
#     listOfDfReplicatesPercentageOfMetCs = []
#     listOfNamesReplicates = []
#     for replicatePath in experimentsClasification[experimentCondition]:

#         replicaname =  experimentCondition+replicatePath.split('/')[-4]
#         replicateDf = loadFileRemoveMtsAndLowMetReport(replicatePath)

#         replicateDfPercentageOfMetCs = calculateValueAsPercentageOfMetCs(replicateDf,replicaname)


#         listOfNamesReplicates.append(replicaname)

        
#     df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['chr','position', 'strand','context','boxID'],
#                                                 how='outer'), listOfDfReplicatesPercentageOfMetCs)
#     print(df_merged)
#     df_merged = df_merged.dropna()
#     df_merged[experimentCondition] = df_merged[listOfNamesReplicates].mean(axis=1)
#     print(df_merged)
#     df_merged = df_merged.drop(columns=listOfNamesReplicates)
#     allthedata.append(df_merged)
# finaldf = reduce(lambda  left,right: pd.merge(left,right,on=['chr','position', 'strand','context','boxID'],
#                                                 how='outer'), allthedata)



# finaldf = finaldf.dropna()