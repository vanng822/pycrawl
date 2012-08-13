import os
import hashlib

class StaticHash(object):
    def __init__(self, path, filetype):
        self.path = path
        self.filetype = filetype
        self.entries = {}
        
    def get_cache(self, path):
        return None
    
    def fetch(self):
        if self.get_cache(self.path) is not None:
            return
        for filename in os.listdir(self.path):
            _, ext = os.path.splitext(filename)
            if ext == self.filetype:
                self.entries.update({filename: self.md5sum(self.path + '/' + filename) + self.filetype})
          
    def md5sum(self, filename):
        md5 = hashlib.md5()
        
        with open(filename, 'rb') as f:
            buf = f.read(md5.block_size)
            while len(buf) > 0:
                md5.update(buf)
                buf = f.read(md5.block_size)
        
        return md5.hexdigest()
          
    def get(self, filename):
        return self.entries.get(filename)
