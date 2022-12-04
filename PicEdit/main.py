import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Dialogue for opening files (and folders)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # needs a Qt.KeepAspectRatio constant to resize while maintaining proportions
from PyQt5.QtGui import QPixmap # screen-optimised
from PIL import Image, ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
app = QApplication([])
win = QWidget()  
win.resize(700, 500) 
win.setWindowTitle('Easy Editor')
 
## =Add Widgets =##
btn_dir = QPushButton("Folder")
list_files = QListWidget()
 
place_image = QLabel("Image will show here")
 
btn_left = QPushButton("Rotate Left")
btn_right = QPushButton("Rotate Right")
btn_mirror = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")
btn_blur = QPushButton("Blur")
btn_smooth = QPushButton("Smooth")
btn_detail = QPushButton("Detail")
btn_edge = QPushButton("Emboss")
btn_c = QPushButton("Emboss")
 
 
## =Add Layout =##
row = QHBoxLayout()        # Main line
 
col1 = QVBoxLayout()      # divided into two columns
col1.addWidget(btn_dir)      # in the first = directory selection button
col1.addWidget(list_files)     # and file list
 
col2 = QVBoxLayout()  
col2.addWidget(place_image, 95) # in the second = image
 
row_tools = QHBoxLayout()    # and button bar
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_smooth)
row_tools.addWidget(btn_detail)
row_tools.addWidget(btn_edge)
row_tools.addWidget(btn_c)
col2.addLayout(row_tools)
 
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
#info from os
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenameList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif',  '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)

 
win.show()
btn_dir.clicked.connect(showFilenameList)

#imgapge proseccer
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        place_image.hide()
        pixmapimage = QPixmap(path)
        w, h = place_image.width(), place_image.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        place_image.setPixmap(pixmapimage)
        place_image.show()

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_smooth(self):
        self.image = self.image.filter(SMOOTH)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_detail(self):
        self.image = self.image.filter(DETAIL)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_edge(self):
        self.image = self.image.filter(EMBOSS)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_c(self):
        self.image = self.image.filter(CONTOUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
workimage = ImageProcessor()

def showChosenImage():
    if list_files.currentRow() >= 0:
        filename= list_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

list_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_mirror.clicked.connect(workimage.do_flip)
btn_blur.clicked.connect(workimage.do_blur)
btn_smooth.clicked.connect(workimage.do_smooth)
btn_detail.clicked.connect(workimage.do_detail)
btn_edge.clicked.connect(workimage.do_edge)
btn_c.clicked.connect(workimage.do_c)
app.exec()