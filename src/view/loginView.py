from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class LoginView(QWidget):

    def __init__(self, utente_ctrl, on_login_success, on_open_register):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.on_login_success = on_login_success
        self.on_open_register = on_open_register

        self.setWindowTitle("Login - Piattaforma di Gruppi Studio")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # titolo
        titolo = QLabel("Accedi")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titolo)

        # email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login)

        # Register button
        btn_register = QPushButton("Registrati")
        btn_register.clicked.connect(self.open_register)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        utente = self.utente_ctrl.login(email, password)

        if not utente:
            QMessageBox.warning(self, "Errore!!", "Credenziali non valide o utente sospeso.")
            return

        self.on_login_success(utente)

    def open_register(self):
        self.on_open_register()
