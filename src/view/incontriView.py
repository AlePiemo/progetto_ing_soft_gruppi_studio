from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem,
    QDateEdit, QTimeEdit, QLineEdit, QTextEdit,
    QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt, QDate, QTime
from datetime import datetime

class IncontriView(QWidget):

    def __init__(self, utente_ctrl, gruppo_ctrl, incontro_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.gruppo_ctrl = gruppo_ctrl
        self.incontro_ctrl = incontro_ctrl

        self.gruppo_attuale = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.lbl_titolo = QLabel("Incontri del gruppo")
        self.lbl_titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.lbl_titolo)

        self.lista_incontri = QListWidget()
        layout.addWidget(self.lista_incontri)

        row = QHBoxLayout()

        btn_crea = QPushButton("Crea incontro")
        btn_crea.clicked.connect(self.crea_incontro)
        row.addWidget(btn_crea)

        btn_modifica = QPushButton("Modifica incontro")
        btn_modifica.clicked.connect(self.modifica_incontro)
        row.addWidget(btn_modifica)

        btn_annulla = QPushButton("Annulla incontro")
        btn_annulla.clicked.connect(self.annulla_incontro)
        row.addWidget(btn_annulla)

        btn_elimina = QPushButton("Elimina incontro")
        btn_elimina.clicked.connect(self.elimina_incontro)
        row.addWidget(btn_elimina)

        layout.addLayout(row)

    def apri_gruppo(self, id_gruppo):
        gruppo = self.gruppo_ctrl.get_gruppo(id_gruppo)

        if not gruppo:
            QMessageBox.warning(self, "Errore", "Gruppo non trovato.")
            return

        self.gruppo_attuale = gruppo
        self.lbl_titolo.setText(f"Incontri - {gruppo.nomeGruppo}")

        self.refresh_incontri()

    def refresh_incontri(self):
        self.lista_incontri.clear()

        if not self.gruppo_attuale:
            return

        incontri = self.incontro_ctrl.incontri_gruppo(self.gruppo_attuale.id)

        for inc in incontri:
            data = inc.dataIncontro.strftime("%d/%m/%Y")
            ora = inc.oraIncontro.strftime("%H:%M")
            stato = inc.statoIncontro.value

            testo = f"{inc.titolo} | {data} {ora} | {stato}"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, inc.id)
            self.lista_incontri.addItem(item)

    def crea_incontro(self):
        if not self.gruppo_attuale:
            return

        u = self.utente_ctrl.get_utente_attivo()
        if not u or u.id not in self.gruppo_attuale.amministratori:
            QMessageBox.warning(self, "Errore", "Solo gli admin possono creare incontri.")
            return

        titolo, ok = QInputDialog.getText(self, "Titolo incontro", "Titolo:")
        if not ok or not titolo:
            return

        descrizione, ok = QInputDialog.getMultiLineText(self, "Descrizione", "Descrizione:")
        if not ok:
            return

        data_w = QDateEdit()
        data_w.setDate(QDate.currentDate())
        data_w.setCalendarPopup(True)
        data = data_w.date().toPyDate()

        ora_w = QTimeEdit()
        ora_w.setTime(QTime.currentTime())

        ora = datetime.combine(datetime.today(), ora_w.time().toPyTime())

        data_dt = datetime.combine(data, datetime.min.time())
        ora_dt = datetime.combine(datetime.today(), ora.time())

        nuovo = self.incontro_ctrl.crea_incontro(
            id_gruppo=self.gruppo_attuale.id,
            id_admin=u.id,
            titolo=titolo,
            descrizione=descrizione,
            data=data_dt,
            ora=ora_dt
        )

        if nuovo:
            QMessageBox.information(self, "OK", "Incontro creato.")
            self.refresh_incontri()
        else:
            QMessageBox.warning(self, "Errore", "Creazione fallita.")

    def modifica_incontro(self):
        item = self.lista_incontri.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona un incontro.")
            return

        inc_id = item.data(Qt.ItemDataRole.UserRole)

        inc = self.incontro_ctrl.get_incontro(inc_id)

        if not inc:
            QMessageBox.warning(self, "Errore", "Incontro non trovato.")
            return

        u = self.utente_ctrl.get_utente_attivo()
        if u.id not in self.gruppo_attuale.amministratori:
            QMessageBox.warning(self, "Errore", "Solo gli admin possono modificare.")
            return

        nuovo_titolo, ok = QInputDialog.getText(self, "Modifica titolo", "Titolo:", text=inc.titolo)
        if not ok:
            return

        nuova_descrizione, ok = QInputDialog.getMultiLineText(self, "Descrizione", "Descrizione:", text=inc.descrizione)
        if not ok:
            return

        ok2 = self.incontro_ctrl.modifica_incontro(
            id_incontro=inc.id,
            id_admin=u.id,
            titolo=nuovo_titolo,
            descrizione=nuova_descrizione
        )

        if ok2:
            QMessageBox.information(self, "OK", "Incontro modificato.")
            self.refresh_incontri()
        else:
            QMessageBox.warning(self, "Errore", "Modifica fallita.")

    def annulla_incontro(self):
        item = self.lista_incontri.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona un incontro.")
            return

        inc_id = item.data(Qt.ItemDataRole.UserRole)
        u = self.utente_ctrl.get_utente_attivo()

        ok = self.incontro_ctrl.annulla_incontro(inc_id, u.id)

        if ok:
            QMessageBox.information(self, "OK", "Incontro annullato.")
            self.refresh_incontri()
        else:
            QMessageBox.warning(self, "Errore", "Operazione fallita.")

    def elimina_incontro(self):
        item = self.lista_incontri.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona un incontro.")
            return

        inc_id = item.data(Qt.ItemDataRole.UserRole)

        conferma = QMessageBox.question(self, "Conferma", "Eliminare questo incontro?")
        if conferma != QMessageBox.StandardButton.Yes:
            return

        u = self.utente_ctrl.get_utente_attivo()
        ok = self.incontro_ctrl.elimina_incontro(inc_id, u.id)

        if ok:
            QMessageBox.information(self, "OK", "Incontro eliminato.")
            self.refresh_incontri()
        else:
            QMessageBox.warning(self, "Errore", "Eliminazione fallita.")
