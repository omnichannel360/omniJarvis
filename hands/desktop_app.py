"""Jarvis desktop app - with mic permission control."""
import tkinter as tk
from tkinter import scrolledtext
import math
import threading
import time

API_URL = "http://localhost:8787"

try:
    import sounddevice as sd
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False


class JarvisCanvas(tk.Canvas):
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
        color = "#4dd0e1" if self.state == "speaking" else "#2196f3"
        self.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill=color, outline=color)

        if self.state in ("listening", "idle"):
            breathe = 10 + 5 * math.sin(self.time * 0.1)
            self.create_oval(
                cx - 20 - breathe, cy - 20 - breathe,
                cx + 20 + breathe, cy + 20 + breathe,
                outline="#4dd0e1", width=2
            )

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
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis — Voice Assistant")
        self.root.geometry("900x850")
        self.root.configure(bg="#0a0e27")
        self.current_task = None
        self.mic_enabled = False
        self.voice_thread = None

        # Mic permission panel (top)
        mic_panel = tk.Frame(root, bg="#0a0e27", highlightthickness=1, highlightbackground="#f44336")
        mic_panel.pack(pady=10, padx=20, fill=tk.X)

        self.mic_status = tk.Label(
            mic_panel, text="🔴 Microphone: PERMISSION REQUIRED",
            font=("Arial", 11, "bold"), bg="#0a0e27", fg="#f44336"
        )
        self.mic_status.pack(side=tk.LEFT, padx=10, pady=8)

        self.btn_mic = tk.Button(
            mic_panel, text="✓ Enable Microphone",
            bg="#4caf50", fg="white", font=("Arial", 10, "bold"),
            padx=15, pady=5, command=self.enable_microphone
        )
        self.btn_mic.pack(side=tk.LEFT, padx=10)

        # Title
        title = tk.Label(
            root, text="Jarvis", font=("Arial", 32, "bold"),
            bg="#0a0e27", fg="#4dd0e1"
        )
        title.pack(pady=15)

        # Status
        self.status = tk.Label(
            root, text="WAITING FOR PERMISSION",
            font=("Arial", 12), bg="#0a0e27", fg="#90caf9"
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

        self.log("Jarvis started. Click 'Enable Microphone' to start.")
        self.log("Windows will ask for microphone permission.")
        self.detect_microphones()
        self.poll_state()

    def detect_microphones(self):
        """Detect available microphones."""
        if not HAS_AUDIO:
            self.log("⚠️ sounddevice not installed")
            return

        try:
            devices = sd.query_devices()
            self.log("🔍 Available audio devices:")
            input_devices = []

            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append(device)
                    name = device['name']
                    channels = device['max_input_channels']
                    self.log(f"  [{i}] {name} ({channels} ch)")

            if input_devices:
                default = sd.default.device
                self.log(f"✓ Default mic: Device {default[0]}")
            else:
                self.log("❌ No microphones detected!")
        except Exception as e:
            self.log(f"Error detecting mics: {e}")

    def enable_microphone(self):
        """Enable microphone with permission check."""
        if not HAS_AUDIO:
            self.log("⚠️ sounddevice not installed. Run: pip install sounddevice")
            return

        self.log("🎤 Requesting microphone access...")

        try:
            # Test microphone access
            sd.rec(1, samplerate=16000, channels=1, dtype='float32')
            sd.wait()
            self.mic_enabled = True
            self.mic_status.config(text="🟢 Microphone: ENABLED", fg="#4caf50")
            self.btn_mic.config(text="✓ Microphone Enabled", state=tk.DISABLED)
            self.status.config(text="LISTENING...")
            self.canvas.set_state("listening")
            self.log("✓ Microphone enabled! Say 'Hey Jarvis'")

            # Start voice listener
            if self.voice_thread is None or not self.voice_thread.is_alive():
                self.voice_thread = threading.Thread(target=self.voice_listener, daemon=True)
                self.voice_thread.start()
        except Exception as e:
            self.log(f"❌ Microphone access denied: {e}")
            self.log("To enable: Settings → Privacy → Microphone → Allow apps to access")
            self.mic_status.config(text="❌ Microphone: ACCESS DENIED", fg="#f44336")

    def voice_listener(self):
        """Listen for audio."""
        if not HAS_AUDIO or not self.mic_enabled:
            return

        try:
            while self.mic_enabled:
                duration = 1
                samplerate = 16000
                audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
                sd.wait()

                amplitude = np.abs(audio).mean()
                if amplitude > 0.05:
                    self.log(f"🎙️ Sound detected! (level: {amplitude:.2f})")
                    self.canvas.set_state("thinking")
                    self.status.config(text="PROCESSING...")
                    time.sleep(0.5)
                    self.canvas.set_state("listening")
                    self.status.config(text="LISTENING...")
        except Exception as e:
            if self.mic_enabled:
                self.log(f"Mic error: {e}")
                time.sleep(2)

    def log(self, msg):
        self.logs.config(state=tk.NORMAL)
        self.logs.insert(tk.END, f"{msg}\n")
        self.logs.see(tk.END)
        self.logs.config(state=tk.DISABLED)

    def poll_state(self):
        try:
            import urllib.request
            urllib.request.urlopen(f"{API_URL}/health", timeout=2)
        except:
            pass
        self.root.after(2000, self.poll_state)

    def approve(self):
        if self.current_task:
            self.log(f"✓ Approved: {self.current_task['task']}")
            self.approval_frame.pack_forget()
            self.current_task = None
            self.canvas.set_state("listening")

    def deny(self):
        if self.current_task:
            self.log(f"✗ Denied: {self.current_task['task']}")
            self.approval_frame.pack_forget()
            self.current_task = None
            self.canvas.set_state("listening")


def main():
    root = tk.Tk()
    app = JarvisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
