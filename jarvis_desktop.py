
import sys
import os
import jarvis
import file_manager

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QLineEdit,
    QFileDialog,
    QInputDialog
)

from PySide6.QtCore import Qt, QThread, Signal


# ==========================================
# AI WORKER
# ==========================================

class RudraWorker(QThread):

    response_ready = Signal(str)
    status_changed = Signal(str)

    def __init__(self, message="", voice=False):
        super().__init__()
        self.message = message
        self.voice = voice

    def run(self):
        try:
            if self.voice:
                self.status_changed.emit("Listening...")

                question = jarvis.listen_to_jarvis()

                if not question:
                    self.status_changed.emit("Ready")
                    return

                self.response_ready.emit("YOU: " + question)

            else:
                question = self.message

            self.status_changed.emit("Thinking...")

            answer = jarvis.ask_jarvis(
                question,
                speak_output=self.voice
            )

            self.response_ready.emit("RUDRA: " + str(answer))
            self.status_changed.emit("Ready")

        except Exception as error:
            self.response_ready.emit("ERROR: " + str(error))
            self.status_changed.emit("Error")


# ==========================================
# FILE SEARCH WORKER
# ==========================================

class FileSearchWorker(QThread):

    search_complete = Signal(str)
    search_failed = Signal(str)

    def __init__(self, directory, keyword):
        super().__init__()

        self.directory = directory
        self.keyword = keyword

    def run(self):
        try:
            results = file_manager.search_files(
                self.directory,
                self.keyword
            )

            if not results:
                self.search_complete.emit(
                    "No matching files found."
                )
                return

            output = (
                f"Found {len(results)} matching file(s):\n\n"
            )

            for path in results[:100]:
                output += path + "\n"

            if len(results) > 100:
                output += (
                    f"\nShowing first 100 of {len(results)} results."
                )

            self.search_complete.emit(output)

        except Exception as error:
            self.search_failed.emit(str(error))


# ==========================================
# RUDRA DESKTOP APPLICATION
# ==========================================

class RudraWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RUDRA - Personal AI Assistant")
        self.resize(1000, 700)

        self.worker = None
        self.search_worker = None

        layout = QVBoxLayout(self)

        # Heading

        self.heading = QLabel("R U D R A")

        self.heading.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.heading.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #00c8ff;
            padding: 15px;
        """)

        # Status

        self.status = QLabel("SYSTEM ONLINE")

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Chat

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.chat.setPlaceholderText(
            "Your conversation with Rudra..."
        )

        # Text input

        self.input_box = QLineEdit()

        self.input_box.setPlaceholderText(
            "Ask Rudra anything..."
        )

        self.input_box.returnPressed.connect(
            self.send_message
        )

        # Buttons

        self.send_button = QPushButton("SEND")

        self.send_button.clicked.connect(
            self.send_message
        )

        self.talk_button = QPushButton("MICROPHONE")

        self.talk_button.clicked.connect(
            self.start_voice
        )

        self.search_button = QPushButton("SEARCH FILES")

        self.search_button.clicked.connect(
            self.start_file_search
        )

        # Input layout

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.talk_button)

        # Search layout

        search_layout = QHBoxLayout()

        search_layout.addWidget(self.search_button)

        # Main layout

        layout.addWidget(self.heading)
        layout.addWidget(self.status)
        layout.addWidget(self.chat)
        layout.addLayout(input_layout)
        layout.addLayout(search_layout)

        # Styling

        self.setStyleSheet("""
            QWidget {
                background-color: #101820;
                color: white;
            }

            QTextEdit, QLineEdit {
                background-color: #1c2833;
                color: white;
                border: 1px solid #0088aa;
                border-radius: 7px;
                padding: 12px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #007caa;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #009dcc;
            }

            QPushButton:disabled {
                background-color: #444444;
            }
        """)

        self.chat.append(
            "RUDRA: Desktop system initialized."
        )

        self.chat.append(
            "RUDRA: AI engine connected."
        )

        self.chat.append(
            "RUDRA: File search module connected."
        )

        self.chat.append(
            "RUDRA: Ready to assist you."
        )

    # ======================================
    # AI CHAT
    # ======================================

    def start_worker(self, message="", voice=False):

        if self.worker is not None and self.worker.isRunning():
            return

        self.send_button.setEnabled(False)
        self.talk_button.setEnabled(False)

        self.worker = RudraWorker(message, voice)

        self.worker.response_ready.connect(
            self.show_response
        )

        self.worker.status_changed.connect(
            self.update_status
        )

        self.worker.finished.connect(
            self.worker_finished
        )

        self.worker.start()

    def send_message(self):

        message = self.input_box.text().strip()

        if not message:
            return

        if self.worker is not None and self.worker.isRunning():
            return

        self.chat.append("\nYOU: " + message)

        self.input_box.clear()

        self.start_worker(message=message)

    def start_voice(self):

        self.start_worker(voice=True)

    def show_response(self, response):

        self.chat.append("\n" + response)

    def update_status(self, status):

        self.status.setText("RUDRA: " + status)

    def worker_finished(self):

        self.send_button.setEnabled(True)
        self.talk_button.setEnabled(True)

        self.status.setText("RUDRA: READY")

    # ======================================
    # FILE SEARCH
    # ======================================

    def start_file_search(self):

        if self.search_worker is not None:
            if self.search_worker.isRunning():
                return

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select folder or drive to search",
            "C:\\"
        )

        if not directory:
            return

        keyword, accepted = QInputDialog.getText(
            self,
            "RUDRA File Search",
            "Enter filename or keyword:"
        )

        if not accepted or not keyword.strip():
            return

        self.chat.append(
            "\nYOU: Search for '" + keyword.strip() + "'"
        )

        self.chat.append(
            "RUDRA: Searching in " + directory
        )

        self.status.setText("RUDRA: SEARCHING FILES...")

        self.search_button.setEnabled(False)

        self.search_worker = FileSearchWorker(
            directory,
            keyword.strip()
        )

        self.search_worker.search_complete.connect(
            self.file_search_complete
        )

        self.search_worker.search_failed.connect(
            self.file_search_failed
        )

        self.search_worker.finished.connect(
            self.file_search_finished
        )

        self.search_worker.start()

    def file_search_complete(self, result):

        self.chat.append(
            "\nRUDRA FILE SEARCH:\n" + result
        )

    def file_search_failed(self, error):

        self.chat.append(
            "\nRUDRA FILE SEARCH ERROR:\n" + error
        )

    def file_search_finished(self):

        self.search_button.setEnabled(True)

        self.status.setText("RUDRA: READY")

    # ======================================
    # CLOSE APPLICATION
    # ======================================

    def closeEvent(self, event):

        if self.worker is not None and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait()

        if (
            self.search_worker is not None
            and self.search_worker.isRunning()
        ):
            self.search_worker.wait()

        event.accept()


# ==========================================
# APPLICATION START
# ==========================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = RudraWindow()

    window.show()

    sys.exit(app.exec())
