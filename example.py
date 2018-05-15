#Example script

import time
from JPEGCamera import JPEGCamera



camera = JPEGCamera("/dev/ttyUSB1")
nfile = "01.jpg"
camera.begin()
camera.reset()
time.sleep(3)
camera.takepicture()
camera.getsize()
camera.savePicture(nfile)
camera.show(nfile)
