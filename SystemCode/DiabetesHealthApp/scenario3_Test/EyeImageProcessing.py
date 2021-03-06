import numpy as np
import pandas as pd
from PIL import Image
import os

class EyeImgProcessing:

    def readLabel(self):
        Trainlabels = pd.read_csv("trainLabels.csv")

        lst_imgs = [img for img in Trainlabels['image']]
        print(os.path.join(os.getcwd(), '/train/' + '28661_left' + '.jpeg'))
        X_train = np.array([np.array(Image.open(os.path.join(os.getcwd(), '/train/' + img + '.jpeg'))) for img in lst_imgs])
        print(X_train.shape)