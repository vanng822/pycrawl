
class CropParams(object):
    def __init__(self):
        self.top = 0
        self.left = 0
        self.right = 0
        self.bottom = 0
        
    def __str__(self):
        return 'top:{0},left:{1},right:{2},bottom:{3}'.format(self.top, self.left, self.right, self.bottom)

def get_crop_params(image_width, image_height, ratio):
    params = CropParams()
    
    image_ratio = (1.0 * image_width) / image_height
    
    # start with same size
    top = 0
    left = 0
    width = image_width
    height = image_height
    
    if ratio < image_ratio: # => width is larger than in the new ratio
        width = image_height * ratio
        left = (image_width - width) / 2
    elif ratio > image_ratio:
        height = image_width / ratio
        top = (image_height - height) / 2
    
    ## int or math.floor
    params.top = int(top)
    params.left = int(left)
    params.right = int(left + width)
    params.bottom = int(top + height)
    
    return params