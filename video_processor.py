#!/usr/bin/python

#
# Color thresholds in OpenCV
# http://www.aishack.in/2010/07/tracking-colored-objects-in-opencv/
#
# load an image, convert to HSV color space, and threshold the image
# for yellow hue values 
#

import cv

class QRDecoder:
	def __init__(self,file_name):
		# Threshholds
		self.green_lower = cv.Scalar(40,100,100)
		self.green_upper = cv.Scalar(75,255,255)
		self.blue_lower = cv.Scalar(100,100,100)
		self.blue_upper = cv.Scalar(130,255,255)

		# create windows for displaying our results
		self.original_window = "original image"
		cv.NamedWindow(self.original_window, cv.CV_WINDOW_AUTOSIZE)
		self.green_window = "green threshed"
		cv.NamedWindow(self.green_window, cv.CV_WINDOW_AUTOSIZE)
		self.blue_window = "blue theshed"
		cv.NamedWindow(self.blue_window, cv.CV_WINDOW_AUTOSIZE)

		# create our image from a file
		self.image = cv.LoadImage(file_name, cv.CV_LOAD_IMAGE_COLOR)

		# convert the original image into HSV
		self.image_hsv = cv.CreateImage(cv.GetSize(self.image), self.image.depth, 3)
		cv.CvtColor(self.image, self.image_hsv, cv.CV_BGR2HSV)

		# showing original
		cv.ShowImage('original image', self.image)		

	def threshhold_amount(self,lower,upper,window):
		# create the placeholder for thresholded image
		channels = 1
		image_threshed = cv.CreateImage(cv.GetSize(self.image), self.image.depth, channels)

		# do the actual thresholding
		cv.InRangeS(self.image_hsv, lower, upper, image_threshed)

		# show the images
		cv.ShowImage(window, image_threshed)

		return cv.CountNonZero(image_threshed)

	def green_amount(self):
		return self.threshhold_amount(self.green_lower,self.green_upper,self.green_window)

	def blue_amount(self):
		return self.threshhold_amount(self.blue_lower,self.blue_upper,self.blue_window)


if __name__ == "__main__":
	qrd = QRDecoder('cat.jpg')

	print "green amount: %d" % qrd.green_amount()
	print "blue amount: %d" % qrd.blue_amount() 

	cv.WaitKey(10000)
