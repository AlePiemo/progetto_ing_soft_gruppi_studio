from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QDateEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from datetime import date


class CalendarioView(QWidget):

    def __init__(self, utente_ctrl, calendario_ctrl, gruppo_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.calendario_ctrl = calendario_ctrl
        self.gruppo_ctrl = gruppo_ctrl

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        titolo = QLabel("Calendario incontri")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titolo)

        # SEZIONE PROSSIMI INCONTRI
        lbl_prossimi = QLabel("Prossimi incontri")
        lbl_prossimi.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(lbl_prossimi)

        self.lista_prossimi = QListWidget()
        layout.addWidget(self.lista_prossimi)

        # SEZIONE FILTRO PER DATA
        filtro_layout = QHBoxLayout()

        lbl_data = QLabel("Incontri in data:")
        filtro_layout.addWidget(lbl_data)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        filtro_layout.addWidget(self.date_edit)

        btn_filtra = QPushButton("Filtra")
        btn_filtra.clicked.connect(self.filtra_per_data)
        filtro_layout.addWidget(btn_filtra)

        layout.addLayout(filtro_layout)

        self.lista_data = QListWidget()
        layout.addWidget(self.lista_data)

        # SEZIONE TUTTI GLI INCONTRI
        lbl_tutti = QLabel("Tutti gli incontri a cui partecipo")
        lbl_tutti.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(lbl_tutti)

        self.lista_tutti = QListWidget()
        layout.addWidget(self.lista_tutti)

        btn_refresh = QPushButton("Aggiorna calendario")
        btn_refresh.clicked.connect(self.refresh_tutto)
        layout.addWidget(btn_refresh)

    # REFRESH COMPLETO DEL CALENDARIO
    def refresh_tutto(self):
        utente = self.utente_ctrl.get_utente_attivo()
        if not utente:
            QMessageBox.warning(self, "Errore", "Devi effettuare il login.")
            return

        self._carica_prossimi_incontri(utente.id)
        self._carica_tutti_incontri(utente.id)
        self.filtra_per_data()  # usa la data attuale nel date_edit

    # CARICA PROSSIMI INCONTRI
    def _carica_prossimi_incontri(self, id_utente: str):
        self.lista_prossimi.clear()

        incontri = self.calendario_ctrl.incontri_futuri_utente(id_utente)

        for inc in incontri:
            gruppo = self.gruppo_ctrl.get_gruppo(inc.gruppo_id)
            nome_gruppo = gruppo.nomeGruppo if gruppo else "Gruppo sconosciuto"

            data_str = inc.dataIncontro.strftime("%d/%m/%Y")
            ora_str = inc.oraIncontro.strftime("%H:%M")
            stato = inc.statoIncontro.value

            testo = f"{data_str} {ora_str} | {inc.titolo} | {nome_gruppo} | {stato}"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, inc.id)
            self.lista_prossimi.addItem(item)

    # CARICA TUTTI GLI INCONTRI DELL'UTENTE
    def _carica_tutti_incontri(self, id_utente: str):
        self.lista_tutti.clear()

        incontri = self.calendario_ctrl.calendario_utente(id_utente)

        for inc in incontri:
            gruppo = self.gruppo_ctrl.get_gruppo(inc.gruppo_id)
            nome_gruppo = gruppo.nomeGruppo if gruppo else "Gruppo sconosciuto"

            data_str = inc.dataIncontro.strftime("%d/%m/%Y")
            ora_str = inc.oraIncontro.strftime("%H:%M")
            stato = inc.statoIncontro.value

            testo = f"{data_str} {ora_str} | {inc.titolo} | {nome_gruppo} | {stato}"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, inc.id)
            self.lista_tutti.addItem(item)
            
    # FILTRA INCONTRI PER UNA DATA
    def filtra_per_data(self):
        utente = self.utente_ctrl.get_utente_attivo()
        if not utente:
            return

        self.lista_data.clear()

        qd: QDate = self.date_edit.date()
        giorno: date = qd.toPyDate()

        incontri = self.calendario_ctrl.incontri_per_data(utente.id, giorno)

        for inc in incontri:
            gruppo = self.gruppo_ctrl.get_gruppo(inc.gruppo_id)
            nome_gruppo = gruppo.nomeGruppo if gruppo else "Gruppo sconosciuto"

            ora_str = inc.oraIncontro.strftime("%H:%M")
            stato = inc.statoIncontro.value

            testo = f"{ora_str} | {inc.titolo} | {nome_gruppo} | {stato}"

            item = QListWidgetItem(testo)
            item.setData(Qt.ItemDataRole.UserRole, inc.id)
            self.lista_data.addItem(item)
