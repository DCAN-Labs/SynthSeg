import sys
import nibabel as nib
import tqdm


def print_labels(nifti_file):
    img = nib.load(nifti_file)
    image_data = img.get_fdata()
    labels = set()
    shape = image_data.shape
    for i in tqdm.tqdm(range(shape[0]), leave=False):
        for j in range(shape[1]):
            for k in range(shape[2]):
                labels.add(int(round(image_data[i][j][k])))
    labels = sorted(list(labels))
    print(labels)

if __name__ == "__main__":
    nifti_file = sys.argv[1]
    print_labels(nifti_file)
