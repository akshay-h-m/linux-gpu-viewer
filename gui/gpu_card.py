from PyQt5 import QtWidgets

class GPUCard(QtWidgets.QFrame):
    def __init__(self, info, vendor_name):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        layout = QtWidgets.QGridLayout(self)
        row = 0

        title = f"{vendor_name} ({info.get('Bus')})"
        lbl_title = QtWidgets.QLabel(f"<b>{title}</b>")
        layout.addWidget(lbl_title, row, 0, 1, 2)
        row += 1

        for key in ['Driver', 'IRQ', 'PCI Class']:
            lbl_k = QtWidgets.QLabel(key + ":")
            lbl_v = QtWidgets.QLabel(info.get(key, 'N/A'))
            layout.addWidget(lbl_k, row, 0)
            layout.addWidget(lbl_v, row, 1)
            row += 1
