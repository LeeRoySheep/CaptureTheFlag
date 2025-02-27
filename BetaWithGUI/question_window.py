import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton, QButtonGroup, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from io import BytesIO

class QuestionWindow(QWidget):
    def __init__(self, image_url, question_text, players, rounds, scores, answers=None):
        super().__init__()
        self.players = players
        self.rounds = rounds
        self.scores = scores
        self.setWindowTitle("Question")
        self.setGeometry(300, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        # Question Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        self.load_question_image(image_url)
        
        # Question Text
        self.label_question = QLabel(question_text)
        self.label_question.setWordWrap(True)
        self.label_question.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.label_question)
        
        # Answer Section
        self.answers = answers
        if self.answers:
            self.button_group = QButtonGroup()
            for answer in self.answers:
                btn = QRadioButton(answer)
                self.button_group.addButton(btn)
                layout.addWidget(btn)
        else:
            self.answer_input = QLineEdit()
            self.answer_input.setStyleSheet("font-size: 16px; height: 30px;")
            layout.addWidget(self.answer_input)
        
        # Submit Button
        self.btn_submit = QPushButton("Submit Answer")
        self.btn_submit.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.btn_submit)
        
        self.setLayout(layout)
    
    def load_question_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(img_data.getvalue())
            self.image_label.setPixmap(pixmap.scaled(500, 250, Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print(f"Error loading image: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionWindow("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Flag_of_Egypt.svg/240px-Flag_of_Egypt.svg.png", "What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"])
    window.show()
    sys.exit(app.exec())
