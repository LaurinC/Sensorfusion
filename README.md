# Quick Start Guide 
## Setup Repository
Kreiere virtual enviroment, aktivieren und installiere requirements
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Aufnahme von Kalibrationsbildern (Benötigt Kalibrierungstarget)
![Kalibrierungstarget](https://github.com/LaurinC/Sensorfusion/blob/calibration/images/wide_lense_3/10.jpg?raw=true)
```
python calibration.py --mode grab --cam 0 --out name --num_imgs 50
```
- Programm begleitet durch die Schritte
- Schlechte Aufnahmen (Unscharf, Target nicht vollständig im Bild) müssen vom Nutzer manuell vor der Kalibrierung bereinigt werden

## Kalibrierung (Benötigt Kalibrierungsbilder)
- --rows x und --cols y entsprechen der Anzahl der inneren Reihen und Spalten des Kalibrierungstarget, für das Beispielbild wären es 8 und 6
```
python calibration.py --mode calibrate --inp name --rows x --cols y 
```
- Ausgabe als name.json (Human Readable) und name.npz (Für die weitere Nutzung)
