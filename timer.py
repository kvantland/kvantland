from login import do_login, current_user
from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import nav
import json
from html import escape
from config import config
import urllib.request as urllib2
import urllib.parse


class Timer:
    time_ = 5400 - 1  # 3/2 hours == 5400 seconds

    def display_timer(self):
        if self.time_ == 0:
            redirect('/tournament1_results')
        hours = self.time_ // 3600
        minutes = self.time_ % 3600 // 60
        seconds = self.time_ % 60

        def representation(n):
            if n < 10:
                return '0' + str(n)
            return str(n)

        time_str = representation(minutes) + ':' + representation(seconds)

        if hours != 0:
            time_str = str(hours) + ':' + time_str
        self.time_ -= 1
        return time_str


@route('/tournament1_results')
def results_page():
    yield from display_results_page(current_user())


def display_results_page(user):
    yield '<!DOCTYPE html>'
    yield '<h1> Поздравляем с окончанием первого турнира! </h1>'
