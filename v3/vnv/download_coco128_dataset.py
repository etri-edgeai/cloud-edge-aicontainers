#------------------------------------------------------
# Config
#------------------------------------------------------

# Test images
zip_images_url = 'https://ultralytics.com/assets/coco128.zip'
dataset_root = './dataset'
fpath = dataset_root + '/coco128.zip'

#------------------------------------------------------
# Download data
#------------------------------------------------------
import os
#import urllib
import urllib.request as urllib

# make download directory
def makedir(path): 
    isdir = os.path.isdir(path)
    
    try: 
        os.makedirs(path)
    except OSError: 
        if not isdir: 
            raise
    return os.path.abspath(path), isdir

# Download images
d, isdir = makedir(dataset_root) # 저장 공간 생성

if isdir:
    url, fname = (zip_images_url, fpath)
    isfile_exist = os.path.exists(os.path.join(os.getcwd(), fname))
    
    print('downloading...')
    if not isfile_exist:
        try: 
            urllib.URLopener().retrieve(url, fname)
        except: 
            urllib.urlretrieve(url, fname)
        print('[+] download completed.')
        
        # Unzip
        cmd = 'unzip ' + fpath + ' -d ' + dataset_root
        print(cmd)
        os.system(cmd)
    else:
        print('[+] download skipped ')

