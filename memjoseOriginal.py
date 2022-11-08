from os import listdir
import subprocess



x = '/home/joaquin/projects/methylation/fasta/fastafiles'
background = '/home/joaquin/projects/methylation/fasta/TAIR10_Model00.txt'
outfolder = '/home/joaquin/projects/methylation/fasta/outresultzoopsparal'
listedDir = listdir(x)

for file in listedDir: 
    fimename = x+'/'+file
    print(file)
    print(f'meme-chip {fimename} -o {outfolder}/{file[:-3]}  -bfile {background} -meme-mod zoops -meme-minw 8 -meme-maxw 15 -meme-nmotifs 2')
    endProcess = subprocess.run(
                f'meme-chip {fimename} -o {outfolder}/{file[:-3]}  -bfile {background} -meme-mod zoops -meme-p 30 -meme-minw 8 -meme-maxw 15 -meme-nmotifs 2',
                shell=True,
                capture_output=True
            )
            # first check if the subcommand has the standar err empty, whith mean it has run correct.
    print(endProcess.stderr,endProcess.stdout)