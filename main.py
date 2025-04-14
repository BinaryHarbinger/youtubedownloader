import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QStyleFactory
)
import dlpscript  # Senin indirme modülün

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 800, 600)

        # Sistem temasını uygula
        system_style = QApplication.style().objectName()
        self.setStyle(QStyleFactory.create(system_style))

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(10)

        # URL giriş kısmı
        url_layout = QHBoxLayout()
        url_layout.addStretch(1)
        self.url_label = QLabel("YouTube URL:")
        self.url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        url_layout.addWidget(self.url_label)

        self.url_entry = QLineEdit()
        self.url_entry.setFixedWidth(300)
        self.url_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.url_entry.textChanged.connect(self.on_url_entered)
        url_layout.addWidget(self.url_entry)

        url_layout.addStretch(1)
        self.main_layout.addLayout(url_layout)

        # Format seçme kısmı
        format_layout = QHBoxLayout()
        format_layout.setSpacing(2)
        format_layout.addStretch(1)
        self.format_label = QLabel("Select file format:")
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        format_layout.addWidget(self.format_label)

        self.format_combo = QComboBox()
        self.format_combo.setFixedWidth(150)
        self.format_combo.addItems(["Video", "Sound"])
        format_layout.addWidget(self.format_combo)

        format_layout.addStretch(1)
        self.main_layout.addLayout(format_layout)

        # İndirme butonu ve checkbox'ı aynı hizaya koy
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.download_button = QPushButton("Download")
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.on_download_click)
        button_layout.addWidget(self.download_button)

        # CheckBox ekle
        self.option_checkbox = QCheckBox("Redownload")
        self.option_checkbox.setChecked(False)  # Varsayılan olarak seçili değil
        button_layout.addWidget(self.option_checkbox)

        button_layout.addStretch(1)
        self.main_layout.addLayout(button_layout)

        # Durum etiketi
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def on_url_entered(self, text):
        # URL boş değilse butonu etkinleştir
        self.download_button.setEnabled(bool(text.strip()))

    def on_download_click(self):
        url = self.url_entry.text().strip()
        file_format = self.format_combo.currentText()
        redownload = self.option_checkbox.isChecked()  # CheckBox değeri True/False olarak alınır

        if url:
            self.status_label.setText("Downloading...")
            self.download_button.setEnabled(False)
            QApplication.processEvents()  # GUI donmasın

            try:
                # İndirici fonksiyon, checkbox bilgisini de alacak şekilde güncellenebilir.
                dlpscript.download_file(url, file_format=file_format, redownload_file=redownload)
                self.status_label.setText("Download completed!")
            except Exception as e:
                print(f"An error occurred: {e}")
                self.status_label.setText("An error occurred.")
                self.download_button.setEnabled(True)
                return

            self.download_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
