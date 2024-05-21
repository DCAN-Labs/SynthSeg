import shutil
from os import listdir
from os.path import isfile, join

from tqdm import tqdm

source = '/scratch.global/reine097/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/SyntheticData/labels/'
destination = '/scratch.global/reine097/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task526_BobsRepo/labelsTr/'
only_files = [f for f in listdir(source) if isfile(join(source, f))]
for f in tqdm(only_files):
    shutil.move(join(source, f), destination)
