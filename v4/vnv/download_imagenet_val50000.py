#------------------------------------------------------
# Config
#------------------------------------------------------

# Test images
zip_images_url = 'http://keticmr.iptime.org:22080/edgeai/images/ILSVRC2012_img_val.tar'
zip_images = 'imagenet-val.tar'
dataset_root = './dataset'
fpath_zip_images = dataset_root + '/' + zip_images
fpath_testimages = dataset_root + '/imagenet-val/'

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
    url, fname = (zip_images_url, fpath_zip_images)
    isfile_exist = os.path.exists(os.path.join(os.getcwd(), fname))
    
    print('downloading...')
    if not isfile_exist:
        try: 
            urllib.URLopener().retrieve(url, fname)
        except: 
            urllib.urlretrieve(url, fname)
        print('[+] download completed.')
        # Unzip
        cmd = 'tar -zxvf ' + fpath_zip_images + ' -d ' + dataset_root
        print(cmd)
        os.system(cmd)
    else:
        print('[+] download skipped ')


from glob import iglob

'''
# read test files
testfiles = []
for fname in sorted( iglob(fpath_testimages + '**/*.JPEG', recursive=True) ):
    testfiles.append(fname)
'''

idx_gt = []
idx = 0
testfiles = []
for d in sorted( iglob(fpath_testimages + 'n*', recursive=False) ):
    for fname in sorted( iglob(d + '/*.JPEG', recursive=True) ):
        testfiles.append(fname)
        idx_gt.append( idx )
    idx += 1

# Read the categories
with open("imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]