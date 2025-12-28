from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

from model.utente import RolePlatform


class SegnalazioniView(QWidget):

    def __init__(self, utente_ctrl, segnalazione_ctrl, gruppo_ctrl, messaggio_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.segnalazione_ctrl = segnalazione_ctrl
        self.gruppo_ctrl = gruppo_ctrl
        self.messaggio_ctrl = messaggio_ctrl

        layout = QVBoxLayout()
        self.setLayout(layout)

        titolo = QLabel("Gestione Segnalazioni")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titolo)

        user_row = QHBoxLayout()

        btn_segnala_utente = QPushButton("Segnala utente")
        btn_segnala_utente.clicked.connect(self.segnala_utente)
        user_row.addWidget(btn_segnala_utente)

        btn_segnala_messaggio = QPushButton("Segnala messaggio")
        btn_segnala_messaggio.clicked.connect(self.segnala_messaggio)
        user_row.addWidget(btn_segnala_messaggio)

        layout.addLayout(user_row)

        layout.addSpacing(10)


        lbl1 = QLabel("Segnalazioni in attesa")
        lbl1.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(lbl1)

        self.lista_attesa = QListWidget()
        layout.addWidget(self.lista_attesa)

        lbl2 = QLabel("Segnalazioni valutate")
        lbl2.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(lbl2)

        self.lista_valutate = QListWidget()
        layout.addWidget(self.lista_valutate)

        lbl3 = QLabel("Segnalazioni archiviate")
        lbl3.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(lbl3)

        self.lista_archiviate = QListWidget()
        layout.addWidget(self.lista_archiviate)

        #admin
        admin_row = QHBoxLayout()

        btn_valuta = QPushButton("Valuta segnalazione")
        btn_valuta.clicked.connect(self.valuta_segnalazione)
        admin_row.addWidget(btn_valuta)

        btn_archivia = QPushButton("Archivia segnalazione")
        btn_archivia.clicked.connect(self.archivia_segnalazione)
        admin_row.addWidget(btn_archivia)

        btn_sanziona = QPushButton("Applica sanzione")
        btn_sanziona.clicked.connect(self.applica_sanzione)
        admin_row.addWidget(btn_sanziona)

        layout.addLayout(admin_row)

        self.refresh()

    def refresh(self):
        self.lista_attesa.clear()
        self.lista_valutate.clear()
        self.lista_archiviate.clear()

        # SEGNALAZIONI IN ATTESA
        for s in self.segnalazione_ctrl.segnalazioni_in_attesa():
            item = QListWidgetItem(self.format_segnalazione(s))
            item.setData(Qt.ItemDataRole.UserRole, s.id)
            self.lista_attesa.addItem(item)

        # SEGNALAZIONI VALUTATE
        for s in self.segnalazione_ctrl.segnalazioni_valutate():
            item = QListWidgetItem(self.format_segnalazione(s))
            item.setData(Qt.ItemDataRole.UserRole, s.id)
            self.lista_valutate.addItem(item)

        # SEGNALAZIONI ARCHIVIATE
        for s in self.segnalazione_ctrl.segnalazioni_archiviate():
            item = QListWidgetItem(self.format_segnalazione(s))
            item.setData(Qt.ItemDataRole.UserRole, s.id)
            self.lista_archiviate.addItem(item)

    def format_segnalazione(self, s):
        autore = self.utente_ctrl.repo_utenti.get_by_id(s.autore)
        autore_txt = f"{autore.nome} {autore.cognome}" if autore else "Sconosciuto"

        ut_target = self.utente_ctrl.repo_utenti.get_by_id(s.destinatario)
        if ut_target:
            target_txt = f"segnalato: {ut_target.nome} {ut_target.cognome} ({ut_target.email})"
        else:
            target_txt = f"messaggio segnalato: {s.destinatario}"

        data = s.data.strftime("%d/%m/%Y %H:%M")

        return f"{data} | Autore: {autore_txt} | {target_txt} | Motivo: {s.motivo}"

    def segnala_utente(self):
        u = self.utente_ctrl.get_utente_attivo()
        if not u:
            QMessageBox.warning(self, "Errore", "effettuare login.")
            return

        email_utente, ok = QInputDialog.getText(self, "Segnala utente", "email utente da segnalare:")
        if not ok or not email_utente:
            return

        motivo, ok = QInputDialog.getMultiLineText(self, "Motivo", "Descrivi il motivo:")
        if not ok:
            return

        s = self.segnalazione_ctrl.segnala_utente(u.id, email_utente, motivo)

        if s:
            QMessageBox.information(self, "OK", "Segnalazione inviata.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile inviare la segnalazione.")

    # SEGNALA MESSAGGIO
    def segnala_messaggio(self):
        u = self.utente_ctrl.get_utente_attivo()
        if not u:
            QMessageBox.warning(self, "Errore", "effettuare login.")
            return

        id_msg, ok = QInputDialog.getText(self, "Segnala messaggio", "messaggio:")
        if not ok or not id_msg:
            return

        motivo, ok = QInputDialog.getMultiLineText(self, "Motivo", "Descrivi il motivo:")
        if not ok:
            return

        s = self.segnalazione_ctrl.segnala_messaggio(u.id, id_msg, motivo)

        if s:
            QMessageBox.information(self, "OK", "Segnalazione inviata.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Errore", "Errore nell'invio.")

    def _seleziona_segnalazione_da_lista(self, lista):
        item = lista.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona una segnalazione.")
            return None
        return item.data(Qt.ItemDataRole.UserRole)


    def valuta_segnalazione(self):
        admin = self.utente_ctrl.get_utente_attivo()

        if not admin or admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            QMessageBox.warning(self, "Errore", "Solo l'amministratore di piattaforma può valutare.")
            return

        id_seg = self._seleziona_segnalazione_da_lista(self.lista_attesa)
        if not id_seg:
            return

        ok = self.segnalazione_ctrl.valuta_segnalazione(admin.id, id_seg)

        if ok:
            QMessageBox.information(self, "OK", "Segnalazione valutata.")
        else:
            QMessageBox.warning(self, "Errore", "Impossibile valutare.")

        self.refresh()

    def archivia_segnalazione(self):
        admin = self.utente_ctrl.get_utente_attivo()

        if not admin or admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            QMessageBox.warning(self, "Errore", "Operazione non autorizzata.")
            return

        id_seg = self._seleziona_segnalazione_da_lista(self.lista_valutate)
        if not id_seg:
            return

        ok = self.segnalazione_ctrl.archivia_segnalazione(admin.id, id_seg)

        if ok:
            QMessageBox.information(self, "OK", "Segnalazione archiviata.")
        else:
            QMessageBox.warning(self, "Errore", "Impossibile archiviare.")

        self.refresh()


    def applica_sanzione(self):
        admin = self.utente_ctrl.get_utente_attivo()

        if not admin or admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            QMessageBox.warning(self, "Errore", "Solo l'amministratore può applicare sanzioni.")
            return

        id_seg = self._seleziona_segnalazione_da_lista(self.lista_valutate)
        if not id_seg:
            return

        tipo, ok = QInputDialog.getText(self, "Sanzione", "Tipo sanzione:")
        if not ok or not tipo:
            return

        note, ok = QInputDialog.getMultiLineText(self, "Note", "Note sanzione:")
        if not ok:
            return

        ok2 = self.segnalazione_ctrl.applica_sanzione(admin.id, id_seg, tipo, note)

        if ok2:
            QMessageBox.information(self, "OK", "Sanzione applicata.")
        else:
            QMessageBox.warning(self, "Errore", "Applicazione sanzione fallita.")

        self.refresh()
