# Importiere die notwendigen Bibliotheken
import sys
import os
import moviepy.editor as mp
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QComboBox, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt
from mutagen.id3 import ID3, TPE1, TCOM, TCON, TALB, TRCK, TYER, APIC, TCOP, TPUB, error
from mutagen.mp3 import MP3

# Definiere die Klasse für den MP4 zu MP3 Konverter
class Mp4ToMp3Converter(QWidget):
    # Initialisiere die Klasse
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP4 zu MP3 Konverter")  # Setze den Fenstertitel
        self.setGeometry(100, 100, 400, 200)  # Setze die Fenstergröße
        self.initUI()  # Initialisiere die Benutzeroberfläche

    # Methode zur Initialisierung der Benutzeroberfläche
    def initUI(self):
        self.setup_background_and_font()  # Hintergrund und Schriftart einstellen
        self.create_widgets()  # Widgets erstellen
        self.create_layout()  # Layout erstellen
        self.setup_connections()  # Verbindungen einrichten

    # Methode zum Einstellen von Hintergrundbild und Schriftart
    def setup_background_and_font(self):
        self.hintergrund = QPixmap('convert.jpg').scaled(self.size(), Qt.KeepAspectRatioByExpanding)  # Lade und skaliere das Hintergrundbild
        palette = QPalette()  # Erstelle eine Palette
        palette.setBrush(QPalette.Window, QBrush(self.hintergrund))  # Setze den Pinsel der Palette
        self.setPalette(palette)  # Wende die Palette auf das Widget an

        # Setze den Stil für Labels und Buttons
        self.setStyleSheet("""
        QLabel, QPushButton {
            color: red;
            font-size: 24pt;
        }
        """)

        self.schriftart = QFont()  # Erstelle eine Schriftart
        self.schriftart.setPointSize(40)  # Setze die Schriftgröße
        self.setFont(self.schriftart)  # Wende die Schriftart an

    # Methode zum Erstellen der Widgets
    def create_widgets(self):
        self.quality_label = QLabel("Qualität:")  # Erstelle ein Label für die Qualität
        self.quality_combo = QComboBox()  # Erstelle eine Dropdown-Liste für die Qualität
        self.quality_combo.addItems(["Schlecht", "Mittel", "Hoch"])  # Füge Optionen zur Dropdown-Liste hinzu

        self.select_button = QPushButton("MP4 Dateien auswählen")  # Erstelle einen Button zum Auswählen von Dateien
        self.convert_button = QPushButton("Konvertieren")  # Erstelle einen Button zum Starten der Konvertierung

        self.album_label = QLabel("Album:")  # Erstelle ein Label für das Album
        self.album_input = QLineEdit()  # Erstelle ein Eingabefeld für das Album
        self.track_label = QLabel("Track:")  # Erstelle ein Label für den Track
        self.track_input = QLineEdit()  # Erstelle ein Eingabefeld für den Track

    # Methode zum Erstellen des Layouts
    def create_layout(self):
        layout = QVBoxLayout()  # Erstelle ein vertikales Layout
        # Füge die Widgets zum Layout hinzu
        layout.addWidget(self.quality_label)
        layout.addWidget(self.quality_combo)
        layout.addWidget(self.select_button)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.album_label)
        layout.addWidget(self.album_input)
        layout.addWidget(self.track_label)
        layout.addWidget(self.track_input)

        self.setLayout(layout)  # Wende das Layout auf das Widget an

    # Methode zum Einrichten der Verbindungen
    def setup_connections(self):
        self.select_button.clicked.connect(self.select_files)  # Verbinde den Auswählen-Button mit der Methode zum Auswählen von Dateien
        self.convert_button.clicked.connect(self.convert_to_mp3)  # Verbinde den Konvertieren-Button mit der Methode zum Konvertieren

    # Methode zum Auswählen von Dateien
    def select_files(self):
        options = QFileDialog.Options()  # Erstelle Optionen für den Dateidialog
        # Öffne den Dateidialog und speichere die ausgewählten Dateien
        files, _ = QFileDialog.getOpenFileNames(self, "MP4 Dateien auswählen", "", "MP4 Dateien (*.mp4)", options=options)
        if files:  # Wenn Dateien ausgewählt wurden
            self.files = files  # Speichere die Dateien
        else:  # Wenn keine Dateien ausgewählt wurden
            QMessageBox.warning(self, "Keine Dateien ausgewählt", "Bitte wählen Sie mindestens eine MP4-Datei aus.")  # Zeige eine Warnung an

    # Methode zum Konvertieren von Dateien
    def convert_to_mp3(self):
        if not hasattr(self, 'files'):  # Wenn keine Dateien ausgewählt wurden
            QMessageBox.warning(self, "Keine Dateien ausgewählt", "Bitte wählen Sie zuerst die Dateien aus.")  # Zeige eine Warnung an
            return  # Beende die Methode

        quality = self.quality_combo.currentText().lower()  # Hole die ausgewählte Qualität
        album = self.album_input.text()  # Hole den eingegebenen Albumnamen
        track = self.track_input.text()  # Hole die eingegebene Tracknummer
        self.show_message("Bitte warten, die Erstellung der MP3 startet...")  # Zeige eine Nachricht an

        for file in self.files:  # Für jede ausgewählte Datei
            try:
                video = mp.VideoFileClip(file)  # Lade das Video
                mp3_file = os.path.splitext(os.path.basename(file))[0] + ".mp3"  # Erstelle den Namen der MP3-Datei
                bitrate = self.get_bitrate(quality)  # Hole die Bitrate basierend auf der Qualität
                video.audio.write_audiofile(mp3_file, bitrate=bitrate)  # Schreibe die Audiospur als MP3-Datei
                self.set_id3_tags(mp3_file, "sunoAI", "Ralf Krümmel", album, track, "2024", "Viking Rock")  # Setze die ID3-Tags
            except Exception as e:  # Wenn ein Fehler auftritt
                QMessageBox.critical(self, "Fehler", f"Ein Fehler ist aufgetreten: {e}")  # Zeige eine Fehlermeldung an
                return  # Beende die Methode

        self.show_message("Konvertierung abgeschlossen!")  # Zeige eine Nachricht an, dass die Konvertierung abgeschlossen ist

    # Methode zum Abrufen der Bitrate basierend auf der Qualität
    def get_bitrate(self, quality):
        bitrate_options = {
            "schlecht": "32k",  # Bitrate für schlechte Qualität
            "mittel": "128k",  # Bitrate für mittlere Qualität
            "hoch": "320k"  # Bitrate für hohe Qualität
        }
        return bitrate_options.get(quality, "128k")  # Gib die entsprechende Bitrate zurück

    # Methode zum Setzen der ID3-Tags
    def set_id3_tags(self, mp3_file, artist, composer, album, track, year, genre, cover_art=None):
        audio = MP3(mp3_file, ID3=ID3)  # Lade die MP3-Datei

        try:
            audio.add_tags()  # Versuche, Tags hinzuzufügen
        except error:  # Wenn die Tags bereits existieren
            pass  # Ignoriere den Fehler

        # Füge die verschiedenen Tags hinzu
        audio.tags.add(TPE1(encoding=3, text=artist))  # Künstler/Interpret
        audio.tags.add(TCOM(encoding=3, text=composer))  # Komponist
        audio.tags.add(TALB(encoding=3, text=album))  # Album
        audio.tags.add(TRCK(encoding=3, text=track))  # Tracknummer
        audio.tags.add(TYER(encoding=3, text=year))  # Jahr
        audio.tags.add(TCON(encoding=3, text=genre))  # Genre
        audio.tags.add(TCOP(encoding=3, text="Ja"))  # Geschützt-Status
        audio.tags.add(TPUB(encoding=3, text="Ralf Krümmel"))  # Herausgeber



        if cover_art:  # Wenn ein Cover-Bild angegeben wurde
            with open(cover_art, 'rb') as albumart:  # Öffne das Bild
                audio.tags.add(APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,  # Cover (front)
                    desc=u'Cover (front)',
                    data=albumart.read()
                ))

        audio.save()

    def show_message(self, message):
        self.message_label = QLabel(message)
        self.message_label.show()
        QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = Mp4ToMp3Converter()
    converter.show()
    sys.exit(app.exec())
