#this gets a list of the files
import os

# read the files. Takes three parameters. A pathname, a list of extensions.
# to contain returned file names.
class filewalker():

    def gettargetfiles(self, contentPath):
        '''with a pathname returns a list of files.'''
        filelist = []
        extensiontargets = [".js"]
        for root, dirs, files in os.walk(contentPath):
            for f in files:
                filename = os.path.join(root,f)
                fileextension = filename[-3:]
                for i in range(len(extensiontargets)):
                    if extensiontargets[i] == fileextension:
                        filelist.append(filename)
        return filelist

