#!/usr/bin/env python3

from process_tools import *
from functools import partial

# Import Qt libs
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.caption_max_width = 240
        self.label_max_height = 16
        self.files = {}
        self.location_fields = {}
        self.captions = {}

        # Global elements
        self.files_layout = QtWidgets.QVBoxLayout()
        self.add_more = QtWidgets.QPushButton("+ Add more")
        self.add_more.clicked.connect(self.add_file)
        self.clear_button = QtWidgets.QPushButton("Clear everything")
        self.clear_button.clicked.connect(self.clear_fields)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_more)
        self.buttons_layout.addWidget(self.clear_button)
        self.process_files = QtWidgets.QPushButton("Process files")
        self.process_files.clicked.connect(self.start_processing)
        self.message = QtWidgets.QLabel("Processing files...")
        self.message.hide()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.files_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.process_files)
        self.layout.addWidget(self.message)

    @QtCore.Slot()
    def add_file(self):
        file_num = len(self.files) + 1
        self.files[file_num] = self.generate_line(file_num)

        if self.files:
            for line in self.files.values():
                self.files_layout.addLayout(line)

    @QtCore.Slot()
    def generate_line(self, number):
        # Single line with text and "browse" button
        field_label = QtWidgets.QLabel(f"File or folder {number}")
        field_label.setMaximumHeight(self.label_max_height)

        self.captions[number] = QtWidgets.QLineEdit()
        self.captions[number].setPlaceholderText("Caption (optional). If provided need to set caption to every file")
        self.captions[number].setMaximumWidth(self.caption_max_width)

        self.location_fields[number] = QtWidgets.QLineEdit()
        self.location_fields[number].setObjectName(f"file_location_{number}")
        self.location_fields[number].setPlaceholderText(f"Select folder or single file {number}, or just put location here")

        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.setObjectName(f"file_button_{number}")
        browse_button.clicked.connect(partial(self.get_files, number))

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setMaximumHeight(2)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName(f"line_{number}")
        horizontal_layout.addWidget(self.location_fields[number])
        horizontal_layout.addWidget(self.captions[number])
        horizontal_layout.addWidget(browse_button)

        new_layout = QtWidgets.QVBoxLayout()
        new_layout.addWidget(field_label)
        new_layout.addLayout(horizontal_layout)
        new_layout.addWidget(line)
        new_layout.setAlignment(QtCore.Qt.AlignTop)

        return new_layout

    @QtCore.Slot()
    def get_files(self, number):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # dlg.setFilter("Text files (*.txt)")
        if dlg.exec():
            filenames = dlg.selectedFiles()
            self.location_fields[number].setText(filenames[0])
            # self.locations[number] = filenames[0]
            print(number, filenames[0])
            return filenames

    @QtCore.Slot()
    def start_processing(self):
        self.message.show()
        locations = [i.text() for i in list(self.location_fields.values())]
        captions = [i.text() for i in list(self.captions.values())]
        captions = captions if captions[0] else None
        process_files(locations, captions)
        self.message.setText("Processing finished!")

    @QtCore.Slot()
    def clear_fields(self):
        for field in self.location_fields.values():
            field.setText("")
            self.location_fields = {}
        for caption in self.captions.values():
            caption.setText("")
            self.captions = {}

        self.message.show()
        self.message.setText("Everything cleaned :)")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 200)
    widget.add_file()
    widget.add_file()
    widget.show()

    sys.exit(app.exec())