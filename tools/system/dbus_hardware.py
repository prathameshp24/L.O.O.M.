import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')



def getBrightness() -> int:
    """Reads current brightness percentage"""
    try:
        currentRaw = subprocess.run(["brightnessctl", "get"], capture_output=True, text=True, check=True).stdout.strip()
        maxRaw = subprocess.run(["brightnessctl", "max"], capture_output=True, text=True, check=True).stdout.strip()

        percentage = int((int(currentRaw) / int(maxRaw)) * 100)
        return percentage

        

    except Exception as e:
        logging.error(f"Failed to get current brightness: {e}")
        return -1

def setBrightness(percentage: int) -> bool:
    """Sets screen brightness to an exact percentage using brightnessctl"""
    percentage = max(0, min(100, percentage))
    try:
        # brightnessctl set 80%
        subprocess.run(["brightnessctl", "set", f"{percentage}%"], check=True, capture_output=True)
        logging.info(f"Brightness physically set to {percentage}%")
        return True
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set brightness. Is brightnessctl installed? Error: {e}")
        return False
    except FileNotFoundError:
        logging.error("brightnessctl command not found. Please install it via dnf.")
        return False

def adjustBrightness(stepPercentage: int) -> bool:
    """Increases or decreases brightness by a percentage"""
    try:
        if stepPercentage > 0:
            action = f"+{stepPercentage}%"
        else:
            action = f"{abs(stepPercentage)}%-"
    

        subprocess.run(["brightnessctl", "set", action], check=True, capture_output=True)
        logging.info(f"Brightness adjusted by {action}")
        return True
    
    except Exception as e:
        logging.error(f"Failed to change brightness : {e}")
        return False


def toggleMute() -> bool:
    """Toggles system default audio sink mute state"""
    try:
        subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"], check=True)
        logging.info("Mute toggled")
        return True
    
    except Exception as e:
        logging.error(f"Could not toggle mute : {e}")
        return False


def setVolume(percentage: int) -> bool:
    """Sets the system volume to the exact percentage"""
    percentage = max(0, min(percentage, 100))
    volDecimal = percentage / 100.0
    try:
        subprocess.run(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", str(volDecimal)], check=True)
        logging.info(f"Set percentage : {percentage}")
        return True
    
    except Exception as e:
        logging.error(f"Could not set volume : {e}")
        return False




if __name__ == "__main__":
    print("Testing LOOM Hardware Toolset")
    # Let's try setting it to 50% to see a noticeable dip, then back up.
    current = getBrightness()
    print(f"Current System Brightness is : {current}%")

    print("Dimming screen by 10%")
    adjustBrightness(-10)

    newCurrent = getBrightness()
    print(f"New System brightness is : {newCurrent}%")

    print(f"Setting the volume to 80%")
    setVolume(80)
