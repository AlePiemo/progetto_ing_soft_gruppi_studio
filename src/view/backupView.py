from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

class BackupView(QWidget):

    def __init__(self, backup_ctrl):
        super().__init__()

        self.backup_ctrl = backup_ctrl

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        titolo = QLabel("Gestione Backup")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titolo)


        lbl_storico = QLabel("Storico backup registrati")
        lbl_storico.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px;")
        layout.addWidget(lbl_storico)

        self.lista_backup = QListWidget()
        layout.addWidget(self.lista_backup)


        btn_backup = QPushButton("Esegui backup manuale")
        btn_backup.clicked.connect(self.backup_manuale)
        layout.addWidget(btn_backup)

        btn_refresh = QPushButton("Aggiorna elenco")
        btn_refresh.clicked.connect(self.refresh)
        layout.addWidget(btn_refresh)

        # Caricamento iniziale
        self.refresh()

    def refresh(self):
        self.lista_backup.clear()

        lista = self.backup_ctrl.lista_backup()

        for b in lista:
            data = b.dataBackup.strftime("%d/%m/%Y %H:%M")
            stato = b.statoBackup.value if hasattr(b.statoBackup, "value") else str(b.statoBackup)
            esito = "SUCCESSO" if b.esito else "FALLITO"

            testo = f"{data} | {stato} | {esito}"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, b.id)
            self.lista_backup.addItem(item)

    def backup_manuale(self):
        backup = self.backup_ctrl.backup_manuale()

        if backup.esito:
            QMessageBox.information(self, "Backup", "Backup completato con successo!")
        else:
            QMessageBox.warning(self, "Backup", "Backup fallito!")

        self.refresh()
