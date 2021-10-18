Intermediate steps of the generative model
==========================================

Example 1
---------

1. we first randomly
select an input label map, that is 

![Input Labels](../img/table3_example1_a.jpg "Input Labels")

Input Labels 

2. spatially augmented with a 3D
transformation. 

![Deformed Labels](../img/table3_example1_b.jpg "Deformed Labels")

Deformed Labels 

4. A first synthetic image is obtained by sampling a
GMM of randomised parameters at HR. 
5. The result is then corrupted
with a bias field and further intensity augmentation. 
6. Slice spacing
and thickness are simulated by successively blurring and downsampling
at random LR. 
7. The training inputs are obtained by resampling to
HR, and keeping the labels of the relevant structures (at the original
resolution) for segmentation.