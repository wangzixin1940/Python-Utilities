import os
import json
os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["clock"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


from turtle import *
from datetime import datetime


def jump(distanz, winkel=0):
    penup()
    right(winkel)
    forward(distanz)
    left(winkel)
    pendown()


def hand(laenge, spitze):
    fd(laenge * 1.15)
    rt(90)
    fd(spitze / 2.0)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze / 2.0)


def make_hand_shape(name, laenge, spitze):
    reset()
    jump(-laenge * 0.15)
    begin_poly()
    hand(laenge, spitze)
    end_poly()
    hand_form = get_poly()
    register_shape(name, hand_form)


def clockface(radius):
    reset()
    pensize(7)
    for i in range(60):
        jump(radius)
        if i % 5 == 0:
            fd(25)
            jump(-radius - 25)
        else:
            dot(3)
            jump(-radius)
        rt(6)


def setup():
    global second_hand, minute_hand, hour_hand, writer
    mode("logo")
    make_hand_shape("second_hand", 125, 25)
    make_hand_shape("minute_hand", 130, 25)
    make_hand_shape("hour_hand", 90, 25)
    clockface(160)
    second_hand = Turtle()
    second_hand.shape("second_hand")
    second_hand.color("gray20", "gray80")
    minute_hand = Turtle()
    minute_hand.shape("minute_hand")
    minute_hand.color("blue1", "red1")
    hour_hand = Turtle()
    hour_hand.shape("hour_hand")
    hour_hand.color("blue3", "red3")
    for hand in second_hand, minute_hand, hour_hand:
        hand.resizemode("user")
        hand.shapesize(1, 1, 3)
        hand.speed(0)
    ht()
    writer = Turtle()
    # writer.mode("logo")
    writer.ht()
    writer.pu()
    writer.bk(85)


def wochentag(t):
    wochentag = ui["days"]
    return wochentag[t.weekday()]


def datum(z):
    monat = ui["month"]
    j = z.year
    m = monat[z.month - 1]
    t = z.day
    return "%s %d %d" % (m, t, j)


def tick():
    t = datetime.today()
    sekunde = t.second + t.microsecond * 0.000001
    minute = t.minute + sekunde / 60.0
    stunde = t.hour + minute / 60.0
    try:
        tracer(False)  # Terminator can occur here
        writer.clear()
        writer.home()
        writer.forward(65)
        writer.write(wochentag(t),
                     align="center", font=("Courier", 14, "bold"))
        writer.back(150)
        writer.write(datum(t),
                     align="center", font=("Courier", 14, "bold"))
        writer.forward(85)
        second_hand.setheading(6 * sekunde)  # or here
        minute_hand.setheading(6 * minute)
        hour_hand.setheading(30 * stunde)
        tracer(True)
        ontimer(tick, 100)
    except Terminator:
        pass  # turtledemo user pressed STOP


def main():
    title(ui["title"])
    tracer(False)
    setup()
    tracer(True)
    tick()
    return "EVENTLOOP"


if __name__ == "__main__":
    mode("logo")
    msg = main()
    print(msg)
    mainloop()
