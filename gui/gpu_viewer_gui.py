import sys, re
from PyQt5 import QtWidgets, QtCore
from pci_ids_parser import load_pci_ids
from gpu_card import GPUCard

PROC = "/proc/gpu_viewer"

class GPUViewerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ids = load_pci_ids("data/pci.ids")
        self.setWindowTitle("GPU Viewer")
        self.resize(600, 400)
        layout = QtWidgets.QVBoxLayout()

        tb = QtWidgets.QHBoxLayout()
        self.btn_refresh = QtWidgets.QPushButton("⟳ Refresh")
        self.btn_refresh.clicked.connect(self.load)
        tb.addWidget(self.btn_refresh)
        layout.addLayout(tb)

        self.scroll = QtWidgets.QScrollArea()
        self.content = QtWidgets.QWidget()
        self.layout_cards = QtWidgets.QVBoxLayout(self.content)
        self.scroll.setWidget(self.content)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.load()

    def load(self):
        try:
            with open(PROC) as f:
                txt = f.read().splitlines()
        except:
            return
        cards = []
        info = {}
        for line in txt:
            if not line.strip():
                if info:
                    cards.append(info)
                info = {}
            elif ':' in line:
                k, v = line.split(":",1)
                info[k.strip()] = v.strip()
        if info:
            cards.append(info)

        for i in reversed(range(self.layout_cards.count())):
            self.layout_cards.itemAt(i).widget().setParent(None)

        for info in cards:
            vid = info.get("Vendor ID","")[2:].lower()
            vendor_name = self.ids.get(vid,"Unknown")
            card = GPUCard(info, vendor_name)
            self.layout_cards.addWidget(card)
