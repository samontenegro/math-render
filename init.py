from os import mkdir

BASE_PATH   = "assets"
IMG_PATH    = "/img"
VID_PATH    = "/vid"

def enum(value,pad):
    _valueString = str(value)
    if len(_valueString) > pad:
        pass
    else:
        while len(_valueString) < pad:
            _valueString = '0' + _valueString
        return _valueString

def init_directories():

    try:
        mkdir(BASE_PATH)
        print("Making base directory...")
    except FileExistsError:
        pass

    try:
        mkdir(BASE_PATH + IMG_PATH)
        print("Making image directory...")
    except FileExistsError:
        pass
    
    try:
        mkdir(BASE_PATH + VID_PATH)
        print("Making video directory...")
    except FileExistsError:
        pass

if __name__ == "__main__":
    pass
else:
    init_directories()