from os import listdir, path
import subprocess



bedPeaks = '/home/joaquin/projects/methylation/data/allDataNarrowPeaksmin2repNineCoincidenceSingleSequence'
fastaArabGenome = '/home/joaquin/projects/methylation/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa'
fastafilesMine = '/home/joaquin/projects/methylation/fasta/fastafilesMine'
background = '/home/joaquin/projects/methylation/fasta/TAIR10_Model00.txt'
outfolder = '/home/joaquin/projects/methylation/fasta/outresultfullmemes'
listedDir = listdir(bedPeaks)

for file in listedDir:

    narrowpeakpath = path.join(bedPeaks,file)
    outFastaName = '_'.join(file.strip().split('_')[0:2]) + '.fa'
    outFastaNamePath = path.join(fastafilesMine,outFastaName)
    print(f'bedtools getfasta -fi {fastaArabGenome} -bed {narrowpeakpath} -fo {outFastaNamePath}')
    endProcess = subprocess.run(
                f'bedtools getfasta -fi {fastaArabGenome} -bed {narrowpeakpath} -fo {outFastaNamePath}',
                shell=True,
                capture_output=True
            )
    print(endProcess.stderr,endProcess.stdout)
    outputFilePath = path.join(outfolder,outFastaName[:-3])
    print(f'meme-chip {outFastaNamePath} -o {outputFilePath}  -bfile {background} -meme-mod zoops -meme-minw 8 -meme-maxw 15 -meme-nmotifs 2')
    endProcess = subprocess.run(
                f'meme-chip {outFastaNamePath} -o {outputFilePath}  -bfile {background} -meme-mod zoops -meme-p 30 -meme-minw 8 -meme-maxw 15 -meme-nmotifs 2',
                shell=True,
                capture_output=True
            )
            # first check if the subcommand has the standar err empty, whith mean it has run correct.
    print(endProcess.stderr,endProcess.stdout)

    # sed -i 's/>/>chr/g' /home/joaquin/projects/TDThub/webproyect/species/finished/inweb/Arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa  | bedtools getfasta -fi /home/joaquin/projects/TDThub/webproyect/species/finished/inweb/Arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa -bed /home/joaquin/projects/methylation/data/allDataNarrowPeaksmin2repNineCoincidenceSingleSequence/MYC324JA_amplified_replicates_common_Peaks_min_2_reps.narrowPeak