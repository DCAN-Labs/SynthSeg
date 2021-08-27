import numpy as np
import sys


def create_dcan_generation_labels_file(out_file):
    labels = np.array(
        [0,  # background
         24,  # CSF
         14,  # 3rd-Ventricle
         15,  # 4th-Ventricle
         16,  # Brain-Stem
         77,  # WM-hypointensities
         85,  # Optic-Chiasm
         172,  # Vermis
         1,  # Left-Cerebral-Exterior
         2,  # Left-Cerebral-White-Matter
         3,  # Left-Cerebral-Cortex
         4,  # Left-Lateral-Ventricle
         5,  # Left-Inf-Lat-Vent
         6,  # Left-Cerebellum-Exterior
         7,  # Left-Cerebellum-White-Matter
         8,  # Left-Cerebellum-Cortex
         10,  # Left-Thalamus-Proper
         11,  # Left-Caudate
         12,  # Left-Putamen
         13,  # Left-Pallidum
         17,  # Left-Hippocampus
         18,  # Left-Amygdala
         26,  # Left-Accumbens-area
         28,  # Left-VentralDC
         30,  # Left-vessel
         31,  # Left-choroid-plexus
         40,  # Right-Cerebral-Exterior
         41,  # Right-Cerebral-White-Matter
         42,  # Right-Cerebral-Cortex
         43,  # Right-Lateral-Ventricle
         44,  # Right-Inf-Lat-Vent
         45,  # Right-Cerebellum-Exterior
         46,  # Right-Cerebellum-White-Matter
         47,  # Right-Cerebellum-Cortex
         49,  # Right-Thalamus-Proper
         50,  # Right-Caudate
         51,  # Right-Putamen
         52,  # Right-Pallidum
         53,  # right hippocampus
         54,  # Right-Amygdala
         58,  # Right-Accumbens-area
         60,  # Right-VentralDC
         62,  # Right-vessel
         63])  # Right-choroid-plexus
    np_array = np.array(labels)
    np.save(out_file, np_array)


if __name__ == "__main__":
    create_dcan_generation_labels_file(sys.argv[1])
