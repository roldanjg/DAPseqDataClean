import subprocess
import pandas as pd
output_folder_path = '/home/joaquin/projects/methylation/data/bisulfite_quick_and_dirty_rep1_rep2/bigwig_from_individual_mets'
chr_sizes = '/home/joaquin/projects/methylation/data/commonData/arabidopsisThaliana/genome.index.txt'

def bedgraphToBwFromMean(bedgraphFilePath, speciesIndexChrSize):
    subprocess.run('bedGraphToBigWig ' + bedgraphFilePath + ' ' + speciesIndexChrSize + ' ' + bedgraphFilePath[:-8]+'bw',
            shell=True)




file_paths = ['CG_BSMet_all_the_samples_no_intersect_files_CG_context','nonCG_BSMet_all_the_samples_no_intersect_files']
context_case_list = ['CG','nonCG']
for file_name, context_case in zip(file_paths, context_case_list):
    df_load = None
    df_load = pd.read_csv(f'/home/joaquin/projects/methylation/data/bisulfite_quick_and_dirty_rep1_rep2/{file_name}.tsv',sep='\t')
    for case in ['1Mock','1JA','1ACC','6Mock','6JA','6ACC','24Mock','24JA','24ACC']:
        bedgraph_file_path = f'{output_folder_path}/{case}_{context_case}.bedgraph'
        subdf = df_load[['chr','position',case]].copy()
        subdf['end'] = subdf['position']
        subdf[['chr','position','end',case]].dropna(axis='rows').to_csv(bedgraph_file_path,sep='\t', index=False, header=False)
        bedgraphToBwFromMean(bedgraph_file_path,chr_sizes)

rsync  -av --exclude={'*.bedgraph'} --max-size=900m joaquin@acrab.cnb.csic.es:/home/joaquin/projects/methylation/data/bisulfite_quick_and_dirty_rep1_rep2/bigwig_from_individual_mets .