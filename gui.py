import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from index import *
from HatDetector import *

class picture(QWidget):
    pic_url = ""
    new_url = ""
    url_base = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, pic_url="", url_base = url_base):
        super(picture, self).__init__()

        self.hatDetector = HatDetector()
        # 获取绝对路径
        self.url = url_base
        for i in url_base:
            if(i == "\\"):
                self.url = self.url + "/"

        self.new_url = ""

        self.pic_url = pic_url
        self.resize(800, 600)
        self.setWindowTitle("label显示图片")
        
        self.res = QLabel(self)
        self.res.setText("")
        self.res.setFixedSize(600, 15)

        
        # 显示图片区域
        self.label = QLabel(self)
        self.label.setText("   显示图片")
        self.label.setFixedSize(600, 400)
        self.label.move(100, 60)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:black;font-size:20px;font-weight:bold;font-family:宋体;}"
                                 )

        # 选择图片的按钮
        self.chooseBtn = QPushButton(self)
        self.chooseBtn.setText("选择图片")
        self.chooseBtn.move(100, 500)
        self.chooseBtn.setStyleSheet("QPushButton:chooseBtn{background:#33D1FF;}")
        self.chooseBtn.clicked.connect(self.openimage)

        uploadBtn = QPushButton(self)
        uploadBtn.setText("上传图片")
        uploadBtn.move(500, 500)
        uploadBtn.clicked.connect(self.uploadimage)

    # 打开图片的函数
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        self.show_pic(imgName)
        self.pic_url = imgName

    # 上传图片的函数
    def uploadimage(self):
        button=QMessageBox.question(self,"Question",  
                                    self.tr("确认上传?"),  
                                    QMessageBox.Ok|QMessageBox.Cancel,  
                                    QMessageBox.Ok)  
        if button==QMessageBox.Ok:  
            self.res.setText("上传成功！请等待检测结果！") 
            self.detect()
        elif button==QMessageBox.Cancel:  
            self.label.setText("上传失败。请重新选择图片！")  
        else:  
            return  

    # 显示测试完成的图片
    def detect(self):
        p_type = str(self.pic_url.split(".")[-1])
        # 调用检测函数,上传的图片地址为pic_url
        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.new_url = self.url + "resource/public/" + time_now + p_type
        # 缓冲图片
        loading = self.url+"resource/loading.gif"
        self.show_pic(loading)
        # 检测
        self.hatDetector.detectImageFile(self.pic_url, self.new_url)
        self.show_pic(self.new_url)

    def show_pic(self, show_url):
        resPic = QtGui.QPixmap(show_url).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(resPic)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    index = indexPage()
    my = picture()
    my.show()
    sys.exit(app.exec_())
