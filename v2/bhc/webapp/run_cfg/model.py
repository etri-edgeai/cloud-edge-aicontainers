## AI model for yaml cfg test
## yolov8

from ultralytics import YOLO
import argparse
import textwrap

class plate_detector:

    def __init__(self, model, data, url=None, project=None, name=None):

        self.model = YOLO(model)
        self.data = data
        self.url = url
        self.project = project
        self.name = name

    
    def train(self, epochs, batch):
    
        # add arguments as you like
        self.model.train(
            data=self.data,
            epochs=epochs,
            batch=batch
        )


    def pred(self, project, name):

        if self.data:
            result = self.model.predict(self.data, save=args.save, project=self.project, name=self.name)

        elif self.url:
            result = self.model(self.url, stream=True, project=self.project, name=self.name)
        
        return result
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            
            YOLOv8 Car License-Plate Detector v1.0

            Functions : 
                Train model
                Car lincense-plate detection

            Train notice : 
                you have to write dataset config .yaml format file.

                you have to reconstruct your dataset into yolov5 format.

                you have to edit codes below self.model.train() in order to manipulate any hyper-parameters.

                results saved in project/name/predict/...
                    default : runs/task(i.e. detect)/predict/...

                detailed informations about model :
                    https://docs.ultralytics.com/modes/
         
        
        ''')
    )
    parser.add_argument(
        '--model',
        type=str,
        default='/home/pd_base.pt',
        help='model file'
    )
    parser.add_argument(
        '--data',
        type=str,
        default='/home/data/test.jpg',
        help='data path'
    )
    parser.add_argument(
        '--save',
        type=bool,
        default=True,
        help='whether save results'
    )
    parser.add_argument(
        '--mod',
        type=str,
        default='pred',
        help='select mode (train, pred, result)'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=10,
        help='train epochs'
    )
    parser.add_argument(
        '--batch',
        type=float,
        default=8,
        help='train batch size'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='predict input url'
    )
    parser.add_argument(
        '--project',
        type=str,
        help='name of project (parent dir)'
    )
    parser.add_argument(
        '--name',
        type=str,
        help='name of work (current dir)'
    )
    args = parser.parse_args()

    pd = plate_detector(
        args.model,
        args.data
    )

    if args.mod == 'train':
        pd.train(args.epochs, args.batch)
    
    elif args.mod == 'pred':
        output = pd.pred()
        print(output)

    elif args.mod == 'result':
        pd.get_result()