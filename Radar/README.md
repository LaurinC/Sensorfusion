# Quick Start Guide
## Demo Firmware Flash
- [Uniflash](https://www.ti.com/tool/UNIFLASH), [mmWave SDK](https://www.ti.com/tool/MMWAVE-SDK) und [CP210x Universal Windows Driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) downloaden und installieren
- [Anleitung](https://www.ti.com/lit/ug/swru546e/swru546e.pdf?ts=1709560091730&ref_url=https%253A%252F%252Fwww.ti.com%252Ftool%252FIWR6843ISK) unter Punkt 4.10 folgen
  - Bei erfolgreicher installation des Treibers sollten 2 neue COM Ports im Gerätemanager erscheinen ("Enhanced COM Port" und "Standard COM Port")
  - Für den Flash benötigte Firmware Datei sollte unter C:/ti/mmwave_sdk_03_06_02_00-LTS/packages/ti/demo/xwr68xx/mmw/xwr68xx_mmw_demo.bin auffindbar sein
  - Wenn es zu Problemen beim Flash kommt kann ein Hard-Reset helfen

## mmWave Demo Visualizer
- zum ausprobieren und parametrisieren kann ein von TI zur Verfügung gestelltes [Frontend](https://dev.ti.com/gallery/view/mmwave/mmWave_Demo_Visualizer/ver/3.6.0/) verwendet werden
- Die installation wird auf der Website erklärt, es muss unter anderem ein Browserextension und der Ti Cloud Agent installiert werden
- Falls die Ports nicht automatisch erkannt werden sollten:
  - Application Port: Enhanced COM
  - Data Port: Standard COM
  - Hard Reset des Sensors

## Python Interface
- Solltet ihr noch kein Python installiert haben würde ich euch [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) als Venv Manager und [VS Code](https://code.visualstudio.com/download) als Text Editor empfehlen
- Ein Prototyp des Interfaces kann unter test.py ausprobiert werden
  - Dazu müssen in der com dictionary unter 'conf_port' der Portname des Enhanced COM und unter 'data_port' der Name des Standard COM angegeben werden

