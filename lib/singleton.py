
def singleton(cls):
    __instances = {}
    def getinstance():
        if cls not in __instances:
            __instances[cls] = cls()
        return __instances[cls]
    
    return getinstance
