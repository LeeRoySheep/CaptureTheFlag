import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# Sample questions
"""questions = [
    {"question": "What is the capital of France?", "options": ["Berlin", "Paris", "Rome", "Madrid"], "answer": "Paris"},
    {"question": "What is 5 + 3?", "options": ["5", "8", "12", "7"], "answer": "8"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Venus", "Mars", "Jupiter"],
     "answer": "Mars"},
]"""


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capture the Flag")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.question_label = QLabel("")
        self.layout.addWidget(self.question_label)

        self.buttons = []
        for _ in range(4):  # Four answer buttons
            btn = QPushButton("")
            btn.clicked.connect(self.check_answer)
            self.layout.addWidget(btn)
            self.buttons.append(btn)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

        self.current_question = 0
        self.score = 0
        self.load_question()

    def load_question(self,players,questions):
        """Loads the current question and updates buttons"""
        if self.current_question < len(questions):
            q_data = questions[self.current_question]
            self.question_label.setText(q_data["question"])
            for i, option in enumerate(q_data["options"]):
                self.buttons[i].setText(option)
                self.buttons[i].setEnabled(True)  # Re-enable buttons
            self.result_label.setText("")
        else:
            self.question_label.setText(f"Quiz Over! Your Score: {self.score}/{len(questions)}")
            for btn in self.buttons:
                btn.hide()  # Hide buttons when quiz ends

    def check_answer(self,question):
        """Checks the answer when a button is clicked"""
        clicked_button = self.sender()
        selected_answer = clicked_button.text()
        correct_answer = questions[self.current_question]["answer"]

        if selected_answer == correct_answer:
            self.result_label.setText("✅ Correct!")
            self.score += 1
        else:
            self.result_label.setText(f"❌ Wrong! Correct: {correct_answer}")

        self.current_question += 1
        self.load_question()


# Run the app
app = QApplication(sys.argv)
quiz = QuizApp()
quiz.show()
sys.exit(app.exec())
