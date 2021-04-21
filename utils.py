from config import *
import numpy as np
from PIL import ImageOps, Image
from sklearn.model_selection import train_test_split
import math


def split_dataset(list_to_split, ratio):
    elements = len(list_to_split)
    middle = int(elements * ratio)
    return [list_to_split[:middle], list_to_split[middle:]]


def convert_image(img_path=None, image=None):
    img = None
    if img_path:
        img = np.array(ImageOps.invert(Image.open(img_path)).resize(IMG_SIZE).convert('L'))
    if image:
        img = np.array(ImageOps.invert(image).resize(IMG_SIZE).convert('L'))
    img = (img / 255.0 * 0.99) + 0.01
    img = img.reshape(IMG_SHAPE)
    return img


def files_to_img_list(files):
    img_list = []
    for file in files:
        img = convert_image(img_path=file)
        img_list.append(img)
    return img_list


def load_nn():
    from NeuralNetwork import NeuralNetwork
    return NeuralNetwork(path=NN_PATH)


def save_nn_to_file(nn):
    nn.saveWeights(path=NN_PATH)


def get_train_and_valid(x, y, ratio=0.8):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=ratio, stratify=y)
    train = [list(x) for x in zip(x_train, y_train)]
    validation = [list(x) for x in zip(x_test, y_test)]
    return train, validation


def get_labels_count(data):
    label_count = {}

    for label in OUTPUT_LABELS:
        label_count[label] = 0

    for i in data:
        label_count[i[1]] += 1

    return label_count


def get_input_nodes():
    var1 = IMG_SIZE[0]
    for i in range(1, NUM_KERNELS + 1):
        var1 = (math.floor((var1 - 2) / 2))
    if IMG_SIZE[0] != IMG_SIZE[1]:
        var2 = IMG_SIZE[1]
        for i in range(1, NUM_KERNELS + 1):
            var2 = (math.floor((var2 - 2) / 2))
        return var1 * var2 * 2 ** (NUM_KERNELS + 1)
    else:
        return var1 ** 2 * 2 ** (NUM_KERNELS + 1)
