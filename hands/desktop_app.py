"""Jarvis desktop app (Tkinter - microphone support)."""
import tkinter as tk
from tkinter import scrolledtext, messagebox
import math
import threading
import time
from datetime import datetime

API_URL = "http://localhost:8787"

try:
    import sounddevice as sd
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False


class JarvisCanvas(tk.Canvas):
    """Animated canvas showing Jarvis state."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#0a0e27", highlightthickness=0, **kwargs)
        self.state = "idle"
        self.time = 0
        self.animate()

    def set_state(self, state):
        self.state = state

    def animate(self):
        self.delete("all")
        self.time += 1

        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            self.after(50, self.animate)
            return

        cx = w / 2
        cy = h / 2

        # Core circle
        color = "#4dd0e1" if self.state == "speaking" else "#2196f3"
        self.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill=color, outline=color)

        # Breathing ring
        if self.state in ("listening", "idle"):
            breathe = 10 + 5 * math.sin(self.time * 0.1)
            self.create_oval(
                cx - 20 - breathe, cy - 20 - breathe,
                cx + 20 + breathe, cy + 20 + breathe,
                outline="#4dd0e1", width=2
            )

        # Spectrum bars
        if self.state in ("thinking", "speaking"):
            for i in range(8):
                angle = (i / 8) * 2 * math.pi
                x = cx + 50 * math.cos(angle)
                y = cy + 50 * math.sin(angle)
                h_bar = 15 + 10 * math.sin(self.time * 0.15 + i)
                self.create_rectangle(
                    x - 4, y - h_bar / 2, x + 4, y + h_bar / 2,
                    fill="#4dd0e1", outline="#4dd0e1"
                )

        self.after(50, self.animate)


class JarvisApp:
    """Main Jarvis desktop application."""

    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis — Voice Assistant")
        self.root.geometry("900x800")
        self.root.configure(bg="#0a0e27")
        self.current_task = None
        self.listening = False

        # Start voice listener
        if HAS_AUDIO:
            self.voice_thread = threading.Thread(target=self.voice_listener, daemon=True)
            self.voice_thread.start()
            self.log("🎤 Microphone listening...")

        # Title
        title_frame = tk.Frame(root, bg="#0a0e27")
        title_frame.pack(pady=20)

        title = tk.Label(
            title_frame, text="Jarvis", font=("Arial", 32, "bold"),
            bg="#0a0e27", fg="#4dd0e1"
        )
        title.pack()

        # Status
        self.status = tk.Label(
            root, text="LISTENING...", font=("Arial", 12),
            bg="#0a0e27", fg="#90caf9"
        )
        self.status.pack(pady=10)

        # Canvas
        self.canvas = JarvisCanvas(root, width=400, height=400)
        self.canvas.pack(pady=10, expand=True)

        # Approval frame
        self.approval_frame = tk.Frame(root, bg="#0a0e27", highlightthickness=1, highlightbackground="#2d55ff")
        self.approval_frame.pack(pady=10, fill=tk.X, padx=20)
        self.approval_frame.pack_forget()

        self.approval_title = tk.Label(
            self.approval_frame, text="Approval Required", font=("Arial", 12, "bold"),
            bg="#0a0e27", fg="#4dd0e1"
        )
        self.approval_title.pack(pady=5)

        self.approval_details = tk.Label(
            self.approval_frame, text="Details pending...", font=("Arial", 10),
            bg="#0a0e27", fg="#b0bec5", wraplength=500, justify=tk.LEFT
        )
        self.approval_details.pack(pady=5)

        btn_frame = tk.Frame(self.approval_frame, bg="#0a0e27")
        btn_frame.pack(pady=10)

        self.btn_approve = tk.Button(
            btn_frame, text="✓ Approve", bg="#4caf50", fg="white",
            font=("Arial", 10), padx=20, command=self.approve
        )
        self.btn_approve.pack(side=tk.LEFT, padx=5)

        self.btn_deny = tk.Button(
            btn_frame, text="✗ Deny", bg="#f44336", fg="white",
            font=("Arial", 10), padx=20, command=self.deny
        )
        self.btn_deny.pack(side=tk.LEFT, padx=5)

        # Logs
        self.logs = scrolledtext.ScrolledText(
            root, height=8, bg="#0a0e27", fg="#4dd0e1",
            font=("Courier", 9), state=tk.DISABLED, insertbackground="#4dd0e1"
        )
        self.logs.pack(pady=10, padx=20, fill=tk.BOTH, expand=False)

        self.log("Jarvis started")
        self.poll_state()

    def log(self, msg):
        """Add message to logs."""
        now = datetime.now().strftime("%H:%M:%S")
        self.logs.config(state=tk.NORMAL)
        self.logs.insert(tk.END, f"[{now}] {msg}\n")
        self.logs.see(tk.END)
        self.logs.config(state=tk.DISABLED)

    def poll_state(self):
        """Poll Jarvis state."""
        try:
            import urllib.request
            urllib.request.urlopen(f"{API_URL}/health", timeout=2)
            self.canvas.set_state("listening")
            self.status.config(text="LISTENING...")
        except Exception as e:
            self.log(f"Connection: {e}")

        self.root.after(2000, self.poll_state)

    def show_approval(self, task_id, task, details):
        """Show approval panel."""
        self.current_task = {"task_id": task_id, "task": task}
        self.approval_title.config(text=f"Approve: {task}")
        self.approval_details.config(text=details)
        self.approval_frame.pack(pady=10, fill=tk.X, padx=20)
        self.canvas.set_state("approval_pending")
        self.log(f"⏳ Waiting approval: {task}")

    def approve(self):
        """Approve task."""
        if self.current_task:
            self.log(f"✓ Approved: {self.current_task['task']}")
            self.approval_frame.pack_forget()
            self.current_task = None
            self.canvas.set_state("listening")

    def deny(self):
        """Deny task."""
        if self.current_task:
            self.log(f"✗ Denied: {self.current_task['task']}")
            self.approval_frame.pack_forget()
            self.current_task = None
            self.canvas.set_state("listening")

    def voice_listener(self):
        """Listen for wake word."""
        if not HAS_AUDIO:
            self.log("⚠️ sounddevice not installed. Run: pip install sounddevice")
            return

        try:
            duration = 1
            samplerate = 16000

            while True:
                self.log("🎤 Listening for 'Hey Jarvis'...")
                self.canvas.set_state("listening")

                try:
                    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
                    sd.wait()

                    # Simple wake word detection (check for sound amplitude)
                    amplitude = np.abs(audio).mean()
                    if amplitude > 0.05:
                        self.log("🎙️ Sound detected!")
                        self.canvas.set_state("thinking")
                        self.status.config(text="PROCESSING...")
                        time.sleep(0.5)
                        self.log("✓ Ready for command")
                        self.canvas.set_state("listening")

                except Exception as e:
                    self.log(f"Microphone error: {e}")
                    time.sleep(2)

        except Exception as e:
            self.log(f"Voice listener error: {e}")


def main():
    root = tk.Tk()
    app = JarvisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
