from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem,
    QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime


class ChatView(QWidget):

    def __init__(self, utente_ctrl, gruppo_ctrl, messaggio_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.gruppo_ctrl = gruppo_ctrl
        self.messaggio_ctrl = messaggio_ctrl

        self.gruppo_attuale = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.lbl_titolo = QLabel("Chat del Gruppo")
        self.lbl_titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.lbl_titolo)

        self.lista_messaggi = QListWidget()
        layout.addWidget(self.lista_messaggi)

        bottom = QHBoxLayout()

        self.input_messaggio = QLineEdit()
        self.input_messaggio.setPlaceholderText("Scrivi un messaggio...")
        bottom.addWidget(self.input_messaggio)

        btn_invia = QPushButton("Invia")
        btn_invia.clicked.connect(self.invia_messaggio)
        bottom.addWidget(btn_invia)

        layout.addLayout(bottom)

        btn_refresh = QPushButton("Aggiorna Chat")
        btn_refresh.clicked.connect(self.refresh_chat)
        layout.addWidget(btn_refresh)

    def apri_chat(self, id_gruppo):
        gruppo = self.gruppo_ctrl.get_gruppo(id_gruppo)
        if not gruppo:
            QMessageBox.warning(self, "Errore", "Gruppo non trovato.")
            return

        self.gruppo_attuale = gruppo
        self.lbl_titolo.setText(f"Chat: {gruppo.nomeGruppo}")

        self.refresh_chat()

    def refresh_chat(self):
        if not self.gruppo_attuale:
            return

        self.lista_messaggi.clear()

        messaggi = self.messaggio_ctrl.chat_gruppo(self.gruppo_attuale.id)

        for msg in messaggi:
            ut = self.utente_ctrl.repo_utenti.get_by_id(msg.mittente)
            nome = f"{ut.nome} {ut.cognome}" if ut else "Utente sconosciuto"

            data_str = msg.data.strftime("%d/%m/%Y %H:%M")

            testo = f"[{data_str}] {nome}: {msg.testo}"

            item = QListWidgetItem(testo)
            self.lista_messaggi.addItem(item)

    def invia_messaggio(self):
        if not self.gruppo_attuale:
            return

        testo = self.input_messaggio.text().strip()
        if not testo:
            return

        utente = self.utente_ctrl.get_utente_attivo()
        if not utente:
            QMessageBox.warning(self, "Errore", "Devi effettuare il login.")
            return

        # verifica che l’utente sia nel gruppo
        if utente.id not in self.gruppo_attuale.listaUtenti:
            QMessageBox.warning(self, "Errore", "Non fai parte del gruppo.")
            return

        ok = self.messaggio_ctrl.invia_messaggio_gruppo(
            self.gruppo_attuale.id,
            utente.id,
            testo
        )

        if not ok:
            QMessageBox.warning(self, "Errore", "Invio fallito.")
            return

        self.input_messaggio.clear()
        self.refresh_chat()
