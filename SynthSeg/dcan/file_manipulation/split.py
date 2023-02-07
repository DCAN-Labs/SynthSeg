import os.path
from os import listdir
from os.path import isfile, join
import shutil
import glob
import os

from sklearn.model_selection import ShuffleSplit

my_path = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
label_files = glob.glob(my_path + '[0-9]mo_SynthSeg_generated_[0-9][0-9][0-9][0-9].nii.gz')
X = []
groups = []
for f in label_files:
    file_name = os.path.basename(f)
    X.append(f)
    groups.append(file_name[0])
rs = ShuffleSplit(n_splits=1, test_size=.20, random_state=0)

base_dir = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/'
labelsTs = '/home/feczk001/shared/data/nnUNet/labelsTs/550/'
imagesTr = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/imagesTr/'
imagesTs = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/imagesTs/'
labelsTr = '/home/feczk001/shared/data/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task550/labelsTr/'


def move_files(index, labels_dest, images_dest):
    for i in index:
        train_file = X[i]
        src = os.path.join(base_dir, train_file)
        dest = labels_dest
        shutil.move(src, dest)

        t1_file = train_file[:-7] + '_0000.nii.gz'
        t1_src = t1_file
        t1_dest = images_dest
        shutil.move(t1_src, t1_dest)

        t2_file = train_file[:-7] + '_0001.nii.gz'
        t2_src = t2_file
        t2_dest = images_dest
        shutil.move(t2_src, t2_dest)


for train_index, test_index in rs.split(X):
    move_files(train_index, labelsTr, imagesTr)
    move_files(test_index, labelsTs, imagesTs)
