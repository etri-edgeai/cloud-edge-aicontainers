import tensorflow.keras.applications as kerasapp
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Input
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


def model_selection():

    ## get model name & change input layer
    model_type = str(input('insert your model : '))
    input_tensor = Input(shape=(224,224,3))

    ## load
    if model_type == 'Xception':
        model = kerasapp.ResNet50(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'VGG16':
        model = kerasapp.VGG16(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'VGG19':
        model = kerasapp.VGG19(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet50':
        model = kerasapp.ResNet50(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet50V2':
        model = kerasapp.ResNet50V2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet52':
        model = kerasapp.ResNet52(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet52V2':
        model = kerasapp.ResNet52V2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet101':
        model = kerasapp.ResNet101(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet101V2':
        model = kerasapp.ResNet101V2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet152':
        model = kerasapp.ResNet152(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ResNet152V2':
        model = kerasapp.ResNet152V2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'InceptionV3':
        model = kerasapp.InceptionV3(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'InceptionResNetV2':
        model = kerasapp.InceptionResNetV2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'MobileNet':
        model = kerasapp.MobileNet(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'MobileNetV2':
        model = kerasapp.MobileNetV2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'DenseNet121':
        model = kerasapp.DenseNet121(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'DenseNet169':
        model = kerasapp.DenseNet169(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'DenseNet201':
        model = kerasapp.DenseNet201(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'NASNetMobile':
        model = kerasapp.NASNetMobile(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'NASNetLarge':
        model = kerasapp.NASNetLarge(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB0':
        model = kerasapp.EfficientNetB0(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB1':
        model = kerasapp.EfficientNetB1(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB2':
        model = kerasapp.EfficientNetB2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB3':
        model = kerasapp.EfficientNetB3(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB4':
        model = kerasapp.EfficientNetB4(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB5':
        model = kerasapp.EfficientNetB5(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB6':
        model = kerasapp.EfficientNetB6(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetB7':
        model = kerasapp.EfficientNetB7(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2B0':
        model = kerasapp.EfficientNetV2B0(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2B1':
        model = kerasapp.EfficientNetV2B1(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2B2':
        model = kerasapp.EfficientNetV2B2(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2B3':
        model = kerasapp.EfficientNetV2B3(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2S':
        model = kerasapp.EfficientNetV2S(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2BM':
        model = kerasapp.ResNet101(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'EfficientNetV2BL':
        model = kerasapp.EfficientNetV2BL(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ConvNeXtTiny':
        model = kerasapp.ConvNeXtTiny(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ConvNeXtSmall':
        model = kerasapp.ConvNeXtSmall(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ConvNeXtBase':
        model = kerasapp.ConvNeXtBase(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ConvNeXtLarge':
        model = kerasapp.ConvNeXtLarge(input_tensor=input_tensor, weights='imagenet', include_top=True)
    elif model_type == 'ConvNeXtXLarge':
        model = kerasapp.ConvNeXtXLarge(input_tensor=input_tensor, weights='imagenet', include_top=True)
    
    return model


def pred():

    ## data preprocessing
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


if __name__ == "__main__" :
    
    model = model_selection()
    img_path = 'path'
    pred()
