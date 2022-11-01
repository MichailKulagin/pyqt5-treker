from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication
import pickle
import os

#print(os.path.realpath(__file__))
dirname, filename = os.path.split(os.path.realpath(__file__))
print(dirname)
Form, Window = uic.loadUiType(dirname+"\\treker.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def seve_to_file():
    global start_date, calc_date, discription
    date_to_save = {"start": start_date, "end" : calc_date, "desc" : discription}
    file1 = open("config.txt", 'wb')
    pickle.dump(date_to_save, file1)
    file1.close()


def read_from_file():
    global start_date, calc_date, discription, now_date
    try:
        file1 = open("config.txt", 'rb')
        date_to_load = pickle.load(file1)
        file1.close()
        start_date = date_to_load["start"]
        calc_date = date_to_load["end"]
        discription = date_to_load["desc"]
        print(start_date.toString("dd-MM-yyyy"), calc_date.toString("dd-MM-yyyy"), discription)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(discription)
        delta_days_left = start_date.daysTo(now_date) # прошло дней
        delta_days_right = now_date.daysTo(calc_date) # осталось дней
        days_total = start_date.daysTo(calc_date)     # всего дней
        print('$$$:', delta_days_left, delta_days_right, days_total)
        procent = int(delta_days_left * 100 / days_total)
        print(procent)
        form.progressBar.setProperty("value", procent)

    except:
        print("Немогу прочитать файл config.txt (может его нет )")


def on_click():
    global calc_date, discription, start_date
    start_date = now_date
    calc_date = form.calendarWidget.selectedDate()
    discription = form.plainTextEdit.toPlainText()
    """print(form.plainTextEdit.toPlainText())
    print(form.dateEdit.dateTime().toString("dd-MM-yyyy"))"""
    print("Clicked!!")
    seve_to_file()
    """print(form.calendarWidget.selectedDate().toString("dd-MM-yyyy"))
    date = QDate(2022, 9, 17)
    form.calendarWidget.setSelectedDate(date)"""

def on_click_calendar():
    global start_date, calc_date
    # print(form.calendarWidget.selectedDate().toString("dd-MM-yyyy"))
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days)



def on_dateedit_change():
    global start_date, calc_date
    #print(form.dateEdit.dateTime().toString("dd-MM-yyyy"))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days)
    form.label_3.setText("До наступления события осталась: %s дней" %delta_days)

form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)


start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
discription = form.plainTextEdit.toPlainText()
read_from_file()
form.label.setText("Трекер события от: %s" % start_date.toString("dd-MM-yyyy"))
form.label_2.setText("Опишите событие:")
on_click_calendar()



app.exec()

