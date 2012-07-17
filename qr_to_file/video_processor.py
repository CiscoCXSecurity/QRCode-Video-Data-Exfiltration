#!/usr/bin/python

#
# Color thresholds in OpenCV
# http://www.aishack.in/2010/07/tracking-colored-objects-in-opencv/
#
# stealing the frame grabbing from http://stackoverflow.com/questions/4929721/opencv-python-grab-frames-from-a-video-file
#
# load an image, convert to HSV color space, and threshold the image
# for yellow hue values 
#

import cv
import sys
import zbar

# Threshholds
green_lower = cv.Scalar(40,100,100)
green_upper = cv.Scalar(75,255,255)
blue_lower = cv.Scalar(100,100,100)
blue_upper = cv.Scalar(130,255,255)

cv.NamedWindow("blah", cv.CV_WINDOW_AUTOSIZE)

def threshhold_amount(image,image_hsv,lower,upper):
    """
    determine how many pixels of an image are within a HSV threshhold
    """
    # create the placeholder for thresholded image
    channels = 1
    image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, channels)

    # do the actual thresholding
    cv.InRangeS(image_hsv, lower, upper, image_threshed)

    return cv.CountNonZero(image_threshed)


def green_amount(image,image_hsv):
    """
    Determine how many green pixels are in an image
    """
    return threshhold_amount(image,image_hsv,green_lower,green_upper)


def blue_amount(image,image_hsv):
    """
    Determine how many blue pixels are in an image
    """
    return threshhold_amount(image,image_hsv,blue_lower,blue_upper)


if __name__ == "__main__":
    fname = sys.argv[-1]

    thresholds = []
    str_frames = []

    capture = cv.CaptureFromFile(fname)

    frame_count = int(cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_COUNT))

    f = cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_POS_FRAMES)

    for i in range(frame_count):
        # bullshit to sync up our i with the actual frame
        while int(f) != i:
            f = cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_POS_FRAMES)
            cv.WaitKey(1)
            cv.QueryFrame(capture)

        # pull the current frame
        image = cv.QueryFrame(capture)

        # display current frame
        cv.ShowImage('foo',image)

        # convert current frame to HSV for colored frame detection
        image_hsv  = cv.CreateImage(cv.GetSize(image),image.depth,3)
        cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)

        # convert current frame to grayscale for zbar
        image_gray = cv.CreateImage(cv.GetSize(image),image.depth,1)
        cv.CvtColor(image, image_gray, cv.CV_BGR2GRAY)

        # calculate the amounts of different colors
        green = green_amount(image,image_hsv)
        blue = blue_amount(image,image_hsv)

        thresholds.append({'green':green,'blue':blue})

        # convert the frame to a string
        str_frames.append(image_gray.tostring())

        print "frame: %d\tgreen: %d\tblue: %d" % (f,green,blue)

    # what is the size of our imges
    height = image.height
    width = image.width
    pixel_count = height*width
    print "pixel count: %d" % pixel_count

    # figure out the middle of each streak of blue
    blues  = []
    i = 0
    while i < len(thresholds):
        # figure out how many of the next frames are blue
        j = 0
        while i+j < len(thresholds) and thresholds[i+j]['blue'] >= pixel_count/4:
            j += 1

        j -= 1

        # if any were blue
        if j >= 0:
            # we add the middle of the blue streak to our list
            blues.append(i+(j//2))

            # and skip over them in our processing
            i += j

        i += 1

    print "blues: %s" % str(blues)

    # figure out the middle of each streak of green
    greens  = []
    i = 0
    while i < len(thresholds):
        # figure out how many of the next frames are green
        j = 0
        while i+j < len(thresholds) and thresholds[i+j]['green'] >= pixel_count/4:
            j += 1

        j -= 1

        # if any were green
        if j >= 0:
            # we add the middle of the green streak to our list
            greens.append(i+(j//2))

            # and skip over them in our processing
            i += j

        i += 1

    print "greens: %s" % str(greens)

    # make sure they recorded long enough
    if blues < 2:
        quit('doesnt look like you recorded enough video. I only see one flash of blue....')

    
    # figure out one cycle of seperators
    seperators = [blues[0]]
    for sep in greens:
        if sep > blues[1]:
            break

        if sep > blues[0]:
            seperators.append(sep)

    seperators.append(blues[1])

    print "seperators: %s" % str(seperators)

    # figure out the key frames between the seperators
    keyframes = []
    for i in range(len(seperators)-1):
        middle = (seperators[i] + seperators[i+1])//2
        keyframes.append(middle)

    print "keyframes: %s" % str(keyframes)

    print "attempting scanning"

    # make the scanner
    scanner = zbar.ImageScanner()

    # configure the reader
    # scanner.set_config(64,0,1)
    # 64 = QRCODE
    scanner.set_config(64)

    output = ""

    for keyframe in keyframes:
        print "checking out keyframe: %d" % keyframe 
        # wrap image data
        # zimage = zbar.Image(width, height, 'I420', str_frames[keyframe])
        zimage = zbar.Image(width, height, 'Y800', str_frames[keyframe])

        # convert to a better format
        # zimage = zimage.convert('Y800')

        # scan the image for barcodes
        scanner.scan(zimage)

        if not len(scanner.results):
            print "error decoding from frame %d" % keyframe
            output += "**ERROR**"

        # extract results
        for symbol in scanner.results:
           output += symbol.data

        del(zimage)

print repr(output)