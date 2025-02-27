import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt

class GameSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Settings")
        self.setGeometry(300, 200, 600, 400)
        
        main_layout = QHBoxLayout()
        settings_layout = QVBoxLayout()
        players_layout = QVBoxLayout()
        
        # Number of Players
        self.label_players = QLabel("Number of Players:")
        self.spin_players = QSpinBox()
        self.spin_players.setMinimum(1)
        self.spin_players.setMaximum(10)
        self.spin_players.setFixedWidth(80)
        self.spin_players.setStyleSheet("font-size: 16px; height: 30px;")
        
        # Number of Rounds
        self.label_rounds = QLabel("Number of Rounds:")
        self.spin_rounds = QSpinBox()
        self.spin_rounds.setMinimum(1)
        self.spin_rounds.setMaximum(20)
        self.spin_rounds.setFixedWidth(80)
        self.spin_rounds.setStyleSheet("font-size: 16px; height: 30px;")
        
        # Difficulty Level
        self.label_difficulty = QLabel("Difficulty:")
        self.combo_difficulty = QComboBox()
        self.combo_difficulty.addItems(["Beginner", "Pro"])
        self.combo_difficulty.setStyleSheet("font-size: 16px; height: 30px;")
        
        # Add to Settings Layout
        settings_layout.addWidget(self.label_players)
        settings_layout.addWidget(self.spin_players)
        settings_layout.addWidget(self.label_rounds)
        settings_layout.addWidget(self.spin_rounds)
        settings_layout.addWidget(self.label_difficulty)
        settings_layout.addWidget(self.combo_difficulty)
        settings_layout.addStretch()
        
        # Player Names (Right Side)
        self.label_names = QLabel("Enter Player Names:")
        players_layout.addWidget(self.label_names)
        self.player_inputs = []
        self.grid_layout = QGridLayout()
        players_layout.addLayout(self.grid_layout)
        
        self.spin_players.valueChanged.connect(self.update_player_fields)
        self.update_player_fields()
        
        # Commit Button
        self.btn_commit = QPushButton("Start Game")
        self.btn_commit.setStyleSheet("font-size: 16px; padding: 10px;")
        
        # Add Layouts to Main Layout
        main_layout.addLayout(settings_layout, 1)
        main_layout.addLayout(players_layout, 2)
        
        self.setLayout(main_layout)
        players_layout.addWidget(self.btn_commit)
    
    def update_player_fields(self):
        # Clear previous inputs
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.player_inputs.clear()
        
        # Add new player name fields
        for i in range(self.spin_players.value()):
            label = QLabel(f"Player {i+1}:")
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 16px; height: 30px;")
            self.grid_layout.addWidget(label, i, 0)
            self.grid_layout.addWidget(input_field, i, 1)
            self.player_inputs.append(input_field)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameSettingsWindow()
    window.show()
    sys.exit(app.exec())
