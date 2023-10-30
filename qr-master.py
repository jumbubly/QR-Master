import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QDialog, QTextBrowser, QHBoxLayout, QMenuBar
from PyQt6.QtGui import QPixmap, QAction, QClipboard
import qrcode
from io import BytesIO

class QRMaster(QMainWindow):
    QR_VERSION = 1
    QR_BOX_SIZE = 10
    QR_BORDER = 5
    INITIAL_SIZE = (400, 250)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Master - Custom QR Code Generator")
        self.setGeometry(100, 100, *self.INITIAL_SIZE)
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        self.text_input = QLineEdit()
        generate_button = QPushButton("Generate QR Code")
        generate_button.clicked.connect(self.generate_qr_code)

        self.qr_label = QLabel()
        self.export_button = QPushButton("Export PNG")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_qr_code)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.clicked.connect(self.clear_ui)

        layout.addWidget(QLabel("Enter your text or link:"))
        layout.addWidget(self.text_input)
        layout.addWidget(generate_button)
        layout.addWidget(self.qr_label)
        layout.addWidget(self.export_button)
        layout.addWidget(self.clear_button)

        main_widget.setLayout(layout)
        self.generated_qr = None

        self.create_menus()

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        file_menu.addAction(about_action)

    def generate_qr_code(self):
        text = self.text_input.text()
        if text:
            qr = qrcode.QRCode(version=self.QR_VERSION, box_size=self.QR_BOX_SIZE, border=self.QR_BORDER)
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, "PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            self.qr_label.setPixmap(pixmap)

            self.generated_qr = img
            self.export_button.setEnabled(True)
            self.clear_button.setEnabled(True)

    def export_qr_code(self):
        if self.generated_qr:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save QR Code as PNG", "", "PNG Files (*.png);;All Files (*)")
            if file_name:
                try:
                    self.generated_qr.save(file_name, "PNG")
                    self.statusBar().showMessage("QR Code saved successfully.")
                except Exception as e:
                    self.statusBar().showMessage(f"Error: {str(e)}")

    def clear_ui(self):
        self.text_input.clear()
        self.qr_label.clear()
        self.export_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.generated_qr = None
        self.resize(*self.INITIAL_SIZE)

    def show_about_dialog(self):
        about_text = """QR Master - Custom QR Code Generator

Author: ReKing
GitHub: https://github.com/jumbubly
Cracked Account: https://cracked.io/rekingg
Bitcoin Code: bc1qadtnnc06hg3ekck785xxw4pmv89nfd2p5q7v3n

This tool allows you to generate custom QR codes from text or links. You can also export the QR codes as PNG images.

Version: 1.0"""
        about_dialog = AboutDialog(about_text, self)
        about_dialog.exec()

class AboutDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About QR Master")
        self.setGeometry(200, 200, 400, 200)
        layout = QVBoxLayout()
        about_text = QTextBrowser()
        about_text.setPlainText(text)

        layout.addWidget(about_text)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = QRMaster()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
