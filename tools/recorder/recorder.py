from pathlib import Path
from datetime import datetime
from threading import RLock
import platform, json
import os, errno
import sys, linecache


MB = 1024 * 1024
MAX_SIZE = 10 * MB

# ----------

AUTHOR = "Alessio"
ICON = "@"
VERSION = "1.0.7"

def _get_signature() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys_info = platform.node()

    signature = {
        "author": AUTHOR,
        "date": now,
        "version": VERSION,
        "host": sys_info,
    }

    return json.dumps(signature)

# ----------


class Recorder:
    def __init__(self, filepath, max_size=MAX_SIZE, _print=False):
        self.recording = True
        self.filepath = filepath
        self.file = None
        self.file_dim = max_size
        self.current_size = 0
        self._print = _print
        self.lock = RLock()

    def __enter__(self):
        with self.lock:
            if self.file is None:
                self.start()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.join()
        return False
    # -----------


    def start(self):
        with self.lock:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            is_new = not self.filepath.exists() or self.filepath.stat().st_size == 0

            try:
                self.file = open(self.filepath, "a", encoding="utf-8")
                if is_new:
                    signature = _get_signature() + "\n"
                    self.file.write(signature)
                    self.file.flush()
                    self.current_size = len(signature.encode())
                else:
                    self.current_size = self.filepath.stat().st_size
            except Exception as e:
                print(e)
                self.file = None

    def rotate(self):
        with self.lock:
            if self.file:
                self.file.close()
                self.file = None

            if not self.filepath.exists():
                return

            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            rotated_path = self.filepath.with_name(f"{self.filepath.stem}_{now}{self.filepath.suffix}")
            self.filepath.rename(rotated_path)

            self.current_size = 0
            self.start()

    def join(self):
        with self.lock:
            if self.file:
                self.file.flush()
                self.file.close()
                self.file = None


    # ----------
    def write(self, msg):
        # ----------
        def build_record(msg: str) -> dict:
            frame = sys._getframe(2)
            context = linecache.getline(frame.f_code.co_filename, frame.f_lineno)
            context = context.strip()

            data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f"),
                "module": frame.f_code.co_filename,
                "function": frame.f_code.co_name,
                "from_line": frame.f_lineno,
                "context":  context if context else "N/A",
                "payload": msg
            }

            return json.dumps(data)
        # ----------

        with self.lock:
            if not self.recording:
                return

            if self.file is None:
                self.start()

            record = build_record(msg) + "\n"
            record_bytes = record.encode()

            if self._print:
                print(record)

            try:
                if self.current_size + len(record_bytes)>= self.file_dim:
                    self.rotate()

                self.file.write(record)
                self.current_size += len(record_bytes)
                self.file.flush()
                os.fsync(self.file.fileno())
            except OSError as e:
                if e.errno == errno.ENOSPC:
                    print("MEMORY DISK FULL")
                    self.recording = False
                    try:
                        self.file.close()
                    except OSError:
                        pass
                else:
                    raise
    # ----------


"""
Record is the bridge between execution and intelligence—a structured chronicler
designed for both human oversight and AI-driven analysis.

Beyond simple logging, it captures the DNA of every event, embedding
traceability and context into a format that speaks fluently to LLMs and
Machine Learning models. By minimizing noise and maximizing structure, it
allows even the most resource-constrained AI to parse, understand, and
reconstruct your data with ease. It is a resilient, thread-safe guardian
that honors the flow of your script while ensuring that every memory
remains accessible, lightweight, and ready for the future of automation.
"""
