from re import S
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(500, 500) #modifie la taille du rectangle

        #Le haut de l'inteface et le positionnement ds l'espace

        self.label1 = QLabel("Enter your Hostname:", self)
        self.label1.move(100, 1)
        self.text1 = QLineEdit(self)
        self.text1.move(100, 20)
        #self.text.setFixedSize(10, 10)

        self.label2 = QLabel("Enter your API key:", self)
        self.label2.move(100, 60)
        self.text2 = QLineEdit(self)
        self.text2.move(100, 100)

        self.label3 = QLabel("Enter your IP:", self)
        self.label3.move(100, 150)
        self.text13 = QLineEdit(self)
        self.text13.move(100, 175)

        self.label2 = QLabel("Answer:", self)
        self.label2.move(100, 220)
        self.button = QPushButton("Send", self)
        self.button.move(100, 250)

        self.button.clicked.connect(self.on_click)  #permet d'allez a la page après des coordonnées juste
        self.button.pressed.connect(self.on_click)  #permet d'avoir le message d'erreur si les coordonnées sont faussses

        self.show() #permet d'afficher la fenetre

    def on_click(self):
        hostname = self.text1.text()
        api_key = self.text2.text()
        ip = self.text13.text()

        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname,ip, api_key)
            if res:
                self.label2.setText("\n Longitude: %s \n Latitude: %s \n" % (res["Longitude"], res["Latitude"]))
                self.label2.adjustSize()
                self.show()
                url1 = "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["Latitude"], res["Longitude"])
                webbrowser.open_new_tab(url1)

    def __query(self, hostname, ip, api_key):
        url = "http://%s/ip/%s?key=%s" % (hostname,ip, api_key)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()

    #Fin du tp !