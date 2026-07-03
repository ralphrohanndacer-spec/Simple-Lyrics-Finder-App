import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTextBrowser, QLabel
from PySide6.QtGui import QIcon
from network import req

class LyricsFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.trackLabel = QLabel("Track name")
        self.artistLabel = QLabel("Artist name")
        self.trackNameInput = QLineEdit()
        self.artistNameInput = QLineEdit()

        self.submitBtn = QPushButton("Submit")

        self.resultLabel = QTextBrowser()

        self.set_up_layouts()
        self.set_up_styles()
        self.perform()

    #Sets up the layouts
    def set_up_layouts(self):
        main_widget = QWidget()

        main_vbox_layout = QVBoxLayout()

        hbox_layout1 = QHBoxLayout()
        hbox_layout1.addWidget(self.trackLabel)
        hbox_layout1.addWidget(self.artistLabel)

        hbox_layout2 = QHBoxLayout()
        hbox_layout2.addWidget(self.trackNameInput)
        hbox_layout2.addWidget(self.artistNameInput)

        main_vbox_layout.addLayout(hbox_layout1)
        main_vbox_layout.addLayout(hbox_layout2)
        main_vbox_layout.addWidget(self.submitBtn)
        main_vbox_layout.addWidget(self.resultLabel)

        main_widget.setLayout(main_vbox_layout)
        self.setCentralWidget(main_widget)

    #Sets up the styles
    def set_up_styles(self):
        self.setWindowTitle("Lyrics Finder")
        self.setWindowIcon(QIcon("icon.png"))

        self.resize(500, 600)
        self.setMaximumHeight(600)

        self.trackNameInput.setPlaceholderText("Nightcall")
        self.artistNameInput.setPlaceholderText("Kavinsky")

        self.setStyleSheet("""
            QLabel, QLineEdit{
                font-size: 30px;
            }
            QLabel, QPushButton{
                color: hsl(348, 74%, 13%);
            }
            QPushButton{
                font-weight: bold;
                font-size: 20px;
                background-color: hsl(62, 0%, 50%);
            }
            QPushButton:pressed{
                background-color: hsl(62, 0%, 40%);
            }
           QLineEdit, QPushButton{
                padding: 5px;
                border: 1px solid;
                border-radius: 5px;
            }
            QTextBrowser{
                border: 1px solid;
                font-size: 18px;
            }
        """)

    #Handles widgets behavior
    def perform(self):
        self.submitBtn.clicked.connect(self.get_lyrics)

    #Displays result
    def get_lyrics(self):
        track_name = self.trackNameInput.text().strip()
        artist_name = self.artistNameInput.text().strip()

        if track_name and artist_name:
            self.resultLabel.setText("Searching...")
            req(track_name=track_name, artist_name=artist_name, ui=self)
        else:
            if not track_name and not artist_name:
                self.resultLabel.setText("Enter the track name and artist name first!")
            elif not track_name:
                self.resultLabel.setText("Enter the track name!")
            elif not artist_name:
                self.resultLabel.setText("Enter the artist name!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lyricsFinder = LyricsFinder()
    lyricsFinder.show()
    sys.exit(app.exec())