"""Jarvis desktop app (PyQt5)."""
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtCore import QTime
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8787"


class JarvisWorker(QObject):
    """Background worker for API calls."""
    state_changed = pyqtSignal(str)
    approval_requested = pyqtSignal(dict)
    log_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True

    def poll_state(self):
        """Poll brain state."""
        try:
            resp = requests.get(f"{API_URL}/health", timeout=2)
            if resp.status_code == 200:
                self.state_changed.emit("listening")
                self.log_message.emit("Connected to Jarvis")
        except Exception as e:
            self.log_message.emit(f"Connection error: {e}")


class CanvasWidget(QFrame):
    """Animated canvas for Jarvis state."""

    def __init__(self):
        super().__init__()
        self.state = "idle"
        self.time = 0
        self.setStyleSheet("background-color: #0a0e27;")
        self.setMinimumSize(400, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)

    def animate(self):
        """Animate based on state."""
        self.time += 1
        self.update()

    def set_state(self, state: str):
        """Update state (idle, listening, thinking, speaking)."""
        self.state = state

    def paintEvent(self, event):
        """Draw canvas animation."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(10, 14, 39))

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2

        color = QColor(77, 208, 225) if self.state == "speaking" else QColor(33, 150, 243)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(cx - 20), int(cy - 20), 40, 40)

        if self.state in ("listening", "idle"):
            import math
            breathe = 10 + 5 * math.sin(self.time * 0.1)
            painter.setPen(QPen(QColor(77, 208, 225, 100), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(int(cx - 20 - breathe), int(cy - 20 - breathe),
                               int(40 + 2 * breathe), int(40 + 2 * breathe))

        if self.state in ("thinking", "speaking"):
            painter.setBrush(QBrush(QColor(77, 208, 225)))
            painter.setPen(Qt.NoPen)
            import math
            for i in range(8):
                angle = (i / 8) * 2 * math.pi
                x = cx + 50 * math.cos(angle)
                y = cy + 50 * math.sin(angle)
                h_bar = 15 + 10 * math.sin(self.time * 0.15 + i)
                painter.drawRect(int(x - 4), int(y - h_bar / 2), 8, int(h_bar))


class JarvisWindow(QMainWindow):
    """Main Jarvis desktop window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis — Voice Assistant")
        self.setGeometry(100, 100, 900, 800)
        self.setStyleSheet("background-color: #0a0e27; color: #e0e0e0;")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        title = QLabel("Jarvis")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: #4dd0e1;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.status_label = QLabel("LISTENING...")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("color: #90caf9;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.canvas = CanvasWidget()
        layout.addWidget(self.canvas, 1)

        self.approval_frame = QFrame()
        self.approval_frame.setStyleSheet(
            "border: 1px solid #2d55ff; background-color: rgba(45, 85, 255, 0.1);"
        )
        self.approval_frame.setVisible(False)
        approval_layout = QVBoxLayout()

        self.approval_title = QLabel("Approval Required")
        self.approval_title.setFont(QFont("Arial", 12, QFont.Bold))
        self.approval_title.setStyleSheet("color: #4dd0e1;")
        approval_layout.addWidget(self.approval_title)

        self.approval_details = QLabel()
        self.approval_details.setStyleSheet("color: #b0bec5;")
        approval_layout.addWidget(self.approval_details)

        btn_layout = QHBoxLayout()
        self.btn_approve = QPushButton("✓ Approve")
        self.btn_approve.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 8px; border-radius: 4px;"
        )
        self.btn_approve.clicked.connect(self.approve)
        btn_layout.addWidget(self.btn_approve)

        self.btn_deny = QPushButton("✗ Deny")
        self.btn_deny.setStyleSheet(
            "background-color: #f44336; color: white; padding: 8px; border-radius: 4px;"
        )
        self.btn_deny.clicked.connect(self.deny)
        btn_layout.addWidget(self.btn_deny)

        approval_layout.addLayout(btn_layout)
        self.approval_frame.setLayout(approval_layout)
        layout.addWidget(self.approval_frame)

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.3); color: #4dd0e1; "
            "border: 1px solid #333; font-family: Courier; font-size: 10px;"
        )
        self.logs.setMaximumHeight(150)
        layout.addWidget(self.logs)

        central.setLayout(layout)

        self.worker = JarvisWorker()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker.state_changed.connect(self.on_state_change)
        self.worker.log_message.connect(self.log)
        self.worker_thread.start()

        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.worker.poll_state)
        self.poll_timer.start(2000)

        self.current_task = None
        self.log("Jarvis started")

    def on_state_change(self, state: str):
        """Handle state change."""
        self.canvas.set_state(state)
        self.status_label.setText(state.upper())

    def log(self, msg: str):
        """Add log message."""
        now = QTime.currentTime().toString("hh:mm:ss")
        self.logs.append(f"[{now}] {msg}")
        self.logs.verticalScrollBar().setValue(self.logs.verticalScrollBar().maximum())

    def show_approval(self, task_id: str, task: str, details: str):
        """Show approval panel."""
        self.current_task = {"task_id": task_id, "task": task}
        self.approval_title.setText(f"Approve: {task}")
        self.approval_details.setText(details)
        self.approval_frame.setVisible(True)
        self.canvas.set_state("approval_pending")
        self.log(f"Waiting approval: {task}")

    def approve(self):
        """Approve task."""
        if self.current_task:
            self.log(f"✓ Approved: {self.current_task['task']}")
            self.approval_frame.setVisible(False)
            self.current_task = None
            self.canvas.set_state("listening")

    def deny(self):
        """Deny task."""
        if self.current_task:
            self.log(f"✗ Denied: {self.current_task['task']}")
            self.approval_frame.setVisible(False)
            self.current_task = None
            self.canvas.set_state("listening")

    def closeEvent(self, event):
        """Clean up on close."""
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = JarvisWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
