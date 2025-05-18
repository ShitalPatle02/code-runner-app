import subprocess
import tempfile
import os

def run_code(code: str, input_data: str) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        filename = f.name

    try:
        result = subprocess.run(
            ["python", "-u", filename],  # unbuffered output
            input=input_data + "\n",
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Error: Execution timed out."
    except Exception as e:
        output = f"Error: {str(e)}"
    finally:
        try:
            os.remove(filename)
        except:
            pass

    return output
