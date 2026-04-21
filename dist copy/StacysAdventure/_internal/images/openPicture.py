import subprocess
import sys, os

_current_image_process = None

def openIMG(imagePath=None, destroy=False):
    global _current_image_process

    # Reap any exited process to prevent zombies
    if _current_image_process and _current_image_process.poll() is not None:
        _current_image_process.wait()
        _current_image_process = None

    # If destroy=True → close the running subprocess
    if destroy:
        if _current_image_process:
            _current_image_process.terminate()
            try:
                _current_image_process.wait(timeout=5)  # Wait up to 5 seconds
            except subprocess.TimeoutExpired:
                _current_image_process.kill()  # Force kill if needed
                _current_image_process.wait()
            _current_image_process = None
        return

    # Destroy previous image if one is open
    if _current_image_process:
        _current_image_process.terminate()
        try:
            _current_image_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _current_image_process.kill()
            _current_image_process.wait()
        _current_image_process = None

    script_path = os.path.join(os.path.dirname(__file__), "openPicture_subprocess.py")
    abs_image_path = os.path.abspath(imagePath)

    # Start Tk process and keep the handle
    _current_image_process = subprocess.Popen([
        sys.executable,
        script_path,
        abs_image_path
    ])


        
    
    


