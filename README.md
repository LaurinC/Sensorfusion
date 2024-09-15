# Sensorfusion
Bachelorprojekt zur Darstellung der Sensorfusion von Radar und Kamera

# Quick Start Guide
# Setup Repository
Klonen und Ausführungsumgebung erstellen
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# Ausführen
Annahme: Radar mit Firmware geflasht, Kamera kalibriert und dazugehörige Koeffizienten in fusion/coefficients abgelegt
```
python main.py
```
- Möglichkeit die volle Kameraauflösung zu verwenden, aber auf dem Testsystem (Raspberry Pi 5) nicht performant genug

