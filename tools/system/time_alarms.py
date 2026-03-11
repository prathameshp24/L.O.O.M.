import datetime
import subprocess
import logging
import threading


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def getCurrentTime()->str:
    """Returns current date and time in a human readable format"""
    now = datetime.datetime.now()

    timeStr = now.strftime("%A, %B %d, %Y at %I:%M %p")
    logging.info(f"Time checked: {timeStr}")
    return timeStr


def triggerAlarm(message: str):
    """Internal callback function that executes when a timer finishes"""
    logging.info(f"Alarm triggered: {message}")
    try:
        subprocess.run(["notify-send", "-u", "critical", "--icon=appointment-soon", "L.O.O.M. Reminder", message], check=True)

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to send desktop notification : {e}")
    
    except FileNotFoundError:
        logging.error("notify-send not found")
    



def setTimer(minutes: float, message: str) -> bool:
    """Sets a background timer that will trigger a desktop notification"""

    try:
        seconds = minutes * 60
        t = threading.Timer(seconds, triggerAlarm, args=[message])
        t.daemon = True
        t.start()

        logging.info(f"Timer set for {minutes} minutes. Remainder : {message}")
        return True
    
    except Exception as e:
        logging.error(f"Failed to set timer : {e}")
        return False
    

if __name__ == "__main__":
    import time
    print("Testing LOOM Time and alarm toolset")

    currentTime = getCurrentTime()
    print(f"Agent sees the time as : {currentTime}")

    print("setting a 3 seconds test timer")

    setTimer(0.05, "Test Timer")

    time.sleep(5)
    print("Test complete")