from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

from model.notifica import TipoNotifica


class NotificheView(QWidget):

    def __init__(self, utente_ctrl, notifica_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.notifica_ctrl = notifica_ctrl

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        titolo = QLabel("Notifiche")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titolo)

        filtro_row = QHBoxLayout()

        lbl_filtro = QLabel("Filtra per tipo:")
        filtro_row.addWidget(lbl_filtro)

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItem("Tutte", userData=None)

        # Aggiungiamo tutti i tipi di notifica definiti nell'enum
        for t in TipoNotifica:
            self.combo_tipo.addItem(t.value, userData=t)

        self.combo_tipo.currentIndexChanged.connect(self.refresh)
        filtro_row.addWidget(self.combo_tipo)

        layout.addLayout(filtro_row)

        self.lista_notifiche = QListWidget()
        layout.addWidget(self.lista_notifiche)

        btn_row = QHBoxLayout()

        btn_refresh = QPushButton("Aggiorna")
        btn_refresh.clicked.connect(self.refresh)
        btn_row.addWidget(btn_refresh)

        btn_elimina = QPushButton("Elimina notifica selezionata")
        btn_elimina.clicked.connect(self.elimina_notifica)
        btn_row.addWidget(btn_elimina)

        layout.addLayout(btn_row)

    def refresh(self):
        self.lista_notifiche.clear()

        utente = self.utente_ctrl.get_utente_attivo()
        if not utente:
            return

        tipo_selezionato = self.combo_tipo.currentData()

        if tipo_selezionato is None:
            # tutte le notifiche
            notifiche = self.notifica_ctrl.notifiche_utente(utente.id)
        else:
            # filtrate per tipo
            notifiche = self.notifica_ctrl.notifiche_per_tipo(utente.id, tipo_selezionato)

        for n in notifiche:
            data_str = n.dataInvio.strftime("%d/%m/%Y %H:%M")
            testo = f"[{data_str}] ({n.tipo.value}) {n.descrizione}"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, n.id)
            self.lista_notifiche.addItem(item)

    def elimina_notifica(self):
        item = self.lista_notifiche.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona notifica.")
            return

        id_notifica = item.data(Qt.ItemDataRole.UserRole)

        conferma = QMessageBox.question(self, "Conferma", "Elimina notifica?")
        if conferma != QMessageBox.StandardButton.Yes:
            return

        ok = self.notifica_ctrl.elimina_notifica(id_notifica)

        if ok:
            QMessageBox.information(self, "OK", "Notifica eliminata.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile eliminare la notifica.")
