from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime
import os


class MaterialiView(QWidget):

    def __init__(self, utente_ctrl, gruppo_ctrl, materiale_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.gruppo_ctrl = gruppo_ctrl
        self.materiale_ctrl = materiale_ctrl

        self.gruppo_attuale = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # HEADER
        self.lbl_titolo = QLabel("Materiali del gruppo")
        self.lbl_titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.lbl_titolo)

        # LISTA MATERIALI
        self.lista_materiali = QListWidget()
        layout.addWidget(self.lista_materiali)

        row = QHBoxLayout()

        btn_carica = QPushButton("Carica materiale")
        btn_carica.clicked.connect(self.carica_materiale)
        row.addWidget(btn_carica)

        btn_scarica = QPushButton("Scarica materiale")
        btn_scarica.clicked.connect(self.scarica_materiale)
        row.addWidget(btn_scarica)

        btn_elimina = QPushButton("Elimina materiale")
        btn_elimina.clicked.connect(self.elimina_materiale)
        row.addWidget(btn_elimina)

        layout.addLayout(row)

    def apri_gruppo(self, id_gruppo):
        gruppo = self.gruppo_ctrl.get_gruppo(id_gruppo)

        if not gruppo:
            QMessageBox.warning(self, "Errore", "Gruppo non trovato.")
            return

        self.gruppo_attuale = gruppo
        self.lbl_titolo.setText(f"Materiali - {gruppo.nomeGruppo}")

        self.refresh_materiali()

    # MOSTRA LISTA MATERIALI
    def refresh_materiali(self):
        if not self.gruppo_attuale:
            return

        self.lista_materiali.clear()

        materiali = self.materiale_ctrl.lista_materiali_gruppo(self.gruppo_attuale.id)

        for m in materiali:
            autore = self.utente_ctrl.repo_utenti.get_by_id(m.autore)
            autore_nome = f"{autore.nome} {autore.cognome}" if autore else "Sconosciuto"

            data_str = m.dataCaricamento.strftime("%d/%m/%Y %H:%M")

            testo = f"{m.titolo} - {m.nome_file} - {autore_nome} ({data_str})"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, m.id)
            self.lista_materiali.addItem(item)

    # CARICA MATERIALE
    def carica_materiale(self):
        if not self.gruppo_attuale:
            return

        utente = self.utente_ctrl.get_utente_attivo()
        if not utente:
            QMessageBox.warning(self, "Errore", "effettuare login.")
            return

        # scegliere file locale
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona file")
        if not file_path:
            return

        titolo = os.path.splitext(os.path.basename(file_path))[0]
        descrizione = ""
        materiale = self.materiale_ctrl.carica_materiale(
            id_gruppo=self.gruppo_attuale.id,
            id_autore=utente.id,
            titolo=titolo,
            descrizione=descrizione,
            percorso_locale=file_path
        )

        if materiale:
            QMessageBox.information(self, "Successo", "Materiale caricato.")
            self.refresh_materiali()
        else:
            QMessageBox.warning(self, "Errore", "Upload fallito.")

    # SCARICA MATERIALE
    def scarica_materiale(self):
        item = self.lista_materiali.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona un materiale.")
            return

        id_materiale = item.data(Qt.ItemDataRole.UserRole)

        # scegliere destinazione
        destinazione = QFileDialog.getExistingDirectory(self, "Scegli cartella di destinazione")
        if not destinazione:
            return

        ok = self.materiale_ctrl.scarica_materiale(id_materiale, destinazione)

        if ok:
            QMessageBox.information(self, "OK", "File scaricato.")
        else:
            QMessageBox.warning(self, "Errore", "Download fallito.")

    # ELIMINA MATERIALE 
    def elimina_materiale(self):
        if not self.gruppo_attuale:
            return

        item = self.lista_materiali.currentItem()
        if not item:
            QMessageBox.warning(self, "Errore", "Seleziona un materiale.")
            return

        utente = self.utente_ctrl.get_utente_attivo()
        if utente.id not in self.gruppo_attuale.amministratori:
            QMessageBox.warning(self, "Errore", "Solo gli admin possono eliminare.")
            return

        id_materiale = item.data(Qt.ItemDataRole.UserRole)

        conferma = QMessageBox.question(self, "Conferma", "Eliminare il materiale?")
        if conferma != QMessageBox.StandardButton.Yes:
            return

        ok = self.materiale_ctrl.elimina_materiale(
            self.gruppo_attuale.id,
            utente.id,
            id_materiale
        )

        if ok:
            QMessageBox.information(self, "OK", "Materiale eliminato.")
            self.refresh_materiali()
        else:
            QMessageBox.warning(self, "Errore", "Eliminazione fallita.")
