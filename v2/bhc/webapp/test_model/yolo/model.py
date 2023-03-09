import torch
import argparse
import textwrap


def load_model(model_name):

    model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    return model


def get_pred(model_name, input):

    model = load_model(model_name)
    img = input

    result = model(img)

    return result




if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        ========== config your model ===========
        pretrained YOLOv5 detection models for test
        from pytorch-hub
        models list :
            * yolov5n (nano)
            * yolov5s (small)
            * yolov5m (medium)
            * yolov5l (large)
            * yolov5x (xlarge)
        
            
        '''))
    
    parser.add_argument(
        '--model_name',
        default='yolov5s',
        type=str,
        help='check models list'
    )
    parser.add_argument(
        '--input',
        default='test.jpg',
        type=str,
        help='./home/data/input.img'
    )
    args = parser.parse_args()
    print(args)

    input_path = './home/data/{input}'.format(input=args.input)
    pred = get_pred(args.model_name, input_path)

    pred.print()
    pred.show()