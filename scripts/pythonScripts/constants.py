"""
    :platform: Unix
    :synopsis: Define different constants needed in the modules.

"""

"""

bowtie2 index:
    bowtie2-build <genome name>.fa genome_index

"""

# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/fragariaCamarosa/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/fragariaVesca/genome_index'
genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9568/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9535/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9557/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9526/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9510/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9593/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9874/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/medicagoTruncatula/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/brassicaOleracea/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/cicerArietinum/genome_index'
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/marchantiaPolimorpha/genome_index' 
# genomeIndex = '/home/joaquin/projects/methylation/data/commonData/solanumTuberosum/genome_index'
# sed -i 's/ version 1.0//g' Carietinum_492_v1.0.fa
# genomeIndex = '/home/joaquin/projects/methylation/data/pseudogenomesAt/genome_index'

"""

GEM index:
    cat <path_to_genome.fasta> |  awk -v RS=">" '{ print RS $0 > substr($1,1) ".fa"}'

"""

# gemIndex = '/home/joaquin/projects/methylation/data/commonData/fragariaCamarosa/Fcamchrs/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/fragariaVesca/FVechrs/'
gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/Athchrs/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9568/Athchrs9568/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9535/Athchrs9535/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9557/Athchrs9557/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9526/Athchrs9526/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9874/Athchrs9874/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9510/Athchrs9510/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9593/Athchrs9593/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/medicagoTruncatula/Mtrchrs/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/brassicaOleracea/Bolechrs/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/cicerArietinum/CiAchrs/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/marchantiaPolimorpha/MapChrs/'
# gemIndex = '/home/joaquin/projects/methylation/data/commonData/solanumTuberosum/solTu'

"""

GEM total gene lenghs:
 
    samtool faidx *fa
    cut -f1,2  *.fa.fai > genome.index.txt

if you want to remove the 00 chr and it is al the end sed -i '/>ST4.03ch00/Q'
"""

# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/fragariaCamarosa/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/fragariaVesca/genome.index.txt'
genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9568/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9535/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9557/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9526/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9510/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9593/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/ecotype9874/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/medicagoTruncatula/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/brassicaOleracea/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/cicerArietinum/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/marchantiaPolimorpha/genome.index.txt'
# genomeSizes = '/home/joaquin/projects/methylation/data/commonData/solanumTuberosum/genome.index.txt'

# -----------------we calculate the number of the efective genome size as the total bp that are not N in the genome
# cp /home/joaquin/projects/methylation/data/commonData/marchantiaPolimorpha/MpTak1v5.1.fasta 
# /home/joaquin/projects/methylation/mapol.fa && 
# sed -i -e 's/N//g' /home/joaquin/projects/methylation/mapol.fa &&
# grep -v '>' /home/joaquin/projects/methylation/mapol.fa | wc -m && grep -v '>' /home/joaquin/projects/methylation/mapol.fa | wc -l


# efective_size = '700000000' #solanumTuberosum
efective_size = '150000000' #arabidopsisThaliana Col-0
# efective_size = str(488104087-5326534) #cicerArietinum 488104087    5326534
# efective_size = str(218142404-444) #marchantiaPolimorpha 488104087    5326534
