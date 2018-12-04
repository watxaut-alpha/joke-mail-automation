import traceback
from datetime import datetime
import time
from core.firebase import JokeFirebaseDB

if __name__ == '__main__':
    # This code will launch a

    try:

        # initializes the Firebase needed authentication
        c = JokeFirebaseDB(is_debug=False)

        # define at which our do you want to send the joke
        i_hour = 8
        i_min = 30
        i_sec = 0

        while True:

            if not c.debug:

                # get today's date and time
                x = datetime.today()

                # get the same date but at 8:30
                y = x.replace(day=x.day, hour=i_hour, minute=i_min, second=i_sec)

                # calculate how much time is left (or passed) from 8:30
                delta_t = y - x

                if delta_t.days < 0:
                    # means that the 8:30 is already past today, so calculate how many seconds do we need to wait
                    # until the next day at the same hour
                    y = x.replace(day=x.day + 1, hour=i_hour, minute=i_min, second=i_sec)
                    delta_t = y - x

                secs = delta_t.total_seconds()

                print('secs to wait:', secs, " s (or in hours hours): ", secs/3600.0)

                time.sleep(secs)  # sleep seconds for next joke

                # send and print output
                print(c.get_joke_send_joke())
            else:
                print(c.get_joke_send_joke())
                time.sleep(8)  # sleep seconds for next joke

    except:

        print(traceback.format_exc())


