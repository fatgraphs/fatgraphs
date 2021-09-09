#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
import numpy as np
from skimage import io, util
from skimage.draw import ellipse
import copy
from skimage.transform import resize

border_width = 3
input_path = "../assets/raw_icons"
raw_pngs_paths = [join(input_path, f) for f in listdir(input_path) if isfile(join(input_path, f))]
raw_pngs = list(map(lambda e: io.imread(e), raw_pngs_paths))

def get_most_frequent_color(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]

def add_ring(img, offset, width, color):
    image = copy.deepcopy(img)
    image_size = len(image)
    orr, occ = ellipse(image_size/2, image_size/2, offset+width, offset+width, shape=[image_size,image_size])
    irr, icc = ellipse(image_size/2, image_size/2, offset, offset, shape=[image_size,image_size])
    mask = np.zeros((image_size, image_size), dtype=np.uint8)
    mask[orr, occ] = 1
    mask[irr, icc] = 0
    # plt.imshow(mask, cmap='gray')
    image[mask==1] = color
    return(image)

def circle_icon_to_square_icon(img, inset=2):
    image = copy.deepcopy(img)
    image_size = len(image)
    dominant_color = get_most_frequent_color(image)
    image = add_ring(image, image_size/2-inset, image_size, dominant_color)
    return(image)

def add_white_rect_border(img, width=3):
    image = copy.deepcopy(img)
    white = [255, 255, 255, 255]
    image_size = len(image)
    image[0:width, :] = white
    image[(image_size-width):image_size, :] = white
    image[:, 0:width] = white
    image[:, (image_size-width):image_size] = white
    return(image)

def add_white_circ_border(img, width=3):
    image = copy.deepcopy(img)
    image = add_ring(image, len(icon)/2-width, width+1, 1)
    image = add_ring(image, len(icon)/2-width, width, [255, 255, 255, 255])
    return(image)

def _to_128(image):
    return util.img_as_ubyte(resize(image, (128, 128, image.shape[2])))


output_path = "../assets/vertex_icons/tokens"
for icon, path in zip(raw_pngs, raw_pngs_paths):

    icon = _to_128(icon)

    if icon.shape[2] == 3:
        icon = np.dstack((icon, np.array([[[1.0]]*128]*128)))

    name = path.split('/')[-1].split('.')[0]
    circle_border_icon = add_white_circ_border(icon)
    io.imsave(output_path + '/' + name + "-eoa.png", circle_border_icon)

    bordered_square_icon = add_white_rect_border(circle_icon_to_square_icon(icon))
    io.imsave(output_path + '/' + name + "-ca.png", bordered_square_icon)
