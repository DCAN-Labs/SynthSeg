#!/usr/bin/env python

"""
This script dilates the LR mask generated for chirality correction in CABINET

Arguments:
    sub_LRmask_dir: location of directory that contains the LRmask.nii.gz file generated for a subject

Usage:
  dilate_lr_mask  <sub_LRmask_dir>
  dilate_lr_mask -h | --help
Options:
  -h --help     Show this screen.
"""

import os
import shutil
import nibabel as nib
import numpy as np
from docopt import docopt

from nipype.interfaces import fsl


def dilate_lr_mask(sub_LRmask_dir):
    os.chdir(sub_LRmask_dir)
    if not os.path.exists('lrmask_dil_wd'):
        os.mkdir('lrmask_dil_wd')

    anatfile = 'LRmask.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-thr 1 -uthr 1',
                           out_file='lrmask_dil_wd/Lmask.nii.gz')
    maths.run()

    maths = fsl.ImageMaths(in_file=anatfile, op_string='-thr 2 -uthr 2',
                           out_file='lrmask_dil_wd/Rmask.nii.gz')
    maths.run()

    maths.run()
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-thr 3 -uthr 3',
                           out_file='lrmask_dil_wd/Mmask.nii.gz')
    maths.run()

    # dilate, fill, and erode each mask in order to get rid of holes
    # (also binarize L and M images in order to perform binary operations)
    anatfile = 'lrmask_dil_wd/Lmask.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-dilM -dilM -dilM -fillh -ero',
                           out_file='lrmask_dil_wd/L_mask_holes_filled.nii.gz')
    maths.run()

    anatfile = 'lrmask_dil_wd/Rmask.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-bin -dilM -dilM -dilM -fillh -ero',
                           out_file='lrmask_dil_wd/R_mask_holes_filled.nii.gz')
    maths.run()

    anatfile = 'lrmask_dil_wd/Mmask.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-bin -dilM -dilM -dilM -fillh -ero',
                           out_file='lrmask_dil_wd/M_mask_holes_filled.nii.gz')
    maths.run()

    # Reassign values of 2 and 3 to R and M masks (L mask already a value of 1)
    anatfile = 'lrmask_dil_wd/R_mask_holes_filled.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-mul 2',
                           out_file='lrmask_dil_wd/R_mask_holes_filled_label2.nii.gz')
    maths.run()

    anatfile = 'lrmask_dil_wd/M_mask_holes_filled.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile, op_string='-mul 3',
                           out_file='lrmask_dil_wd/M_mask_holes_filled_label3.nii.gz')
    maths.run()

    # recombine new L, R, and M mask files
    anatfile_left = 'lrmask_dil_wd/L_mask_holes_filled.nii.gz'
    anatfile_right = 'lrmask_dil_wd/R_mask_holes_filled_label2.nii.gz'
    anatfile_mid = 'lrmask_dil_wd/M_mask_holes_filled_label3.nii.gz'
    maths = fsl.ImageMaths(in_file=anatfile_left, op_string='-add {}'.format(anatfile_right),
                           out_file='lrmask_dil_wd/recombined_mask_LR.nii.gz')
    maths.run()

    maths = fsl.ImageMaths(in_file=anatfile_mid, op_string='-add lrmask_dil_wd/recombined_mask_LR.nii.gz',
                           out_file='lrmask_dil_wd/dilated_LRmask.nii.gz')
    maths.run()

    ## Fix incorrect values resulting from recombining dilated components
    orig_LRmask_img = nib.load('LRmask.nii.gz')
    orig_LRmask_data = orig_LRmask_img.get_fdata()

    fill_LRmask_img = nib.load('lrmask_dil_wd/dilated_LRmask.nii.gz')
    fill_LRmask_data = fill_LRmask_img.get_fdata()

    # Flatten numpy arrays
    orig_LRmask_data_2D = orig_LRmask_data.reshape((182, 39676), order='C')
    orig_LRmask_data_1D = orig_LRmask_data_2D.reshape(7221032, order='C')

    fill_LRmask_data_2D = fill_LRmask_data.reshape((182, 39676), order='C')
    fill_LRmask_data_1D = fill_LRmask_data_2D.reshape(7221032, order='C')

    # grab index values of voxels with a value greater than 2.0 in filled L/R mask
    voxel_check = np.where(fill_LRmask_data_1D > 2.0)

    # Replace possible overlapping label values with corresponding label values from initial mask
    for i in voxel_check[:]:
        fill_LRmask_data_1D[i] = orig_LRmask_data_1D[i]

    # reshape numpy array
    fill_LRmask_data_2D = fill_LRmask_data_1D.reshape((182, 39676), order='C')
    fill_LRmask_data_3D = fill_LRmask_data_2D.reshape((182, 218, 182), order='C')

    # save new numpy array as image
    empty_header = nib.Nifti1Header()
    out_img = nib.Nifti1Image(fill_LRmask_data_3D, orig_LRmask_img.affine, empty_header)
    nib.save(out_img, 'LRmask_dil.nii.gz')

    #remove working directory with intermediate outputs
    #shutil.rmtree('lrmask_dil_wd')

if __name__ == '__main__':
    args = docopt(__doc__)
    dilate_lr_mask(args['<sub_LRmask_dir>'])
