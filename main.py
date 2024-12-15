import sys
import os
import shutil
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.start_program_button = QtWidgets.QPushButton("Start Program")
        self.upload_desktop_image_button = QtWidgets.QPushButton("Upload AFK Picture")
        self.upload_your_image_button = QtWidgets.QPushButton("Upload Your Picture")
        self.setup_face_recognition_button = QtWidgets.QPushButton("Setup Face Recognition")
        self.image_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.upload_desktop_image_button)
        self.layout.addWidget(self.upload_your_image_button)
        self.layout.addWidget(self.setup_face_recognition_button)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.start_program_button)

        self.start_program_button.clicked.connect(self.start_program)
        self.setup_face_recognition_button.clicked.connect(self.setup_face_recognition)
        self.upload_desktop_image_button.clicked.connect(lambda: self.upload_picture("AFK Poster"))
        self.upload_your_image_button.clicked.connect(lambda: self.upload_picture("Your Images"))

    @QtCore.Slot()
    def upload_picture(self, folder_name):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.review_selected_image(file_name, folder_name)

    @QtCore.Slot()
    def review_selected_image(self, file_name, folder_name):
        pixmap = QtGui.QPixmap(file_name)
        review = QMessageBox(self)
        review.setIconPixmap(pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio))
        review.setWindowTitle("Review Image")
        review.setText("Do you want to keep this image?")
        review.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel | QMessageBox.Retry)
        
        retval = review.exec()
        if retval == QMessageBox.Ok:
            #self.image_label.setPixmap
            self.copy_image_to_folder(file_name, folder_name)
        elif retval == QMessageBox.Retry:
            self.upload_picture(folder_name)

    def copy_image_to_folder(self, file_name, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        destination = os.path.join(folder_name, os.path.basename(file_name))
        shutil.copy(file_name, destination)

    @QtCore.Slot()
    def start_program(self):
        print("Program Started")

    @QtCore.Slot()
    def setup_face_recognition(self):
        print("Face Recognition Setup")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.showMaximized()
    widget.show()

    sys.exit(app.exec())