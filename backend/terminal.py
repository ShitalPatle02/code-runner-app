# terminal_handler.py (Windows-compatible)
import subprocess
import threading
import uuid
import os

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

class PythonSession:
    def __init__(self):
        self.code_buffer = []  # Stores all code lines sent
        self.lock = threading.Lock()

    def send_input(self, user_input: str) -> str:
        with self.lock:
            self.code_buffer.append(user_input)
            return self.run_code()

    def run_code(self) -> str:
        code = "\n".join(self.code_buffer)
        filename = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.py")
        try:
            with open(filename, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def start_session(self):
        return "Python session started. Type your code below."

    def close(self):
        with self.lock:
            self.code_buffer.clear()

# One-shot code execution using subprocess (legacy style)
def run_code_batch(code: str, input_data: str = "") -> str:
    filename = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.py")
    with open(filename, "w") as f:
        f.write(code)
    try:
        result = subprocess.run(
            ["python", filename],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)
    finally:
        if os.path.exists(filename):
            os.remove(filename)