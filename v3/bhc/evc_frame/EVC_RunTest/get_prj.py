import os
import re

class git_downloader:


    def __init__(self, url=None, account=None):

        self.url = url
        self.account = account


    def clone(self):

        os.system('git clone {url}'.format(url=self.url))
        os.listdir()

    
    def get_path(self):
        
        p_repo = re.compile("\/{account}\/.+\.git".format(account=self.account))
        repo = p_repo.findall(self.url)[0]
        repo = repo.replace('/', '')
        repo = repo.replace(self.account, '')
        repo = repo.replace('.git', '')
        
        return repo



if __name__ == "__main__":

    gd = git_downloader(
        url='https://github.com/ethicsense/EVC_test.git'
    )

    prj_name = gd.get_path()
    print(prj_name)