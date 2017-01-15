

"""
getprovinces

"""
import bisect
import pickle
import threading
import sys
import time
import numpy as np
from numpy import deg2rad


__init_flag__ = False

def init():
    '''''
    '''
    j = ['|', '/', '-', '\\']
    i = 0
    while not __init_flag__:
        sys.stdout.write(j[i%4]+" init\r")
        i = i + 1
        sys.stdout.flush()
        time.sleep(0.1)

threading.Thread(target=init).start()

__database__ = {
    'locations':pickle.load(file('locations.obj', 'rb')),
    'matrix':pickle.load(file('matrix.obj', 'rb')),
    # 'id_province':pickle.load(file('id_province.obj', 'rb')),
    'id_province':[u'\u6d77\u5357\u7701',\
                    u'\u5e7f\u4e1c\u7701',\
                    u'\u5e7f\u897f\u58ee\u65cf\u81ea\u6cbb\u533a',\
                    u'\u4e91\u5357\u7701',\
                    u'\u53f0\u6e7e\u7701',\
                    u'\u6fb3\u95e8\u7279\u522b\u884c\u653f\u533a',\
                    u'\u9999\u6e2f\u7279\u522b\u884c\u653f\u533a',\
                    u'\u798f\u5efa\u7701',\
                    u'\u6c5f\u897f\u7701',\
                    u'\u8d35\u5dde\u7701',\
                    u'\u6e56\u5357\u7701',\
                    u'\u56db\u5ddd\u7701',\
                    u'\u897f\u85cf\u81ea\u6cbb\u533a',\
                    u'\u6d59\u6c5f\u7701',\
                    u'\u91cd\u5e86\u5e02',\
                    u'\u6e56\u5317\u7701',\
                    u'\u5b89\u5fbd\u7701',\
                    u'\u4e0a\u6d77\u5e02',\
                    u'\u6c5f\u82cf\u7701',\
                    u'\u6cb3\u5357\u7701',\
                    u'\u9752\u6d77\u7701',\
                    u'\u9655\u897f\u7701',\
                    u'\u7518\u8083\u7701',\
                    u'\u65b0\u7586\u7ef4\u543e\u5c14\u81ea\u6cbb\u533a',\
                    u'\u5c71\u4e1c\u7701',\
                    u'\u5c71\u897f\u7701',\
                    u'\u5b81\u590f\u56de\u65cf\u81ea\u6cbb\u533a',\
                    u'\u6cb3\u5317\u7701',\
                    u'\u5185\u8499\u53e4\u81ea\u6cbb\u533a',\
                    u'\u8fbd\u5b81\u7701',\
                    u'\u5929\u6d25\u5e02',\
                    u'\u5317\u4eac\u5e02',\
                    u'\u5409\u6797\u7701',\
                    u'\u9ed1\u9f99\u6c5f\u7701']
}
__database__['lats'] = sorted(__database__['locations'].keys())
__init_flag__ = True

def get_centre(lat, lng):
    '''''
    '''
    #deal lat
    left_lat_index = bisect.bisect_left(__database__['lats'], lat)
    left_lat = __database__['lats'][left_lat_index]
    right_lat = __database__['lats'][left_lat_index + 1]
    mlat = right_lat if (right_lat - lat) < (lat - left_lat) else left_lat
    #deal lng
    lng_coordinate = dict(__database__['locations'][mlat])
    lngs = sorted(lng_coordinate.keys())
    left_lng_index = bisect.bisect_left(lngs, lng)
    left_lng = lngs[left_lng_index]
    right_lng = lngs[left_lng_index + 1]
    mlng = right_lng if (right_lng - lng) < (lng - left_lng) else left_lng

    centre = lng_coordinate[mlng]

    # print str((lat, lng)) + ' coordinate is ' + str(centre)
    return centre

def sector_mask(shape, centre, radius, angle_range):
    """
    Return a boolean mask for a circular sector. The start/stop angles in
    `angle_range` should be given in clockwise order.
    """

    x,y = np.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin, tmax = deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin:
        tmax += 2*np.pi

    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = np.arctan2(x-cx,y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)

    # circular mask
    circmask = r2 <= radius*radius

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask*anglemask

def get_provinces():
    '''''
    '''
    # print 'success'
    # from matplotlib import pyplot as pp

    lat = float(raw_input(u'input lat(>3.91 & < 53.5): '))
    lng = float(raw_input(u'input lng(>73.6 & < 135): '))
    radius = float(raw_input(u'input radius: '))
    try:
        print 'centre is ' + str((lat, lng)) + ' radius is ' + str(radius) + ' km'
        matrix = pickle.load(file('matrix.obj', 'rb'))
        mask = sector_mask(matrix.shape, get_centre(lat, lng), radius/5, (0, 360))
        matrix[~mask] = -1
        idset = set()
        for row in matrix:
            idset = idset|set(row)
        # return [__database__['id_province'][item] for item in idset if item != -1]
        # print idset
        for item in idset:
            if item != -1:
                print __database__['id_province'][item]
    except:
        print 'please input correct format'

if __name__ == "__main__":
    while 1:
        get_provinces()

