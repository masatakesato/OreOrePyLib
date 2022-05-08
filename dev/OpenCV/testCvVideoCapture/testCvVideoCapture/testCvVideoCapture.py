import numpy
import cv2


g_FrameColor = (225, 225, 225)
g_FrameThickness = 1
g_FrameCenterRadius = 5



def clamp( x, min_val, max_val ):
    return min(max(x, min_val),max_val)



def scaleCropRect( crop_size, crop_start, crop_end, cam_size, delta ):
    
    if( ( crop_start[0]<=0 or crop_start[1]<=0 or crop_end[0]>=cam_size[0] or crop_end[1]>=cam_size[1] ) and delta>0 ):
        return crop_size, crop_start, crop_end

    new_crop_size = ( int(clamp(crop_size[0] + 2*delta, 0, cam_size[0])), int(clamp(crop_size[1] + 2*delta, 0, cam_size[1])) )
    new_crop_start = ( crop_start[0] - delta, crop_start[1] - delta )
    new_crop_end = ( crop_end[0] + delta, crop_end[1] + delta )

    print( 'set crop size:(' + str(new_crop_size[0]) + ', ' + str(new_crop_size[1]) + ')' )

    return new_crop_size, new_crop_start, new_crop_end



def moveCropRect( crop_center, crop_start, crop_end, cam_size, delta ):

    if( (crop_start[0]<=0 and delta[0]<0) or (crop_start[1]<=0 and delta[1]<0) or
        (crop_end[0]>=cam_size[0] and delta[0]>0) or (crop_end[1]>=cam_size[1] and delta[1]>0) ):
        return crop_center, crop_start, crop_end

    new_crop_center = ( crop_center[0] + delta[0], crop_center[1] + delta[1] )
    new_crop_start = ( crop_start[0] + delta[0], crop_start[1] + delta[1] )
    new_crop_end = ( crop_end[0] + delta[0], crop_end[1] + delta[1] )

    print( 'set center:(' + str(new_crop_center[0]) + ', ' + str(new_crop_center[1]) + ')' )

    return new_crop_center, new_crop_start, new_crop_end



def resetCropRect( cam_size, crop_size=None ):

    new_crop_size = None
    new_crop_center = None
    new_crop_start = None
    new_crop_end = None

    if( crop_size==None ):
        new_crop_size = cam_size
        new_crop_start = (0,0)
        new_crop_end = cam_size
    else:
        new_crop_size = ( int(clamp(crop_size[0], 0, cam_size[0])), int(clamp(crop_size[1], 0, cam_size[1])) )
        new_crop_start = ( int(clamp((cam_size[0]-crop_size[0])/2, 0, cam_size[0])), int(clamp((cam_size[1]-crop_size[1])/2, 0, cam_size[1])) )
        new_crop_end = ( clamp(new_crop_start[0]+crop_size[0], 0, cam_size[0]), clamp(new_crop_start[1]+crop_size[1], 0, cam_size[1]) )

    new_crop_center = ( int((new_crop_start[0]+new_crop_end[0])/2), int((new_crop_start[1]+new_crop_end[1])/2) )

    print( 'reset crop setteings...' )

    return new_crop_size, new_crop_center, new_crop_start, new_crop_end



def capture_camera( default_crop_size=(256, 256) ):
    """Capture video from c,amera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号
    cap.set( 3, 320 )
    cap.set( 4, 240 )


    if( cap.isOpened()==False ): 
        return

    cam_size = ( int(cap.get(3)), int(cap.get(4)) )
    crop_size = default_crop_size
    mirror = False

    bSizeSpecified = (crop_size != None and len(crop_size)==2)
    
    crop_size, crop_center, crop_start, crop_end = resetCropRect( cam_size, crop_size )


    print( 'cam_size:', cam_size[0], cam_size[1] )
    print( 'crop_size:', cam_size[0], cam_size[1] )


    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # mirroring on/off
        if mirror is True:
            frame = cv2.flip( frame, 1 )

        k = cv2.waitKey(25) # wait for 5ms
        if( k == 27 ): # esc key... quit
            break

        elif( k == 115 ): # s key.. capture image
            crop_img = frame[ crop_start[1]:crop_end[1], crop_start[0]:crop_end[0] ] if bSizeSpecified else frame # フレームをリサイズ
            cv2.imwrite( 'img.png', crop_img )
            print('image captured')

        elif( k == 2555904 ):# right key
            crop_center, crop_start, crop_end = moveCropRect( crop_center, crop_start, crop_end, cam_size, (1,0) )

        elif( k == 2424832 ):# left key
            crop_center, crop_start, crop_end = moveCropRect( crop_center, crop_start, crop_end, cam_size, (-1,0) )

        elif( k == 2490368 ):# up key
            crop_center, crop_start, crop_end = moveCropRect( crop_center, crop_start, crop_end, cam_size, (0,-1) )

        elif( k == 2621440 ):# down key
            crop_center, crop_start, crop_end = moveCropRect( crop_center, crop_start, crop_end, cam_size, (0,1) )

        elif( k == 114 ):# r key... reset
            crop_size, crop_center, crop_start, crop_end = resetCropRect( cam_size, default_crop_size )
            mirror= False

        elif( k == 109 ): # m key... mirror image
            mirror = not(mirror)
            print( 'set mirror mode: ', str(mirror) )

        elif( k == 43 ): # + key... expand crop area
            crop_size, crop_start, crop_end = scaleCropRect( crop_size, crop_start, crop_end, cam_size, 1 )

        elif( k == 45 ): # - key... shrink crop area
            crop_size, crop_start, crop_end = scaleCropRect( crop_size, crop_start, crop_end, cam_size, -1 )


        # フレームを表示する
        cv2.circle( frame, crop_center, g_FrameCenterRadius, g_FrameColor, g_FrameThickness )
        cv2.rectangle( frame, crop_start, crop_end, g_FrameColor, g_FrameThickness )
        cv2.imshow( 'camera capture', frame )

        

    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    capture_camera( default_crop_size=(128,128) )