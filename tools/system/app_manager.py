import subprocess
import logging
import shlex

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def is_app_running(process_name: str) -> bool:
    try:
        result = subprocess.run(
            ["pgrep", "-f", process_name], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Failed to check if {process_name} is running: {e}")
        return False

def open_app(command: str) -> bool:
    """
    Launches an application deterministically.
    Supports basic binaries ('gnome-calculator') and Flatpaks ('flatpak run com.spotify.Client').
    """
    # Just check the first word (e.g., 'spotify' or 'flatpak') to avoid massive logs
    base_name = command.split()[-1] 
    
    if is_app_running(base_name):
        logging.info(f"{base_name} is already running.")
        return True
        
    try:
        logging.info(f"Launching: {command}...")
        # shlex.split safely breaks "flatpak run com.spotify.Client" into the list subprocess needs
        cmd_list = shlex.split(command)
        
        subprocess.Popen(
            cmd_list,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        return True
    except FileNotFoundError:
        logging.error(f"Could not find command: '{command}'. Is it installed?")
        return False
    except Exception as e:
        logging.error(f"Failed to launch {command}: {e}")
        return False

def close_app(process_name: str) -> bool:
    if not is_app_running(process_name):
        logging.info(f"{process_name} is not running.")
        return True

    try:
        logging.info(f"Force closing {process_name}...")
        subprocess.run(["pkill", "-f", process_name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to close {process_name}: {e}")
        return False

if __name__ == "__main__":
    import time
    
    # Let's test it with the exact Flatpak command!
    test_launch_cmd = "flatpak run com.spotify.Client"
    test_kill_name = "spotify"  # We still just search for 'spotify' to kill it
    
    print("\nAttempting to open Spotify via Flatpak...")
    open_app(test_launch_cmd)
    
    time.sleep(5)  # Give Spotify time to boot
    
    # print(f"\nAttempting to close {test_kill_name}...")
    # close_app(test_kill_name)