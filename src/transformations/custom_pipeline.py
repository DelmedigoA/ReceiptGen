from augraphy.base.augmentationpipeline import AugraphyPipeline
from augraphy.augmentations import Letterpress
from augraphy import *
import cv2
import numpy as np
import PIL
import textwrap
import random

def add_noise(img: PIL.Image.Image):
    array = np.array(img)
    return PIL.Image.fromarray(pipeline(array))


prob = 0.4

ink_phase = [
            NoiseTexturize(sigma_range=(1, 3),
                                 turbulence_range=(1, 4),
                                 texture_width_range=(10, 300),
                                 texture_height_range=(10, 300),
                                 p=prob
                                 ),


              Scribbles(scribbles_type="random",
                      scribbles_ink="random",
                      scribbles_location="random",
                      scribbles_size_range=(100, 600),
                      scribbles_count_range=(1, 6),
                      scribbles_thickness_range=(1, 3),
                      scribbles_brightness_change=[8, 16],
                      scribbles_skeletonize=0,
                      scribbles_skeletonize_iterations=(2, 3),
                      scribbles_color="random",
                      scribbles_text="random",
                      scribbles_text_font="random",
                      scribbles_text_rotate_range=(0, 360),
                      scribbles_lines_stroke_count_range=(1, 6),
                      p=prob
                      ),


              NoisyLines(noisy_lines_direction = random.choice([0,1]),
                        noisy_lines_location = "random",
                        noisy_lines_number_range = (3,5),
                        noisy_lines_color = (0,0,0),
                        noisy_lines_thickness_range = (2,2),
                        noisy_lines_random_noise_intensity_range = (0.01, 0.1),
                        noisy_lines_length_interval_range = (0, 100),
                        noisy_lines_gaussian_kernel_value_range = (3,3),
                        noisy_lines_overlay_method = "ink_to_paper",
                        p=prob
                        ),

              DirtyDrum(line_width_range=(5, 10),
                      line_concentration=0.3,
                      direction=random.choice([0,1]),
                      noise_intensity=0.2,
                      noise_value=(0, 10),
                      ksize=(3, 3),
                      sigmaX=0,
                      p=prob
                      ),


              Letterpress(n_samples=(50, 100),
                          n_clusters=(10, 10),
                          std_range=(100, 400),
                          value_range=(200, 255),
                          blur=0.1,
                          p=0.9
            ),
]

pipeline = AugraphyPipeline(ink_phase=ink_phase)