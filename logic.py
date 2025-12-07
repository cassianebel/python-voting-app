from PyQt6.QtWidgets import *
from gui import *
import csv
import re

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_submit.clicked.connect(lambda : self.submit())

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