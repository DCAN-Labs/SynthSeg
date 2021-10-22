Intermediate steps of the generative model
==========================================

|           | Input Labels                                                 | Deformed Labels                                                    | GMM Sampling                                                 | Bias Corruption | Downsampling | Inputs for training |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------ | --------------- | --------------- | --------------- |
| 8-month-old | ![Input Labels](../img/table3_example1_a.jpg "Input Labels") | ![Deformed Labels](../img/table3_example1_b.jpg "Deformed Labels") | ![GMM Sampling](../img/table3_example1_c.jpg "GMM Sampling") | ![Bias Corruption](../img/table3_example1_d.jpg "Bias Corruption") | ![Downsampling](../img/table3_example1_e.jpg "Downsampling") | ![Images for training](../img/table3_example1_f.jpg "Images for training") |
| 4-month-old | ![Input Labels](../img/table3_example2_a.jpg "Input Labels") | ![Deformed Labels](../img/table3_example2_b.jpg "Deformed Labels") | ![GMM Sampling](../img/table3_example2_c.jpg "GMM Sampling") | ![Bias Corruption](../img/table3_example2_d.jpg "Bias Corruption") | ![Downsampling](../img/table3_example2_e.jpg "Downsampling") | ![Images for training](../img/table3_example2_f.jpg "Images for training") |
| 0-month-old | ![Input Labels](../img/table3_example3_a.jpg "Input Labels") | ![Deformed Labels](../img/table3_example3_b.jpg "Deformed Labels") | ![GMM Sampling](../img/table3_example2_c.jpg "GMM Sampling") | ![Bias Corruption](../img/table3_example3_d.jpg "Bias Corruption") | ![Downsampling](../img/table3_example3_e.jpg "Downsampling") | ![Images for training](../img/table3_example3_f.jpg "Images for training") |

1. we first randomly
select an input label map, that is 
2. spatially augmented with a 3D
transformation. 
3. A first synthetic image is obtained by sampling a
GMM of randomised parameters at HR. 
4. The result is then corrupted
with a bias field and further intensity augmentation. 
5. Slice spacing
and thickness are simulated by successively blurring and downsampling
at random LR. 
6. The training inputs are obtained by resampling to
HR, and keeping the labels of the relevant structures (at the original
resolution) for segmentation.