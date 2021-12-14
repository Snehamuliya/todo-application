import time
from plyer import notification

if __name__=="__main__":
    while True:
        notification.notify(
            title = "take a break",
            message = "its good to take short break",
            timeout=10
        )
        time.sleep(3)