from PyQt6.QtWidgets import *
from gui import *
import csv
import re

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_submit.clicked.connect(lambda : self.submit())

        self.button_results.clicked.connect(lambda : self.results())

        self.button_back.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))

    def submit(self):
        try:
            voter_id = self.input_id.text()
            if len(voter_id) != 4:
                raise ValueError("Enter a valid 4 digit voter ID")
            for digit in voter_id:
                if not digit.isdigit():
                    raise ValueError("Enter a valid 4 digit voter ID")
            with open('votes.csv', 'r') as csvfile:
                if re.search(voter_id, csvfile.read()):
                    raise ValueError(f'Voter {voter_id} has already voted')

            vote = self.radio_group.checkedButton()
            if vote:
                vote = vote.text()
            else:
                raise ValueError("Please select a candidate")
        except ValueError as error:
            self.label_help.setText(str(error))
            self.label_help.setStyleSheet("color: red;")
        else:
            with open('votes.csv', 'a') as csvfile:
                content = csv.writer(csvfile)
                content.writerow([voter_id, vote])
            self.input_id.clear()
            if self.radio_group.checkedButton() is not None:
                self.radio_group.setExclusive(False)
                self.radio_group.checkedButton().setChecked(False)
                self.radio_group.setExclusive(True)
            self.label_help.setText("Your vote has been submitted")
            self.label_help.setStyleSheet("")
            self.input_id.setFocus()

    def results(self):
        self.stackedWidget.setCurrentIndex(1)
        self.label_totalJane.setStyleSheet("")
        self.label_totalJohn.setStyleSheet("")
        total_jane = 0
        total_john = 0
        with open('votes.csv', 'r') as csvfile:
            content = csv.reader(csvfile, delimiter=',')
            for line in content:
                if line[1] == "Jane":
                    total_jane += 1
                elif line[1] == "John":
                    total_john +=1
        self.label_totalJane.setText(f'{total_jane} Jane')
        self.label_totalJohn.setText(f'{total_john} John')
        if total_jane > total_john:
            self.label_totalJane.setStyleSheet("color: green;")
        elif total_john > total_jane:
            self.label_totalJohn.setStyleSheet("color: green;")
