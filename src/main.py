import sys
import os
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QStyleFactory,
    QFileDialog, QProgressBar
)
import dlpscript

class DownloadThread(QThread):
    finished = pyqtSignal(bool, str)  # (success, message)
    progress = pyqtSignal(str)  # Progress message

    def __init__(self, video_url, custom_output_dir, file_format, redownload_file):
        super().__init__()
        self.video_url = video_url
        self.custom_output_dir = custom_output_dir
        self.file_format = file_format
        self.redownload_file = redownload_file

    def run(self):
        try:
            self.progress.emit("Starting download...")
            dlpscript.download_file(
                video_url=self.video_url,
                custom_output_dir=self.custom_output_dir,
                file_format=self.file_format,
                redownload_file=self.redownload_file
            )
            self.finished.emit(True, "Download completed!")
        except Exception as e:
            error_message = str(e)
            print(f"Error occurred: {error_message}")
            self.finished.emit(False, f"Error: {error_message}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 800, 600)
        self.custom_path = None
        self.download_thread = None

        # Apply system theme
        system_style = QApplication.style().objectName()
        self.setStyle(QStyleFactory.create(system_style))

        # Main widget and layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(10)

        # URL input section
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

        # Format selection section
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

        # Directory selection section
        path_layout = QHBoxLayout()
        path_layout.addStretch(1)

        self.path_label = QLabel("Save to:")
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_layout.addWidget(self.path_label)

        self.path_entry = QLineEdit()
        self.path_entry.setFixedWidth(250)
        self.path_entry.setReadOnly(True)
        self.path_entry.setPlaceholderText("Default directory")
        path_layout.addWidget(self.path_entry)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        path_layout.addWidget(self.browse_button)

        self.reset_path_button = QPushButton("Reset")
        self.reset_path_button.clicked.connect(self.reset_path)
        path_layout.addWidget(self.reset_path_button)

        path_layout.addStretch(1)
        self.main_layout.addLayout(path_layout)

        # Download button and checkbox layout
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.download_button = QPushButton("Download")
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.on_download_click)
        button_layout.addWidget(self.download_button)

        self.option_checkbox = QCheckBox("Redownload")
        self.option_checkbox.setChecked(False)
        button_layout.addWidget(self.option_checkbox)

        button_layout.addStretch(1)
        self.main_layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.hide()
        self.main_layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Download Directory",
            os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly
        )
        if directory:
            self.custom_path = directory
            display_path = directory
            if len(display_path) > 40:
                display_path = "..." + display_path[-37:]
            self.path_entry.setText(display_path)

    def reset_path(self):
        self.custom_path = None
        self.path_entry.clear()
        self.path_entry.setPlaceholderText("Default directory")

    def on_url_entered(self, text):
        self.download_button.setEnabled(bool(text.strip()))

    def update_progress(self, message):
        self.status_label.setText(message)
        self.progress_bar.setFormat(message)

    def download_finished(self, success, message):
        self.progress_bar.hide()
        self.status_label.setText(message)
        self.download_button.setEnabled(True)
        self.url_entry.setEnabled(True)
        self.format_combo.setEnabled(True)
        self.option_checkbox.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.reset_path_button.setEnabled(True)

        if success:
            self.url_entry.clear()

    def on_download_click(self):
        url = self.url_entry.text().strip()
        if not url:
            return

        # Disable UI elements during download
        self.download_button.setEnabled(False)
        self.url_entry.setEnabled(False)
        self.format_combo.setEnabled(False)
        self.option_checkbox.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.reset_path_button.setEnabled(False)

        # Show progress bar
        self.progress_bar.setMaximum(0)
        self.progress_bar.show()
        self.status_label.setText("Preparing download...")

        # Start download thread
        self.download_thread = DownloadThread(
            video_url=url,
            custom_output_dir=self.custom_path,
            file_format=self.format_combo.currentText(),
            redownload_file=self.option_checkbox.isChecked()
        )
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
