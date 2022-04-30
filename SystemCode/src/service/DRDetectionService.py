# importing the requests library
from keras.models import load_model
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import cv2
import io
import os

def cnnmodel():

    module_path = os.path.abspath(os.path.join('../..'))
    filepath = module_path +  'model/' + 'model2.h5'
    print(filepath)

    model = load_model(filepath)
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

    return model

def cvt_2_base64(file_name):
    img = cv2.imread(file_name)
    _, im_arr = cv2.imencode('.jpeg', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64

def stringToImage(base64_string):
    im_bytes = base64.b64decode(base64_string)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    return img

def getRetinopathyLevel(strbase64):
    #img = cv2.imread(img)
    #img64 = Image.open(BytesIO(base64.decodebytes(bytes(strbase64))))
    try:
        img = stringToImage(strbase64)
        img = cv2.resize(img, (224, 224))
        img = np.reshape(img, [1, 224, 224, 3])

        model = cnnmodel()
        model_preds = model.predict(img)
        print("getRetinopathyLevel")
        print(model_preds)
        classes = np.argmax(model.predict(img), axis=-1)

        print(classes)
    except Exception as e: 
        print(e)        
        print('Ooopss')

    return classes
    #return model_preds

def testImage():
    image_64_encode = cvt_2_base64('43873_left.jpeg')
    return (getRetinopathyLevel(image_64_encode))

#testImage()

class Startegy3Model:
    def test():
        image_64_encode = cvt_2_base64('43873_left.jpeg')
        return (getRetinopathyLevel(image_64_encode))