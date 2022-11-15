import tensorflow.keras.applications as kerasapp
from tensorflow.keras.preprocessing import image

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

warnings.filterwarnings("ignore")


def model_selection():
    ## import model
    model_type = str(input('insert your model : '))
    if model_type == 'Xception':
        model = kerasapp.ResNet50(weights='imagenet')
    elif model_type == 'VGG16':
        model = kerasapp.VGG16(weights='imagenet')
    elif model_type == 'VGG19':
        model = kerasapp.VGG19(weights='imagenet')
    elif model_type == 'ResNet50':
        model = kerasapp.ResNet50(weights='imagenet')
    elif model_type == 'ResNet50V2':
        model = kerasapp.ResNet50V2(weights='imagenet')
    elif model_type == 'ResNet52':
        model = kerasapp.ResNet52(weights='imagenet')
    elif model_type == 'ResNet52V2':
        model = kerasapp.ResNet52V2(weights='imagenet')
    elif model_type == 'ResNet101':
        model = kerasapp.ResNet101(weights='imagenet')
    elif model_type == 'ResNet101V2':
        model = kerasapp.ResNet101V2(weights='imagenet')
    elif model_type == 'ResNet152':
        model = kerasapp.ResNet152(weights='imagenet')
    elif model_type == 'ResNet152V2':
        model = kerasapp.ResNet152V2(weights='imagenet')
    elif model_type == 'InceptionV3':
        model = kerasapp.InceptionV3(weights='imagenet')
    elif model_type == 'InceptionResNetV2':
        model = kerasapp.InceptionResNetV2(weights='imagenet')
    elif model_type == 'MobileNet':
        model = kerasapp.MobileNet(weights='imagenet')
    elif model_type == 'MobileNetV2':
        model = kerasapp.MobileNetV2(weights='imagenet')
    elif model_type == 'DenseNet121':
        model = kerasapp.DenseNet121(weights='imagenet')
    elif model_type == 'DenseNet169':
        model = kerasapp.DenseNet169(weights='imagenet')
    elif model_type == 'DenseNet201':
        model = kerasapp.DenseNet201(weights='imagenet')
    elif model_type == 'NASNetMobile':
        model = kerasapp.NASNetMobile(weights='imagenet')
    elif model_type == 'NASNetLarge':
        model = kerasapp.NASNetLarge(weights='imagenet')
    elif model_type == 'EfficientNetB0':
        model = kerasapp.EfficientNetB0(weights='imagenet')
    elif model_type == 'EfficientNetB1':
        model = kerasapp.EfficientNetB1(weights='imagenet')
    elif model_type == 'EfficientNetB2':
        model = kerasapp.EfficientNetB2(weights='imagenet')
    elif model_type == 'EfficientNetB3':
        model = kerasapp.EfficientNetB3(weights='imagenet')
    elif model_type == 'EfficientNetB4':
        model = kerasapp.EfficientNetB4(weights='imagenet')
    elif model_type == 'EfficientNetB5':
        model = kerasapp.EfficientNetB5(weights='imagenet')
    elif model_type == 'EfficientNetB6':
        model = kerasapp.EfficientNetB6(weights='imagenet')
    elif model_type == 'EfficientNetB7':
        model = kerasapp.EfficientNetB7(weights='imagenet')
    elif model_type == 'EfficientNetV2B0':
        model = kerasapp.EfficientNetV2B0(weights='imagenet')
    elif model_type == 'EfficientNetV2B1':
        model = kerasapp.EfficientNetV2B1(weights='imagenet')
    elif model_type == 'EfficientNetV2B2':
        model = kerasapp.EfficientNetV2B2(weights='imagenet')
    elif model_type == 'EfficientNetV2B3':
        model = kerasapp.EfficientNetV2B3(weights='imagenet')
    elif model_type == 'EfficientNetV2S':
        model = kerasapp.EfficientNetV2S(weights='imagenet')
    elif model_type == 'EfficientNetV2BM':
        model = kerasapp.ResNet101(weights='imagenet')
    elif model_type == 'EfficientNetV2BL':
        model = kerasapp.EfficientNetV2BL(weights='imagenet')
    elif model_type == 'ConvNeXtTiny':
        model = kerasapp.ConvNeXtTiny(weights='imagenet')
    elif model_type == 'ConvNeXtSmall':
        model = kerasapp.ConvNeXtSmall(weights='imagenet')
    elif model_type == 'ConvNeXtBase':
        model = kerasapp.ConvNeXtBase(weights='imagenet')
    elif model_type == 'ConvNeXtLarge':
        model = kerasapp.ConvNeXtLarge(weights='imagenet')
    elif model_type == 'ConvNeXtXLarge':
        model = kerasapp.ConvNeXtXLarge(weights='imagenet')


def pred():
    ## data preprocessing
    img_path = 'data/island2.jpeg'
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    ## get prediction
    preds = model.predict(x)

    ## output origin image & top x predictions

    ## origin image
    data = plt.imread(img_path)
    plt.imshow(data)
    # image = Image.open(img_path)
    # image.show()

    ## top 5
    print('Prediction : ', decode_predictions(preds, top=5)[0])

