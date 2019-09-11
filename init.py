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
        print("Making base directory...")
        mkdir(BASE_PATH)
    except FileExistsError:
        pass

    try:
        print("Making image directory...")
        mkdir(BASE_PATH + IMG_PATH)
    except FileExistsError:
        pass
    
    try:
        print("Making video directory...")
        mkdir(BASE_PATH + VID_PATH)
    except FileExistsError:
        pass

if __name__ == "__main__":
    pass
else:
    init_directories()