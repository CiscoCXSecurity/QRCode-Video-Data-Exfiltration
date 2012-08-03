#QRCode-Video-Data-Exfiltration#

Exfiltrate data with QR code videos generated from files by HTML5/JS.

## Data => QR Code Video ##
Host the files in the folder labled `file_to_qr` on a web server. Visit the web server. Drag and drop a file into the browser window where it says `Drop files here...`. A video of QR codes should start flashing.

Point a cellphone camera or other video capture device at the screen and record. Make sure to record until you have seen the blue flash twice. This will ensure that you have gotten all the data.

## QR Code Video => Data ##

First you need to convert the data to something that opencv will understand. See [this page](http://opencv.willowgarage.com/wiki/VideoCodecs) for information on compatible formats. I have found the following command to do the trick for me:

	mencoder ./foo.mov -ovc raw -vf format=i420 -nosound -o out.avi

Next, you will need to run this video through the processing script. **Remember to provide the full path to the video rather than the relative path**. Blame opencv for this, not me. This should look like:

	python ./video_processor.py /home/mastahyeti/out.avi

You should see a bunch of stuff about frames and what-not. Unless you see any errors, this ins't too important. At the end you should see your previous data. 

## Dependancies ##
pyopencv

	sudo pip install pyopencv

zbar

	sudo pip install zbar

## Notes ##

- If you plan to use this in the wild, you might want to consider packing/obfuscating the HTML/JS used for creating the video to avoid detection.

## Author ##

Ben Toews (@mastahyeti)

## Credits ##

- Idea stolen from Michael Pearce
- Greg Ose
- http://www.aishack.in/2010/07/tracking-colored-objects-in-opencv/
- http://sourceforge.net/apps/mediawiki/zbar/index.php?title=HOWTO:_Scan_images_using_the_API

