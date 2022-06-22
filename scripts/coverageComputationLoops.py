from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
   performIntersectLoops,
    manageFolderLocationIntersects,
    mergeResultsloop
)
ids_file = '/home/joaquin/projects/methylation/data/commonData/id_intersect_loops.csv'
working_folder = '/home/joaquin/projects/methylation/data/'
intersectsFolder= '/home/joaquin/projects/methylation/data/intersects/loops/'

idsDf = pd.read_csv(
            ids_file,
            names=['folder','id', 'tf', 'loop']
                    )

with cd(working_folder):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.folder, id.tf, id.loop)
        
        # performIntersectLoops(targetFolder)
        manageFolderLocationIntersects(intersectsFolder, targetFolder)
        mergeResultsloop(intersectsFolder)



