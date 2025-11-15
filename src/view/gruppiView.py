from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem,
    QLineEdit, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt

class GruppiView(QWidget):
    def __init__(self, gruppo_ctrl, utente_ctrl):
        super().__init__()

        self.gruppo_ctrl = gruppo_ctrl
        self.utente_ctrl = utente_ctrl

        layout = QHBoxLayout()
        self.setLayout(layout)

        # LISTA GRUPPI
        left = QVBoxLayout()

        lbl = QLabel("Gruppi disponibili")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold;")
        left.addWidget(lbl)

        # ricerca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca gruppo..")
        self.search_input.textChanged.connect(self.refresh_gruppi)
        left.addWidget(self.search_input)

        # lista gruppi
        self.lista_gruppi = QListWidget()
        self.lista_gruppi.itemClicked.connect(self.mostra_dettagli_gruppo)
        left.addWidget(self.lista_gruppi)

        # bottone crea gruppo
        btn_crea = QPushButton("Crea nuovo gruppo")
        btn_crea.clicked.connect(self.crea_gruppo)
        left.addWidget(btn_crea)

        layout.addLayout(left, 2)

        # DETTAGLI GRUPPO
        right = QVBoxLayout()

        self.lbl_nome = QLabel("Nome gruppo: ")
        self.lbl_descrizione = QLabel("Descrizione: ")
        self.lbl_admin = QLabel("Amministratori: ")
        self.lbl_membri = QLabel("Membri: ")

        for w in [
            self.lbl_nome, self.lbl_descrizione,
            self.lbl_admin, self.lbl_membri
        ]:
            w.setStyleSheet("font-size: 14px;")
            right.addWidget(w)

        self.btn_aggiungi_utente = QPushButton("Aggiungi utente")
        self.btn_rimuovi_utente = QPushButton("Rimuovi utente")
        self.btn_promuovi_admin = QPushButton("Promuovi admin")
        self.btn_modifica = QPushButton("Modifica gruppo")
        self.btn_elimina = QPushButton("Elimina gruppo")

        self.btn_aggiungi_utente.clicked.connect(self.aggiungi_utente)
        self.btn_rimuovi_utente.clicked.connect(self.rimuovi_utente)
        self.btn_promuovi_admin.clicked.connect(self.promuovi_admin)
        self.btn_modifica.clicked.connect(self.modifica_gruppo)
        self.btn_elimina.clicked.connect(self.elimina_gruppo)

        # Contenitore della parte admin
        self.admin_buttons = [
            self.btn_aggiungi_utente,
            self.btn_rimuovi_utente,
            self.btn_promuovi_admin,
            self.btn_modifica,
            self.btn_elimina
        ]

        for btn in self.admin_buttons:
            right.addWidget(btn)

        layout.addLayout(right, 3)

        self.gruppo_selezionato = None

        self.refresh_gruppi()

    # REFRESH LISTA GRUPPI
    def refresh_gruppi(self):
        self.lista_gruppi.clear()
        filtro = self.search_input.text()

        if filtro:
            gruppi = self.gruppo_ctrl.cerca_gruppi(filtro)
        else:
            gruppi = self.gruppo_ctrl.lista_gruppi()

        for g in gruppi:
            item = QListWidgetItem(g.nomeGruppo)
            item.setData(Qt.ItemDataRole.UserRole, g.id)
            self.lista_gruppi.addItem(item)

    # MOSTRA DETTAGLI DI UN GRUPPO
    def mostra_dettagli_gruppo(self, item):
        id_gruppo = item.data(Qt.ItemDataRole.UserRole)
        gruppo = self.gruppo_ctrl.get_gruppo(id_gruppo)
        self.gruppo_selezionato = gruppo

        self.lbl_nome.setText(f"Nome gruppo: {gruppo.nomeGruppo}")
        self.lbl_descrizione.setText(f"Descrizione: {gruppo.descrizione}")
        admin_nomi = []
        for id_admin in gruppo.amministratori:
            ut = self.utente_ctrl.repo_utenti.get_by_id(id_admin)
            if ut:
                admin_nomi.append(f"{ut.nome} {ut.cognome}")
        if admin_nomi:
            self.lbl_admin.setText("Amministratori: " + ", ".join(admin_nomi))
        else:
            self.lbl_admin.setText("Amministratori: nessuno")
        
        membri_nomi = []
        for id_membro in gruppo.listaUtenti:
            ut = self.utente_ctrl.repo_utenti.get_by_id(id_membro)
            if ut:
                membri_nomi.append(f"{ut.nome} {ut.cognome}")
        if membri_nomi:
            self.lbl_membri.setText("Membri: " + ", ".join(membri_nomi))
        else:
            self.lbl_membri.setText("Membri: nessuno")

        self.aggiorna_permessi_admin()

    def aggiorna_permessi_admin(self):
        u = self.utente_ctrl.get_utente_attivo()
        gruppo = self.gruppo_selezionato

        if not gruppo:
            for btn in self.admin_buttons:
                btn.setVisible(False)
            return

        is_admin = u.id in gruppo.amministratori

        for btn in self.admin_buttons:
            btn.setVisible(is_admin)

    # CREA GRUPPO
    def crea_gruppo(self):
        u = self.utente_ctrl.get_utente_attivo()
        if not u:
            QMessageBox.warning(self, "Errore", "effettuare il login.")
            return

        nome, ok = QInputDialog.getText(self, "Nome gruppo", "Inserisci il nome:")
        if not ok or not nome:
            return

        descrizione, ok = QInputDialog.getMultiLineText(self, "Descrizione gruppo", "Descrizione:")
        if not ok:
            return

        self.gruppo_ctrl.crea_gruppo(nome, descrizione, u.id)
        self.refresh_gruppi()

    # ADMIN: AGGIUNGI UTENTE
    def aggiungi_utente(self):
        gruppo = self.gruppo_selezionato
        if not gruppo:
            return

        id_utente, ok = QInputDialog.getText(self, "Aggiungi utente", "utente da aggiungere:")
        if not ok or not id_utente:
            return

        u = self.utente_ctrl.get_utente_attivo()

        if self.gruppo_ctrl.aggiungi_utente(gruppo.id, u.id, id_utente):
            QMessageBox.information(self, "OK", "Utente aggiunto.")
            self.mostra_dettagli_gruppo(self.lista_gruppi.currentItem())
        else:
            QMessageBox.warning(self, "Errore", "Impossibile aggiungere utente.")

    # ADMIN: RIMUOVI UTENTE
    def rimuovi_utente(self):
        gruppo = self.gruppo_selezionato
        if not gruppo:
            return

        id_utente, ok = QInputDialog.getText(self, "Rimuovi utente", "utente da rimuovere:")
        if not ok or not id_utente:
            return

        admin = self.utente_ctrl.get_utente_attivo()

        if self.gruppo_ctrl.rimuovi_utente(gruppo.id, admin.id, id_utente):
            QMessageBox.information(self, "OK", "Utente rimosso.")
            self.mostra_dettagli_gruppo(self.lista_gruppi.currentItem())
        else:
            QMessageBox.warning(self, "Errore", "Operazione fallita.")

    # ADMIN: PROMUOVI ADMIN
    def promuovi_admin(self):
        gruppo = self.gruppo_selezionato
        if not gruppo:
            return

        id_utente, ok = QInputDialog.getText(self, "Promuovi admin", "utente da promuovere:")
        if not ok or not id_utente:
            return

        admin = self.utente_ctrl.get_utente_attivo()

        if self.gruppo_ctrl.nomina_admin(gruppo.id, admin.id, id_utente):
            QMessageBox.information(self, "OK", "Utente promosso admin.")
            self.mostra_dettagli_gruppo(self.lista_gruppi.currentItem())
        else:
            QMessageBox.warning(self, "Errore", "Operazione fallita.")

    # ADMIN: MODIFICA GRUPPO
    def modifica_gruppo(self):
        gruppo = self.gruppo_selezionato
        if not gruppo:
            return

        nuovo_nome, ok = QInputDialog.getText(self, "Modifica nome", "Nuovo nome:", text=gruppo.nomeGruppo)
        if not ok:
            return

        nuova_descrizione, ok = QInputDialog.getMultiLineText(
            self, "Modifica descrizione", "Descrizione:", text=gruppo.descrizione
        )
        if not ok:
            return

        admin = self.utente_ctrl.get_utente_attivo()

        if self.gruppo_ctrl.modifica_gruppo(gruppo.id, admin.id, nomeGruppo=nuovo_nome, descrizione=nuova_descrizione):
            QMessageBox.information(self, "OK", "Gruppo modificato.")
            self.refresh_gruppi()
        else:
            QMessageBox.warning(self, "Errore", "Modifica fallita.")

    # ADMIN: ELIMINA GRUPPO
    def elimina_gruppo(self):
        gruppo = self.gruppo_selezionato
        if not gruppo:
            return

        admin = self.utente_ctrl.get_utente_attivo()

        conferma = QMessageBox.question(self, "Conferma", f"Eliminare il gruppo '{gruppo.nomeGruppo}'?")

        if conferma == QMessageBox.StandardButton.Yes:
            if self.gruppo_ctrl.elimina_gruppo(gruppo.id, admin.id):
                QMessageBox.information(self, "OK", "Gruppo eliminato.")
                self.refresh_gruppi()
            else:
                QMessageBox.warning(self, "Errore", "Eliminazione fallita.")
