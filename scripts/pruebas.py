from cdmanager import cd
import pandas as pd
import os

# the program must be run from the scripts folder
# define all  dir names in side your main project folder, methylation folder in this case

ROOT_DIR = os.path.dirname(os.path.abspath('.'))
SOURCE_MAIN_FOLDER = 'data/bisulfite_rep1_rep2'
DESTINATION_MAIN_FOLDER = 'data/bisulfite_reports'
IDS_FILE = 'data/commonData/ids_bisulfite_rep1_rep2.csv'

# define the paths for each folder necessary

dataSourceMainFolderPath = os.path.join(ROOT_DIR, SOURCE_MAIN_FOLDER)
dataDestinationMainFolderPath = os.path.join(ROOT_DIR, DESTINATION_MAIN_FOLDER)
idsPath = os.path.join(ROOT_DIR, IDS_FILE)

idsDf = pd.read_csv(
            idsPath, names=['id', 'rep', 'time', 'treatment']
                    )

for index, id in idsDf.iterrows():
    experimentSourceFolderPath = os.path.join(
                                            dataSourceMainFolderPath,
                                            str(id.rep),
                                            str(id.time),
                                            id.treatment
                                        )

    experimentDestinationFolderPath = os.path.join(
                                            dataDestinationMainFolderPath,
                                            str(id.rep),
                                            str(id.time),
                                            id.treatment
                                        )


Path(targetFolder).mkdir(parents=True, exist_ok=True)

