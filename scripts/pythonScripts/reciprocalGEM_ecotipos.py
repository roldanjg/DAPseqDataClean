from cdmanager import cd
from pathlib import Path
from utilpipeline import (
    performGEMfree
)
from pathlib import Path
# comparamos todos los ecotipos ip frente a col-0(col-0 input)
basefolder_rep_two_or_one = '/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP_rep2'
# information_case_1 = [
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/1/2/IP12sorted.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP1-col0-cagadaaa'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/2/2/IP22.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP2-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/3/2/IP32.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP3-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/4/2/IP42.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP4-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/5/2/IP52.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP5-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/7/2/IP72.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP7-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/8/2/IP82.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP8-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/10/2/IP102.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP10-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/11/2/IP112.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP11-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/12/2/IP122.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP12-col0'],
#     ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/14/2/IP142.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP14-col0']
# ]
# # comparamos col-0 frente a cada uno de los ecotipos ip (ip input)
# information_case_2 = [
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/1/2/IP12.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP1'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/2/2/IP22.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP2'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/3/2/IP32.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP3'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/4/2/IP42.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP4'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/5/2/IP52.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP5'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/7/2/IP72.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP7'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/8/2/IP82.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP8'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/10/2/IP102.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP10'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/11/2/IP112.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP11'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/12/2/IP122.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP12'],
#     ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/14/2/IP142.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP14']
# ]

# comparamos todos los ecotipos ip frente a col-0(col-0 input)

information_case_3 = [
    [f'{basefolder_rep_two_or_one}/IP/1/1/IP11sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP1-col0'],
    [f'{basefolder_rep_two_or_one}/IP/2/1/IP21sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP2-col0'],
    [f'{basefolder_rep_two_or_one}/IP/3/1/IP31sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP3-col0'],
    [f'{basefolder_rep_two_or_one}/IP/4/1/IP41sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP4-col0'],
    [f'{basefolder_rep_two_or_one}/IP/5/1/IP51sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP5-col0'],
    [f'{basefolder_rep_two_or_one}/IP/7/1/IP71sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP7-col0'],
    [f'{basefolder_rep_two_or_one}/IP/8/1/IP81sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP8-col0'],
    [f'{basefolder_rep_two_or_one}/IP/10/1/IP101sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP10-col0'],
    [f'{basefolder_rep_two_or_one}/IP/11/1/IP111sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP11-col0'],
    [f'{basefolder_rep_two_or_one}/IP/12/1/IP121sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP12-col0'],
    [f'{basefolder_rep_two_or_one}/IP/13/1/IP131sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP13-col0'],
    [f'{basefolder_rep_two_or_one}/IP/14/1/IP141sorted.bam',f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/col0input/IP14-col0']
]

information_case_4 = [
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/1/1/IP11sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP1'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/2/1/IP21sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP2'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/3/1/IP31sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP3'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/4/1/IP41sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP4'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/5/1/IP51sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP5'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/7/1/IP71sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP7'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/8/1/IP81sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP8'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/10/1/IP101sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP10'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/11/1/IP111sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP11'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/12/1/IP121sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP12'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/13/1/IP131sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP13'],
    f'{basefolder_rep_two_or_one}/Input/Col-0/Input/InputCol-0Input.bam',[f'{basefolder_rep_two_or_one}/IP/14/1/IP141sorted.bam','/home/joaquin/projects/methylation/data/reciprocal_gem/arabidopsis_ecotypes_IP_second_round/ipinput/col0-IP14']
]
for information in [information_case_3,information_case_4]:
    for samplePath, inputControlpath, outputPaht in information:
        print(samplePath, inputControlpath, outputPaht)
        Path(outputPaht).mkdir(parents=True, exist_ok=True)

        performGEMfree(samplePath, inputControlpath, outputPaht)
