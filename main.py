import subprocess
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

class VideoDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(440, 419)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")


        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 10, 441, 361))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")


        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(0, 10, 441, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")


        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(0, 70, 441, 21))
        self.lineEdit.setObjectName("lineEdit")


        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 50, 441, 16))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")


        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(0, 110, 441, 16))
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")


        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(0, 130, 441, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")

        #container log
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(0, 190, 441, 171))
        self.textEdit.setFrameShape(QtWidgets.QFrame.VLine)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("color: red;")



        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(0, 170, 441, 21))
        self.label_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        #start downlaod
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 380, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.download_video)


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 380, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openDialog)
        self.setCentralWidget(self.centralwidget)


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


        self.show()

    Path_ = ""
    def openDialog(self):
        global Path_
        file_dialog = QFileDialog()
        path = file_dialog.getExistingDirectory(self, 'Select Directory')
        Path_ = path
        self.textEdit.append("PATH: "+Path_)
        print("Selected Path:", path)  # You can replace this line with your desired logic

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Video Downloader"))
        self.label.setText(_translate("MainWindow", "Enter URL"))
        self.label_2.setText(_translate("MainWindow", "Referer"))
        self.label_3.setText(_translate("MainWindow", "Log"))

        self.pushButton.setText(_translate("MainWindow", "Download"))
        self.pushButton.clicked.connect(self.download_video)

        self.pushButton_2.setText(_translate("MainWindow", "Select Folder"))

    def download_video(self):
        self.pushButton.setEnabled(False)  # Disable the button during download
        global Path_
        input_url = self.lineEdit.text()
        output_file = Path_+"/"+"output.mp4"
        referer = self.lineEdit_2.text()
        input_params = {"headers": "Referer: " + referer}
        command = [
            "ffmpeg",
            "-headers",
            input_params["headers"],
            "-hwaccel",
            "videotoolbox",  # Specify VideoToolbox as the hardware acceleration
            "-i",
            input_url,
            "-c:v",
            "h264_videotoolbox",  # Specify VideoToolbox encoder
            output_file
        ]
        index_ = 0
        total_ = 0

        # Set total of URL
        response = requests.get(input_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Count the occurrences of "#EXTINF" in the response content
            count = response.text.count("#EXTINF")
            total_ = count
        else:
            self.textEdit.append("Failed to fetch the M3U8 file.")

        # Use subprocess.Popen to capture the output in real-time
        process = subprocess.Popen(command, stderr=subprocess.PIPE)
        # Read the output line by line
        for line in process.stderr:
            # Decode the line from bytes to string
            line = line.decode().strip()

            if line.endswith("for reading"):
                index_ += 1
                # Log percent of download
                percent = (index_ / total_) * 100
                percent = round(percent, 2)
                self.textEdit.append(str(line)+" "+"PERCENT: "+str(percent)+"%")
                self.update_progress(percent)

                if percent >= 100:
                    self.textEdit.append("SUCCESS")

        # Wait for the process to finish
        # process.wait()

        self.pushButton.setEnabled(True)  # Enable the button after download completes

    def update_progress(self, percent):
        self.progressBar.setValue(int(percent))
        QApplication.processEvents()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = VideoDownloader()
    sys.exit(app.exec_())