class Config(object):

    # objects more distant than this will be eliminated
    distance_thres = 1500
    
    # objects smaller than this area will be eliminated
    min_area = 1400

    # for opening on image
    open_kernel = (15,15)

    # crop ground, the lower 0.25 part on the depth image will be masked.
    crop_ground = 0.25

config = Config()