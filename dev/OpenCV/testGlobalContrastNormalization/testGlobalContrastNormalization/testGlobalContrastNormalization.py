# http://www.cellstat.net/std/

import cv2
import numpy as np
import scipy
import scipy.misc
from PIL import Image


def global_contrast_normalization(filename, outpath, epsilon=0.000000001 ):

    x = cv2.imread( filename, cv2.IMREAD_COLOR ).astype(np.float32)
    #x = np.array(Image.open(filename)).astype(np.float32)

    #print( str(x.mean()), ',', str(x.std()) )
    x =( x - np.mean(x) ) / max(np.std(x), epsilon) * 64 + 128#16  + 64
    print( str(x.mean()), ',', str(x.std()) )

    ## scipy can handle it
    #scipy.misc.imsave( outpath, x )
    cv2.imwrite( outpath, x)



#global_contrast_normalization( 'mri1.png', 'mri1_out.png' )
#global_contrast_normalization( 'mri2.png', 'mri2_out.png' )
#global_contrast_normalization( 'mri3.png', 'mri3_out.png' )
#global_contrast_normalization( 'cat.jpg', 'cat_out.png' )
#global_contrast_normalization( 'cat2.jpg', 'cat_out2.png' )
global_contrast_normalization( '20141125234825.png', '20141125234825_out.png' )
global_contrast_normalization( '20141125234831.png', '20141125234831_out.png' )



#import cv2
#import numpy as np
#from matplotlib import pyplot as plt
#import matplotlib
#plt.figure(figsize=(20,20))

#for i in range(1,4):
#    img = cv2.imread("mri"+str(i)+".png",0)
    
#    plt.subplot(4, 3, i)
#    plt.imshow(img,clim=[0,255])
#    plt.colorbar()
#    plt.subplot(4, 3, i+3)
#    plt.imshow(cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_GRAY2BGR))
#    plt.colorbar()
    
#    print( np.mean(img), np.std(img) )
#    img = (img - np.mean(img))/np.std(img)*16+64
    
#    plt.subplot(4, 3, i+6)
#    plt.imshow(img,clim=[0,255])
#    plt.colorbar()
#    plt.subplot(4, 3, i+9)
#    plt.imshow(cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_GRAY2BGR))
#    plt.colorbar()

#plt.show()