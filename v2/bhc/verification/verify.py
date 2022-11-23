from bs4 import BeautifulSoup as bs
import requests
import argpaser

def main():

    reg_url = args.url
    arch = args.arch
    task = args.task

    search = requests.get('{url}/v2/_catalog'.format(url=reg_url))
    print(search.text)
    model = "{arch}-model".format(arch=arch)

    if model in search.text:
        search2 = requests.get('{url}/v2/{model}/tags/list'.format(url=reg_url, model=model))
        print(search2.text)
        if task in search2.text:
            image_name = "{model}:{task}".format(model=model, task=task)
            print('we already have the model.')
            print("download command : 'docker pull {url}/{image_name}'".format(url=reg_url, image_name=image_name))
        else:
            print('activate distribution sequence.')


if __name__ == "__main__" :

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        ========== config your model ===========

        * arch : your CPU architecture
        * type : your model's task
        * url : docker registry address

        '''))
    parser.add_argument(
        '--url',
        default='localhost:5000',
        type=str,
        help='default : localhost:5000'
    )

    parser.add_argument(
        '--arch',
        type=str,
        help='look up your CPU architecture using "$ uname -a"'
    )
    parser.add_argument(
        '--task',
        type=str,
        help='what is the purpose of this model? [ ex) animal, fruit, cars, etc... ]'
    )

    args = parser.parse_args()
    print(args)

    
    main()