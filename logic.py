import csv
import os
from PyQt6.QtGui import QColor

class GradingLogic:
    def __init__(self, ui) -> None:
        '''
        Initializes variables
        '''
        self.ui = ui
        self.ui.AttemptsConfirm.clicked.connect(self.show_inputs)
        self.ui.SubmitButton.clicked.connect(self.submit_clicked)
        self.ui.ErrorLabel.setText('')
        self.ui.Score1Label.hide()
        self.ui.Score1Input.hide()
        self.ui.Score2Label.hide()
        self.ui.Score2Input.hide()
        self.ui.Score3Label.hide()
        self.ui.Score3Input.hide()
        self.ui.Score4Label.hide()
        self.ui.Score4Input.hide()

    def show_inputs(self) -> None:
        '''
        Handles name and attempts inputs
        Creates and shows input boxes
        '''
        student_name: str = self.ui.StudentInput.text().strip()
        if not student_name:  # confirms valid name
            self.raise_error("Please enter a student name", "red")
            return

        attempts_text: str = self.ui.ScoresInput.text()
        try:
            num_of_attempts: int = int(attempts_text)  # confirm valid number of attempts
            if num_of_attempts < 1 or num_of_attempts > 4:
                self.raise_error("Max number of attempts is 4", "red")
                return
            self.ui.ErrorLabel.setText("")

            for i in range(1, num_of_attempts + 1):  # creates correct number of score inputs
                label = getattr(self.ui, f"Score{i}Label")
                input_box = getattr(self.ui, f"Score{i}Input")
                label.show()
                input_box.show()
        except ValueError:
            self.raise_error("Invalid input for number of attempts", "red")
            return

    def submit_clicked(self) -> None:
        '''
        Takes in inputs for scores
        '''
        student_name: str = self.ui.StudentInput.text().strip()
        if not student_name:
            self.raise_error("Please enter a student name", "red")
            return

        scores: list[int] = []
        num_of_attempts: int = int(self.ui.ScoresInput.text())

        for i in range(1, 5):  # assigns score values
            input_box = getattr(self.ui, f"Score{i}Input")
            if i <= num_of_attempts:
                score_text: str = input_box.text()
            else:
                score_text: str = '0'

            if not self.score_validation(score_text):
                self.raise_error("Scores must be between 0 and 100", "yellow")
                return

            try:
                score: int = int(score_text)
                scores.append(score)
            except ValueError:
                self.raise_error(f"Invalid input for Score {i}", "yellow")
                return

        if scores:
            max_score: int = max(scores)
        else:
            max_score: int = 0

        self.write_to_csv(student_name, scores, max_score)

        self.ui.ErrorLabel.setText("Submitted")
        self.ui.ErrorLabel.setStyleSheet("color: green")

    def write_to_csv(self, student_name: str, scores: list[int], max_score: int) -> None:
        '''
        Writes the data from the gui to a csv
        '''
        header: list[int] = ['name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Final']
        file_exists: bool = os.path.isfile('grades.csv')

        with open('grades.csv', 'a', newline='') as csvfile:  # writes data to csv
            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(header)

            writer.writerow([student_name] + scores + [max_score])

    def score_validation(self, score_text: str) -> bool:
        '''
        Checks if score is between 0 and 100
        '''
        try:
            score: int = int(score_text)  # confirms valid score values
            return 0 <= score <= 100
        except ValueError:
            return False

    def raise_error(self, message: str, color: str) -> None:
        '''
        Takes in a message and color to create an error message
        '''
        self.ui.ErrorLabel.setText(message)
        self.ui.ErrorLabel.setStyleSheet(f"color: {color}")