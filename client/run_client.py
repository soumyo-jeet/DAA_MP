import os
import subprocess
import sys

if __name__ == "__main__":
    if hasattr(sys, "frozen"):
        print("This helper is not supported in a frozen application.")
        sys.exit(1)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_dir, "app.py")

    print("Starting Streamlit app...")
    command = [sys.executable, "-m", "streamlit", "run", app_path]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print("Failed to launch Streamlit.")
        print(exc)
        sys.exit(exc.returncode)
