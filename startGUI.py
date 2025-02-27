import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextBrowser, QMessageBox
)
from PyQt6.QtCore import Qt
from game_settings import GameSettingsWindow

# Database and file names
DB_NAME = "highscores.db"
HIGHSCORE_TABLE = "highscores"
RULES_FILE = "rules.txt"
README_FILE = "README.md"

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quiz Game")
        self.setGeometry(200, 200, 400, 350)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.text_prompt = QLabel("Welcome to the Quiz Game!\nChoose an option:")
        self.text_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_prompt)

        self.btn_open_db = self.create_button("View Highscores", self.view_highscores)
        layout.addWidget(self.btn_open_db)

        self.btn_new_game = self.create_button("New Game", self.new_game)
        layout.addWidget(self.btn_new_game)

        self.btn_show_rules = self.create_button("Show Rules", self.show_rules)
        layout.addWidget(self.btn_show_rules)

        self.btn_show_readme = self.create_button("Show README", self.show_readme)
        layout.addWidget(self.btn_show_readme)

        self.setLayout(layout)
        self.highscore_window = None
        self.readme_window = None
        self.rules_window = None

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        button.setStyleSheet(
            "background-color: #444; color: white; border: 2px solid #61dafb; "
            "border-radius: 10px; padding: 10px; font-size: 14px;"
        )
        return button

    def view_highscores(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(f"SELECT player_name, score FROM {HIGHSCORE_TABLE} ORDER BY score DESC")
            data = cursor.fetchall()
            conn.close()

            if not data:
                QMessageBox.information(self, "Highscores", "No highscores available.")
                return

            if self.highscore_window is None or not self.highscore_window.isVisible():
                self.highscore_window = HighscoreWindow(data)
                self.highscore_window.show()
            else:
                self.highscore_window.raise_()
        except sqlite3.OperationalError as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")

    def new_game(self):
        if not hasattr(self, 'game_settings_window') or not self.game_settings_window.isVisible():
            self.game_settings_window = GameSettingsWindow()
            self.game_settings_window.show()
        else:
            self.game_settings_window.raise_()

    def show_rules(self):
        try:
            with open(RULES_FILE, "r", encoding="utf-8") as file:
                content = file.read()
                if self.rules_window is None or not self.rules_window.isVisible():
                    self.rules_window = ScrollableTextWindow("Game Rules", content)
                    self.rules_window.show()
                else:
                    self.rules_window.raise_()
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"File '{RULES_FILE}' not found!")

    def show_readme(self):
        try:
            with open(README_FILE, "r", encoding="utf-8") as file:
                content = file.read()
                if self.readme_window is None or not self.readme_window.isVisible():
                    self.readme_window = ScrollableTextWindow("README", content, markdown=True)
                    self.readme_window.show()
                else:
                    self.readme_window.raise_()
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"File '{README_FILE}' not found!")

class HighscoreWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Highscores")
        self.setGeometry(200, 150, 600, 400)
        self.setStyleSheet("background-color: #282c34; color: white; font-size: 18px;")

        layout = QVBoxLayout()

        self.text_edit = QTextBrowser()
        self.text_edit.setOpenExternalLinks(True)
        self.text_edit.setStyleSheet("background-color: #1e2127; color: #61dafb; border: none; padding: 10px;")
        self.text_edit.setHtml("<br>".join([f"<center><b style='color:#ffcc00;'>{i+1}. {row[0]}</b> - <span style='color:#00ff00;'>{row[1]} points</span></center>"
                                           for i, row in enumerate(data)]))
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("background-color: #444; color: white; border-radius: 10px; padding: 10px;")

        layout.addWidget(self.text_edit)
        layout.addWidget(close_button)
        self.setLayout(layout)

class ScrollableTextWindow(QWidget):
    def __init__(self, title, content, markdown=False):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 600, 500)

        layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        if markdown:
            self.text_browser.setMarkdown(content)
        else:
            self.text_browser.setPlainText(content)
        self.text_browser.setStyleSheet("font-size: 18px; padding: 10px;")
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("background-color: #444; color: white; border-radius: 10px; padding: 10px;")

        layout.addWidget(self.text_browser)
        layout.addWidget(close_button)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec())
