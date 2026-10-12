"""Jarvis desktop app - SpeechRecognition for proper Windows mic access."""
import tkinter as tk
from tkinter import scrolledtext
import math
import threading
import time

API_URL = "http://localhost:8787"

try:
    import speech_recognition as sr
    HAS_SPEECH = True
except ImportError:
    HAS_SPEECH = False


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
        self.recognizer = None

        # Mic permission panel
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
        title = tk.Label(root, text="Jarvis", font=("Arial", 32, "bold"), bg="#0a0e27", fg="#4dd0e1")
        title.pack(pady=15)

        # Status
        self.status = tk.Label(root, text="WAITING FOR PERMISSION", font=("Arial", 12), bg="#0a0e27", fg="#90caf9")
        self.status.pack(pady=10)

        # Canvas
        self.canvas = JarvisCanvas(root, width=400, height=400)
        self.canvas.pack(pady=10, expand=True)

        # Approval frame
        self.approval_frame = tk.Frame(root, bg="#0a0e27", highlightthickness=1, highlightbackground="#2d55ff")
        self.approval_frame.pack(pady=10, fill=tk.X, padx=20)
        self.approval_frame.pack_forget()

        self.approval_title = tk.Label(self.approval_frame, text="Approval Required", font=("Arial", 12, "bold"), bg="#0a0e27", fg="#4dd0e1")
        self.approval_title.pack(pady=5)

        self.approval_details = tk.Label(self.approval_frame, text="Details pending...", font=("Arial", 10), bg="#0a0e27", fg="#b0bec5", wraplength=500, justify=tk.LEFT)
        self.approval_details.pack(pady=5)

        btn_frame = tk.Frame(self.approval_frame, bg="#0a0e27")
        btn_frame.pack(pady=10)

        self.btn_approve = tk.Button(btn_frame, text="✓ Approve", bg="#4caf50", fg="white", font=("Arial", 10), padx=20, command=self.approve)
        self.btn_approve.pack(side=tk.LEFT, padx=5)

        self.btn_deny = tk.Button(btn_frame, text="✗ Deny", bg="#f44336", fg="white", font=("Arial", 10), padx=20, command=self.deny)
        self.btn_deny.pack(side=tk.LEFT, padx=5)

        # Logs
        self.logs = scrolledtext.ScrolledText(root, height=8, bg="#0a0e27", fg="#4dd0e1", font=("Courier", 9), state=tk.DISABLED, insertbackground="#4dd0e1")
        self.logs.pack(pady=10, padx=20, fill=tk.BOTH, expand=False)

        self.log("Jarvis started. Click 'Enable Microphone'")
        self.log("Using SpeechRecognition (Google STT).")
        self.poll_state()

    def enable_microphone(self):
        if not HAS_SPEECH:
            self.log("Install: pip install SpeechRecognition")
            return

        self.log("🎤 Initializing microphone...")

        try:
            self.recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.log("✓ Microphone ready!")

            self.mic_enabled = True
            self.mic_status.config(text="🟢 Microphone: ENABLED", fg="#4caf50")
            self.btn_mic.config(text="✓ Listening...", state=tk.DISABLED)
            self.status.config(text="LISTENING...")
            self.canvas.set_state("listening")

            if self.voice_thread is None or not self.voice_thread.is_alive():
                self.voice_thread = threading.Thread(target=self.voice_listener, daemon=True)
                self.voice_thread.start()
                self.log("🎤 Say something...")

        except Exception as e:
            self.log(f"❌ Error: {e}")
            self.mic_status.config(text="❌ FAILED", fg="#f44336")

    def voice_listener(self):
        if not self.recognizer or not self.mic_enabled:
            return

        try:
            with sr.Microphone() as source:
                while self.mic_enabled:
                    try:
                        self.canvas.set_state("listening")
                        self.log("🎧 Listening (10 sec timeout)...")

                        audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                        self.canvas.set_state("thinking")
                        self.status.config(text="PROCESSING...")
                        self.log("🔄 Converting to text...")

                        text = self.recognizer.recognize_google(audio)
                        self.log(f"✓ HEARD: {text}")
                        self.canvas.set_state("speaking")
                        self.status.config(text="UNDERSTOOD")
                        time.sleep(1)

                    except sr.UnknownValueError:
                        self.log("? Could not understand")
                    except sr.RequestError as e:
                        self.log(f"Google API error: {e}")
                    except sr.WaitTimeoutError:
                        self.log("Timeout - no sound detected")

        except Exception as e:
            if self.mic_enabled:
                self.log(f"Listener error: {e}")

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
            self.log(f"✓ Approved")
            self.approval_frame.pack_forget()
            self.current_task = None
            self.canvas.set_state("listening")

    def deny(self):
        if self.current_task:
            self.log(f"✗ Denied")
            self.approval_frame.pack_forget()
            self.current_task = None
            self.canvas.set_state("listening")


def main():
    root = tk.Tk()
    app = JarvisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
