#converter.py
import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

class ConversionThread(QThread):
    progress = pyqtSignal(str)

    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        input_ext = os.path.splitext(self.input_file)[1]
        output_ext = os.path.splitext(self.output_file)[1]

        try:
            if input_ext == '.json':
                data = read_json(self.input_file)
            elif input_ext in ['.yml', '.yaml']:
                data = read_yaml(self.input_file)
            elif input_ext == '.xml':
                data = read_xml(self.input_file)

            if output_ext == '.json':
                write_json(data, self.output_file)
            elif output_ext in ['.yml', '.yaml']:
                write_yaml(data, self.output_file)
            elif output_ext == '.xml':
                write_xml(data, self.output_file)

            self.progress.emit('Conversion successful!')
        except Exception as e:
            self.progress.emit(f'Error: {str(e)}')

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def write_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, indent=4)

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = ET.tostring(root, encoding='unicode')
    return data

def write_xml(data, file_path):
    root = ET.fromstring(data)
    tree = ET.ElementTree(root)
    tree.write(file_path)

class ConverterUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('File Converter')

        self.label = QLabel('Choose files to convert', self)
        self.label.move(20, 20)

        self.btn_open = QPushButton('Open File', self)
        self.btn_open.move(20, 60)
        self.btn_open.clicked.connect(self.open_file_dialog)

        self.btn_save = QPushButton('Save File As', self)
        self.btn_save.move(150, 60)
        self.btn_save.clicked.connect(self.save_file_dialog)

        self.btn_convert = QPushButton('Convert', self)
        self.btn_convert.move(100, 120)
        self.btn_convert.clicked.connect(self.convert_file)

        self.input_file = None
        self.output_file = None

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;JSON Files (*.json);;YAML Files (*.yml *.yaml);;XML Files (*.xml)', options=options)
        if file:
            self.input_file = file
            self.label.setText(f'Input: {file}')

    def save_file_dialog(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'All Files (*);;JSON Files (*.json);;YAML Files (*.yml *.yaml);;XML Files (*.xml)', options=options)
        if file:
            self.output_file = file
            self.label.setText(f'Output: {file}')

    def convert_file(self):
        if not self.input_file or not self.output_file:
            self.label.setText('Error: Input and output files must be selected')
            return

        self.thread = ConversionThread(self.input_file, self.output_file)
        self.thread.progress.connect(self.update_label)
        self.thread.start()

    def update_label(self, message):
        self.label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConverterUI()
    ex.show()
    sys.exit(app.exec_())
