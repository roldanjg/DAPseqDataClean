from cdmanager import cd
from pathlib import Path
from utilpipeline import (
    performGEMfree
)
from pathlib import Path
# comparamos todos los ecotipos ip frente a col-0(col-0 input)

information_case_1 = [
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/1/2/IP12.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP1-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/2/2/IP22.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP2-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/3/2/IP32.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP3-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/4/2/IP42.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP4-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/5/2/IP52.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP5-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/7/2/IP72.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP7-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/8/2/IP82.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP8-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/10/2/IP102.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP10-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/11/2/IP112.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP11-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/12/2/IP122.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP12-col0'],
    ['/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/14/2/IP142.bam','/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/col0input/IP14-col0']
]
# comparamos col-0 frente a cada uno de los ecotipos ip (ip input)
information_case_2 = [
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/1/2/IP12.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP1'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/2/2/IP22.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP2'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/3/2/IP32.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP3'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/4/2/IP42.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP4'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/5/2/IP52.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP5'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/7/2/IP72.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP7'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/8/2/IP82.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP8'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/10/2/IP102.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP10'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/11/2/IP112.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP11'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/12/2/IP122.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP12'],
    ['/home/joaquin/projects/methylation/data/data_concentraciones_round2/ZYMO/15/50ng/ZYMO1550ngsorted.bam','/home/joaquin/projects/methylation/data/data_arabidopsis_ecotypes_IP/IP/14/2/IP142.bam','/home/joaquin/projects/methylation/data/data_reciprocal_gem/ipinput/col0-IP14']
]
for information in [information_case_2, information_case_1]:
    for samplePath, inputControlpath, outputPaht in information:
        print(samplePath, inputControlpath, outputPaht)
        Path(outputPaht).mkdir(parents=True, exist_ok=True)

        performGEMfree(samplePath, inputControlpath, outputPaht)
