from cdmanager import cd
from pathlib import Path
from utilpipeline import (
    performGEMmultipleReplicateSpecialcaseTwoInputs
)
from pathlib import Path

basefolder_rep_one = '/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP'
basefolder_rep_two_or_one = '/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP_rep2'
output_general_folder = '/home/joaquin/projects/methylation/data/gemFiles/MultiGEM_arabidopsis_ecotypes_IP'

information_case = [
    [f'{basefolder_rep_one}/IP/1/2/IP12sorted.bam',f'{basefolder_rep_one}/Input/1/Input/Input1Input.bam',f'{basefolder_rep_two_or_one}/IP/1/1/IP11sorted.bam',f'{basefolder_rep_two_or_one}/Input/1/Input/Input1Input.bam',f'{output_general_folder}/IP1'],
    [f'{basefolder_rep_one}/IP/2/2/IP22sorted.bam',f'{basefolder_rep_one}/Input/2/Input/Input2Input.bam',f'{basefolder_rep_two_or_one}/IP/2/1/IP21sorted.bam',f'{basefolder_rep_two_or_one}/Input/2/Input/Input2Input.bam',f'{output_general_folder}/IP2'],
    [f'{basefolder_rep_one}/IP/3/2/IP32sorted.bam',f'{basefolder_rep_one}/Input/3/Input/Input3Input.bam',f'{basefolder_rep_two_or_one}/IP/3/1/IP31sorted.bam',f'{basefolder_rep_two_or_one}/Input/3/Input/Input3Input.bam',f'{output_general_folder}/IP3'],
    [f'{basefolder_rep_one}/IP/3/2/IP42sorted.bam',f'{basefolder_rep_one}/Input/4/Input/Input4Input.bam',f'{basefolder_rep_two_or_one}/IP/4/1/IP41sorted.bam',f'{basefolder_rep_two_or_one}/Input/4/Input/Input4Input.bam',f'{output_general_folder}/IP4'],
    [f'{basefolder_rep_two_or_one}/IP/5/2/IP52sorted.bam',f'{basefolder_rep_two_or_one}/Input/5/Input/Input5Input.bam',f'{basefolder_rep_two_or_one}/IP/5/1/IP51sorted.bam',f'{basefolder_rep_two_or_one}/Input/5/Input/Input5Input.bam',f'{output_general_folder}/IP5'],
    [f'{basefolder_rep_one}/IP/7/2/IP72sorted.bam',f'{basefolder_rep_one}/Input/7/Input/Input7Input.bam',f'{basefolder_rep_two_or_one}/IP/7/1/IP71sorted.bam',f'{basefolder_rep_two_or_one}/Input/7/Input/Input7Input.bam',f'{output_general_folder}/IP7'],
    [f'{basefolder_rep_one}/IP/8/2/IP82sorted.bam',f'{basefolder_rep_one}/Input/8/Input/Input8Input.bam',f'{basefolder_rep_two_or_one}/IP/8/1/IP81sorted.bam',f'{basefolder_rep_two_or_one}/Input/8/Input/Input8Input.bam',f'{output_general_folder}/IP8'],
    [f'{basefolder_rep_one}/IP/10/2/IP102sorted.bam',f'{basefolder_rep_one}/Input/10/Input/Input10Input.bam',f'{basefolder_rep_two_or_one}/IP/10/1/IP101sorted.bam',f'{basefolder_rep_two_or_one}/Input/10/Input/Input10Input.bam',f'{output_general_folder}/IP10'],
    [f'{basefolder_rep_one}/IP/11/2/IP112sorted.bam',f'{basefolder_rep_one}/Input/11/Input/Input11Input.bam',f'{basefolder_rep_two_or_one}/IP/11/1/IP111sorted.bam',f'{basefolder_rep_two_or_one}/Input/11/Input/Input11Input.bam',f'{output_general_folder}/IP11'],
    [f'{basefolder_rep_one}/IP/12/2/IP122sorted.bam',f'{basefolder_rep_one}/Input/12/Input/Input12Input.bam',f'{basefolder_rep_two_or_one}/IP/12/1/IP121sorted.bam',f'{basefolder_rep_two_or_one}/Input/12/Input/Input12Input.bam',f'{output_general_folder}/IP12'],
    [f'{basefolder_rep_two_or_one}/IP/13/2/IP132sorted.bam',f'{basefolder_rep_two_or_one}/Input/13/Input/Input13Input.bam',f'{basefolder_rep_two_or_one}/IP/13/1/IP131sorted.bam',f'{basefolder_rep_two_or_one}/Input/13/Input/Input13Input.bam',f'{output_general_folder}/IP13'],
    [f'{basefolder_rep_one}/IP/14/2/IP142sorted.bam',f'{basefolder_rep_one}/Input/14/Input/Input14Input.bam',f'{basefolder_rep_two_or_one}/IP/14/1/IP141sorted.bam',f'{basefolder_rep_two_or_one}/Input/14/Input/Input14Input.bam',f'{output_general_folder}/IP14'],
    [f'{basefolder_rep_one}/Col-0/Col-0/50ng/ZYMO1550ngsorted.bam',f'{basefolder_rep_one}/Input/Col-0/Input/InputCol-0Input.bam',f'{basefolder_rep_two_or_one}/IP/Col-0/1/IPCol-01sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',f'{output_general_folder}/Col-0']
    ]

for information in [information_case]:
    for sample1Path,inputControlpathone,sample2Path,inputControlpathtwo, outputPaht in information:
        print(sample1Path,sample2Path, inputControlpathone, inputControlpathtwo, outputPaht)
        Path(outputPaht).mkdir(parents=True, exist_ok=True)
        performGEMmultipleReplicateSpecialcaseTwoInputs(sample1Path,sample2Path, inputControlpathone,inputControlpathtwo, outputPaht)
