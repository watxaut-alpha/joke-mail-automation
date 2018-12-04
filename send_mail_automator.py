import traceback
from core.firebase import JokeFirebaseDB
import time
from datetime import datetime

if __name__ == '__main__':
    # Executing this code will bring joy to anyone in the mail list of receivers by providing a joke only if this is
    # executed between 8:20 - 8:40 am (in your time zone). This is useful while used with Automator or any other tool
    # to automate scripts
    try:

        x = datetime.today()
        y = datetime(x.year, x.month, x.day, 8, 30, 0)

        # get the difference and if the difference is less than 10 minutes, send mail
        delta_t = x-y
        min_to_830 = abs(delta_t.total_seconds()/60.0)

        # day_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][x.weekday()]
        day_week = x.weekday()
        # try to send the xist today
        if min_to_830 <= 10:

            # sleep time until 8:30 exact
            time.sleep(delta_t.total_seconds())

            c = JokeFirebaseDB(is_debug=False)

            if day_week <= 3:  # from monday to thursday send chist

                print(c.get_joke_send_joke())

            elif day_week == 4:     # Fridayyyyy, send any other thing if any
                print(c.get_joke_send_joke())

            else:                   # Saturday and sunday do nothing(..?)
                print("it's Saturday/Sunday motherdackeeerrrsss")
        else:
            print("No chiste sent, reason: 'not 8:30'")

    except:

        print(traceback.format_exc())

