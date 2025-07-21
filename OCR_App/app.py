from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QFormLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import easyocr
import cv2
import sys


class IDCardWindow(QWidget):
    def __init__(self, reader):
        super().__init__()
        self.reader = reader
        self.setWindowTitle("🎓 Scan Student ID")
        self.setGeometry(150, 150, 400, 450)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.form_layout = QFormLayout()
        self.inputs = {
            "University Name": QLineEdit(),
            "Location": QLineEdit(),
            "Name": QLineEdit(),
            "Student Number": QLineEdit(),
            "Date": QLineEdit(),
        }

        for label, widget in self.inputs.items():
            widget.setStyleSheet(
                "background-color: #2c2c2c; color: white; border: 1px solid gray;"
            )
            self.form_layout.addRow(label, widget)

        self.image_label = QLabel("📤 No image uploaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(200)
        self.image_label.setStyleSheet("border: 1px solid gray;")

        self.upload_button = QPushButton("Upload ID Image")
        self.upload_button.setStyleSheet(self.button_style())
        self.upload_button.clicked.connect(self.load_and_process_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(self.form_layout)
        layout.addWidget(self.upload_button)
        self.setLayout(layout)

    def button_style(self):
        return """
            QPushButton {
                background-color: #007acc;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """

    def load_and_process_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open ID Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            pixmap = QPixmap(file_path).scaled(
                self.image_label.width(), 200, Qt.KeepAspectRatio
            )
            self.image_label.setPixmap(pixmap)

            results = self.reader.readtext(file_path)

            # Sort by top-to-bottom position (Y-axis)
            sorted_results = sorted(results, key=lambda x: x[0][0][1])
            texts = [text for _, text, _ in sorted_results]

            # Layout-based assignment:
            if len(texts) >= 5:
                self.inputs["University Name"].setText(texts[0])
                self.inputs["Location"].setText(texts[1])
                self.inputs["Name"].setText(texts[2])
                self.inputs["Student Number"].setText(texts[3])
                self.inputs["Date"].setText(texts[4])
            else:
                for key in self.inputs:
                    self.inputs[key].setText("Could not detect")


class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 OCR Dashboard")
        self.setGeometry(100, 100, 1220, 720)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.reader = easyocr.Reader(["en"])

        # Image label
        self.image_label = QLabel(self)
        self.image_label.setGeometry(20, 20, 700, 600)
        self.image_label.setStyleSheet(
            "border: 2px solid #444; background-color: #2c2c2c;"
        )

        # Text output
        self.text_output = QTextEdit(self)
        self.text_output.setGeometry(740, 20, 460, 600)
        self.text_output.setStyleSheet(
            """
            background-color: #2c2c2c;
            color: #dddddd;
            font-family: Consolas;
            font-size: 13px;
            border: 2px solid #444;
        """
        )

        self.upload_button = QPushButton("📤 Upload Image", self)
        self.upload_button.setGeometry(20, 640, 180, 40)
        self.upload_button.setStyleSheet(self.button_style())
        self.upload_button.clicked.connect(self.load_image)

        self.ocr_button = QPushButton("🔍 Scan", self)
        self.ocr_button.setGeometry(220, 640, 180, 40)
        self.ocr_button.setStyleSheet(self.button_style())
        self.ocr_button.clicked.connect(self.run_ocr)

        self.id_button = QPushButton("🎓 Scan ID Card", self)
        self.id_button.setGeometry(420, 640, 180, 40)
        self.id_button.setStyleSheet(self.button_style())
        self.id_button.clicked.connect(self.open_id_window)

        self.current_image_path = None

    def button_style(self):
        return """
            QPushButton {
                background-color: #007acc;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.current_image_path = file_path
            pixmap = QPixmap(file_path).scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
            )
            self.image_label.setPixmap(pixmap)
            self.text_output.clear()

    def run_ocr(self):
        if not self.current_image_path:
            self.text_output.setPlainText("No image loaded.")
            return

        results = self.reader.readtext(self.current_image_path)

        lines = []
        last_y = -100
        current_line = []

        for bbox, text, _ in results:
            y = bbox[0][1]
            if abs(y - last_y) > 15:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [text]
                last_y = y
            else:
                current_line.append(text)
        if current_line:
            lines.append(" ".join(current_line))

        full_text = "\n".join(lines)

        # Show text
        image = cv2.imread(self.current_image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for bbox, text, _ in results:
            (tl, tr, br, bl) = bbox
            tl = tuple(map(int, tl))
            br = tuple(map(int, br))
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            cv2.putText(image, text, tl, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        output_path = "ocr_output.jpg"
        cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        pixmap = QPixmap(output_path).scaled(
            self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)

        self.text_output.setPlainText(full_text)

    def open_id_window(self):
        self.id_window = IDCardWindow(self.reader)
        self.id_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
