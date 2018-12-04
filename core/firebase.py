# coding=utf-8
import smtplib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import traceback

import auth.gmail as gmail
import core.globvars as globvars


class JokeFirebaseDB(object):

    def __init__(self, is_debug=False):
        self.path_to_auth = r'../auth/firebase.json'
        self.url_path = globvars.firebase_http

        # init Firebase
        # Fetch the service account key JSON file contents
        self.cred = credentials.Certificate(self.path_to_auth)

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(self.cred, {'databaseURL': self.url_path})

        self.debug = is_debug

    def get_joke_send_joke(self):

        l_receivers = self.get_all_receivers(self.debug)

        s_chiste, author, rating = self.get_joke(self.debug)

        is_sent = self.send_mail(l_receivers, s_chiste, globvars.s_subject, globvars.s_disclaimer)
        return is_sent

    @staticmethod
    def get_all_receivers(is_debug):

        if not is_debug:
            ref_name = globvars.email_users_path
        else:
            ref_name = globvars.email_users_debug_path

        email_ref = db.reference(ref_name).get()

        if type(email_ref) == dict:
            return email_ref.values()
        elif type(email_ref) == list:
            return email_ref
        else:
            raise Exception("unknown type of email_ref: {}".format(type(email_ref)))

    @staticmethod
    def get_joke(is_debug):

        # As an admin, the app has access to read and write all data, regardless of Security Rules
        all_jokes = db.reference(globvars.db_jokes_path).get()

        # reverse list so that later jokes are the first ones
        reversed_list = zip(range(len(all_jokes)), all_jokes)
        reversed_list.reverse()

        for i_joke, d_joke in reversed_list:
            if d_joke is not None:
                if d_joke['used'] == 0:
                    s_joke = d_joke["xist"]  # xist means 'joke'
                    rating = d_joke["rating"]
                    author = d_joke["author"]
                    d_joke['used'] = 1

                    if not is_debug:
                        # get the reference for the joke and set used to 1
                        used_joke_ref = db.reference("{}/{}/used".format(globvars.db_jokes_path, i_joke))
                        used_joke_ref.set(d_joke['used'])

                    break
        else:  # all jokes used!!!1
            raise Exception("ALL JOKES USED!")

        return s_joke, author, rating

    @staticmethod
    def send_mail(l_receivers, s_joke, subject, s_disclaimer):

        email_text = "From: {}\nTo: {}\nSubject: {}\n\n{}\n\n\n{}".format(gmail.USER,
                                                                          ",".join(l_receivers),
                                                                          subject,
                                                                          s_joke,
                                                                          s_disclaimer)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail.USER, gmail.PASSWORD)

            server.sendmail(gmail.USER, l_receivers, email_text)
            server.close()

            print('Email sent!', email_text)
            return True

        except:
            print('Something went wrong...')
            print(traceback.format_exc())
            return False

