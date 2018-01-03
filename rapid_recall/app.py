from browser import document,alert
from browser.html import P
import browser.timer
import math
import random
import time

right_questions = 0
wrong_questions = 0
timeout_questions = 0
started = 0
time_remaining= 7000
counted = 0


def handle_timer():
    global time_remaining
    global started
    global timeout_questions
    global counted
    if not started:
        return
    time_remaining -= 100
    if time_remaining <= 0:
        time_remaining = 6999
        started = 0
        document['indicator'].text = "Timer Not Running"
        document['declaration'].text = "Timed_out"
        document['declaration'].classList.add('decl_timeout')
        if not counted:
            timeout_questions += 1
            counted = 1
            document['timeout_questions'].text = str(timeout_questions)
            document['tot_questions'].text = str(right_questions + wrong_questions + timeout_questions)
    document['time_left'].text = "{0:.2d}".format(math.floor(time_remaining/1000) + 1)

def handle_start(event):
    global time_remaining
    global started
    global counted
    started = 1
    time_remaining = 6999
    document['time_left'].text = "{0:.2d}".format(math.floor(time_remaining/1000) + 1)
    document['indicator'].text = "Timer Started"
    document['number1'].text = "{0:.2d}".format(random.randint(2,10))
    document['number2'].text = "{0:.2d}".format(random.randint(2,10))
    document['result'].value = ""
    document['declaration'].text = ""
    document['declaration'].classList.remove('decl_right')
    document['declaration'].classList.remove('decl_wrong')
    document['declaration'].classList.remove('decl_timeout')
    document['result'].focus()
    counted = 0

def check_answer(event):
    global started
    global right_questions
    global wrong_questions
    global counted
    answer = int(document['result'].value)
    number1 = int(document['number1'].text)
    number2 = int(document['number2'].text)
    declare = ""
    if answer == number1 * number2:
        declare = "Correct"
        started = 0
        document['indicator'].text = "Timer Not Running"
        document['declaration'].classList.remove('decl_timeout')
        document['declaration'].classList.remove('decl_wrong')
        document['declaration'].classList.add('decl_right')
        document['next_btn'].focus()
        if not counted:
            right_questions += 1
            counted = 1
            document['right_questions'].text = str(right_questions)
            document['tot_questions'].text = str(right_questions + wrong_questions + timeout_questions)
    else:
        declare = "Wrong"
        document['declaration'].classList.remove('decl_timeout')
        document['declaration'].classList.add('decl_wrong')
        document['result'].focus()
        if not counted:
            wrong_questions += 1
            counted = 1
            document['wrong_questions'].text = str(wrong_questions)
            document['tot_questions'].text = str(right_questions + wrong_questions + timeout_questions)
    document['declaration'].text = declare

document['start_btn'].bind('click',handle_start)
document['next_btn'].bind('click',handle_start)
document['result'].bind('change',check_answer)
document['start_btn'].focus()
browser.timer.set_interval(handle_timer,100)
