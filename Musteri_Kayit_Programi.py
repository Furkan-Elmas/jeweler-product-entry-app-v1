import datetime
import locale
import sys
import sqlite3
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from MusteriGuncelDurumEkrani import Ui_musteriGuncelDurum
from AtolyeGuncelDurumEkrani import  Ui_atolyeGuncelDurum
from MusteriSatis_Odeme_Iade import Ui_musteriSatisOdemeIade
from AtolyeSatinalma_Odeme_Iade import Ui_AtolyeSatinalmaOdemeIade
from musteriEkleSil import Ui_Form_MusteriEkleSil
from atolyeEkleSil import  Ui_atolyeEkleSil
from atolyeEkrani import Ui_Form_AtolyeEkrani
from musteriEkrani import Ui_Form_MusteriEkrani
from girisEkrani import Ui_MainWindow_GirisEkrani

locale.setlocale(locale.LC_ALL, '')


class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow_GirisEkrani()
        self.ui.setupUi(self)

        self.musteriPenceresi = MusteriIslemEkrani()
        self.ui.ileriButonu.clicked.connect(self.musteriGoruntule)

        self.atolyePenceresi = AtolyeIslemEkrani()
        self.ui.ileriButonu.clicked.connect(self.atolyeleriGoruntule)

        self.ui.listWidget.setCurrentRow(0)

        self.show()


    def musteriGoruntule(self):
        index = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(index)
        if item.text() == "Müşteriler":
            self.musteriPenceresi.show()


    def atolyeleriGoruntule(self):
        index = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(index)
        if item.text() == "Atölyeler":
            self.atolyePenceresi.show()


class AtolyeIslemEkrani(QWidget):
    def __init__(self):
        super(AtolyeIslemEkrani, self).__init__()

        self.ui = Ui_Form_AtolyeEkrani()
        self.ui.setupUi(self)

        self.atolyeEkleSil = AtolyeEkleSilEkrani()
        self.ui.btnEkleSil.clicked.connect(self.atolyeEkleSilEkraniCalistir)

        self.atolyesatinalmaodemeiade = AtolyeSatinalmaOdemeEkrani()
        self.ui.btnSatinAl.clicked.connect(self.atolyeSatinalmaEkraniCalistir)

        self.atolyeGenelDurumEkrani = AtolyeGenelDurumEkrani()
        self.ui.btnGuncelDurum.clicked.connect(self.atolyeGenelDurumEkraniCalistir)

    def atolyeEkleSilEkraniCalistir(self):
        self.atolyeEkleSil.show()

    def atolyeSatinalmaEkraniCalistir(self):
        self.atolyesatinalmaodemeiade.showMaximized()

    def atolyeGenelDurumEkraniCalistir(self):
        self.atolyeGenelDurumEkrani.show()


class AtolyeGenelDurumEkrani(QWidget):
    def __init__(self):
        super(AtolyeGenelDurumEkrani, self).__init__()

        self.ui = Ui_atolyeGuncelDurum()
        self.ui.setupUi(self)

        #####  MÜŞTERİ İSİMLERİ ÇAĞIRILIYOR  #####
        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumAtolyeler")
            self.atolyeler = self.cursor.fetchall()

            self.bosliste = []
            for i in self.atolyeler:
                self.bosliste += i

        #####  MÜŞTERİLERİ GÖSTERME VE FİLTRELEME  ####
        self.model = QStandardItemModel(len(self.atolyeler), 1)
        self.model.setHorizontalHeaderLabels(['Atölyeler'])


        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        self.filterProxyModel = QSortFilterProxyModel()
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_Arama.textChanged.connect(self.filterProxyModel.setFilterRegExp)
        self.ui.tableView_Atolyeler.setModel(self.filterProxyModel)
        self.ui.tableView_Atolyeler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.table_alisverisozet = QStandardItemModel()
        self.ui.table_alisverisozet1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.lineEdit.setPlaceholderText("Ara")
        self.ui.lineEdit_Arama.setPlaceholderText("Ara")

        self.ui.tableView_Atolyeler.clicked.connect(self.atolyeSec)
        self.ui.tableView_Atolyeler.clicked.connect(self.bilgileriGoster)
        self.ui.tableView_Atolyeler.clicked.connect(self.modelBelirle)
        self.ui.tableView_Atolyeler.clicked.connect(self.istatistik)
        self.ui.comboBox.currentTextChanged.connect(self.istatistik)


        self.ui.radioButton_3.click()
        self.siralamaBelirle()
        self.ui.radioButton_3.clicked.connect(self.siralamaBelirle)
        self.ui.radioButton_2.clicked.connect(self.siralamaBelirle)
        self.ui.radioButton.clicked.connect(self.siralamaBelirle)

        self.ui.comboBox.hide()
        self.ui.label_2.hide()


    def istatistik(self):

        self.ui.comboBox.show()
        self.ui.label_2.show()

        if not self.ui.verticalLayout_4.isEmpty():
            self.ui.verticalLayout_4.removeWidget(self.chartView)

        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT tarih,satinalinannethas,odemenethas FROM '{self.secilenAtolye}'")
            liste = cursor.fetchall()


        ocakS,ocakO = 0,0
        subatS,subatO = 0,0
        martS,martO = 0,0
        nisanS,nisanO = 0,0
        mayisS,mayisO = 0,0
        haziranS,haziranO = 0,0
        temmuzS,temmuzO = 0,0
        agustosS,agustosO = 0,0
        eylulS,eylulO = 0,0
        ekimS,ekimO = 0,0
        kasimS,kasimO = 0,0
        aralikS,aralikO = 0,0

        for i,j,k in liste:

            i = i.split(".")
            i[0] =int(i[0])
            i[1] =int(i[1])
            i[2] =int(i[2])

            bugun = datetime.date.today()
            bugununYili = datetime.date.strftime(bugun,'%Y')
            tarih = bugun.replace(i[0],i[1],i[2])
            ay = datetime.date.strftime(tarih,'%B')
            yil = datetime.date.strftime(tarih,'%Y')

            if j == None:
                j=0
            if k == None:
                k=0

            if self.ui.comboBox.currentText() == yil:
                if ay == "Ocak":
                    ocakS += j
                    ocakO +=k
                if ay == "Şubat":
                    subatS += j
                    subatO+=k
                if ay == "Mart":
                    martS += j
                    martO += k
                if ay == "Nisan":
                    nisanS += j
                    nisanO+=k
                if ay == "Mayıs":
                    mayisS += j
                    mayisO+=k
                if ay == "Haziran":
                    haziranS += j
                    haziranO+=k
                if ay == "Temmuz":
                    temmuzS += j
                    temmuzO+=k
                if ay == "Ağustos":
                    agustosS += j
                    agustosO+=k
                if ay == "Eylül":
                    eylulS += j
                    eylulO+=k
                if ay == "Ekim":
                    ekimS += j
                    ekimO+=k
                if ay == "Kasım":
                    kasimS += j
                    kasimO+=k
                if ay == "Aralık":
                    aralikS += j
                    aralikO+=k

        aylar = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım",
        "Aralık"]

        set1 = QBarSet("Toplam Satın Alma (Has Cinsinden Gram)")
        set2 = QBarSet("Toplam Ödeme (Has Cinsinden Gram)")
        set3 = QBarSet("Net Kar (Has Cinsinden Gram)")

        set1.append([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])
        set2.append([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])
        set3.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        series = QBarSeries()
        series.append(set1)
        series.append(set2)
        series.append(set3)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Yıllık Alışveriş Çizelgesi")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(aylar)

        axisY = QValueAxis()


        if max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>700 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>700:
            axisY.setRange(0, 800)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>600 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>600:
            axisY.setRange(0, 700)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>500 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>500:
            axisY.setRange(0, 600)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>400 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>400:
            axisY.setRange(0, 500)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>300 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>300:
            axisY.setRange(0, 400)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>200 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>200:
            axisY.setRange(0,300)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>100 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>100:
            axisY.setRange(0, 200)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>50 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>50:
            axisY.setRange(0, 100)
        else:
            axisY.setRange(0, 50)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        series.attachAxis(axisY)
        series.attachAxis(axisX)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.ui.verticalLayout_4.addWidget(self.chartView)

    def atolyeSec(self):

        self.secilenAtolye = self.ui.tableView_Atolyeler.currentIndex().model().itemData(self.ui.tableView_Atolyeler.currentIndex()).get(0)

        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT satinalinannethas FROM '{self.secilenAtolye}'")
            self.satilanToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT odemenethas FROM '{self.secilenAtolye}'")
            self.odemeToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT iadenethas FROM '{self.secilenAtolye}'")
            self.iadeToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT iadeodemenethas FROM '{self.secilenAtolye}'")
            self.iadeOdemeToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT sondurum FROM TumAtolyeler WHERE adi='{self.secilenAtolye}'")
            self.sonDurumLine = cursor.fetchall()
            cursor.execute(f"SELECT rowid,tarih,islemturu FROM '{self.secilenAtolye}'")
            self.tarihveislem = cursor.fetchall()


            ###### ALIŞVERİŞ ÇİZELGESİ İÇİN TARİHLER BELİRLENİYOR

            cursor.execute(f"SELECT tarih FROM '{self.secilenAtolye}'")
            self.tarih = cursor.fetchall()
            self.yilListesi = []
            for i in self.tarih:
                ss = i[0].split(".")
                ss[0] = int(ss[0])
                ss[1] = int(ss[1])
                ss[2] = int(ss[2])

                bugun = datetime.date.today()
                bugununYili = datetime.date.strftime(bugun, '%Y')
                tarih = bugun.replace(ss[0], ss[1], ss[2])
                ay = datetime.date.strftime(tarih, '%B')
                self.yil = datetime.date.strftime(tarih, '%Y')
                if not self.yilListesi.__contains__(self.yil):
                    self.yilListesi.append(self.yil)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.yilListesi)

        self.sontarih = "0"
        self.sonislem = ""
        self.sayacs = 1
        self.sayaso = 1
        self.sayaci = 1
        self.sayacio = 1

        for k,i,j in self.tarihveislem:
            if i > self.sontarih:
                if j == "Tartı satın alma" or j == "Adet satın alma":
                    self.sontarihsatis = i
                    self.sonislemsatis = j
                    self.sayacs += 1
                if j == "Tartı ödeme" or j == "Adet ödeme" or j =="Nakit ödeme":
                    self.sontarihodeme = i
                    self.sonislemodeme = j
                if j == "Tartı iade" or j == "Adet iade":
                    self.sontarihiade = i
                    self.sonislemiade = j
                if j == "Tartı iade ödeme" or j == "Adet iade ödeme" or j == "Nakit iade ödeme":
                    self.sontarihiadeodeme = i
                    self.sonislemiadeodeme = j


    def bilgileriGoster(self):

        self.ui.label_bakiye.setText(str(self.sonDurumLine[0][0])+" Gram")
        try:
            self.sontarihsatis = self.sontarihsatis.split(".")
            self.ui.label_sonsatis.setText(".".join([i for i in self.sontarihsatis[::-1]]))
            self.sontarihsatis = "-"
        except:
            pass
        try:
            self.sontarihodeme = self.sontarihodeme.split(".")
            self.ui.label_sonodeme.setText(".".join([i for i in self.sontarihodeme[::-1]]))
            self.sontarihodeme = "-"
        except:
            pass
        try:
            self.sontarihiade = self.sontarihiade.split(".")
            self.ui.label_soniade.setText(".".join([i for i in self.sontarihiade[::-1]]))
            self.sontarihiade = "-"
        except:
            pass
        try:
            self.sontarihiadeodeme = self.sontarihiadeodeme.split(".")
            self.ui.label_soniadeodeme.setText(".".join([i for i in self.sontarihiadeodeme[::-1]]))
            self.sontarihiadeodeme = "-"
        except:
            pass

        self.ui.table_alisverisozet = QStandardItemModel()
        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            self.ui.table_alisverisozet.clear()
            sayac = 1
            sayacrow = 0
            self.ui.table_alisverisozet.setColumnCount(6)
            for r,i,j in self.tarihveislem[::-1]:
                self.ui.table_alisverisozet.setRowCount(sayac)
                cursor.execute(f"SELECT * FROM '{self.secilenAtolye}' WHERE rowid='{r}'")
                liste = cursor.fetchall()
                yeniliste = []
                for k in liste[0]:
                    if k != None:
                        yeniliste.append(f"{k}")

                yeniliste[0] = yeniliste[0].split(".")

                tarih = datetime.date.today()
                tarih = tarih.replace(int(yeniliste[0][0]), int(yeniliste[0][1]), int(yeniliste[0][2]))
                gün = datetime.date.strftime(tarih, '%A')

                self.ui.table_alisverisozet.setItem(sayacrow, 0, QStandardItem(".".join([i for i in yeniliste[0][::-1]])+"   "+gün))
                self.ui.table_alisverisozet.setItem(sayacrow, 1, QStandardItem(yeniliste[1]))
                self.ui.table_alisverisozet.setItem(sayacrow, 2, QStandardItem(yeniliste[2]))
                if yeniliste[1].__contains__("Tartı"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 3, QStandardItem(yeniliste[3]+"   Gram"))
                if yeniliste[1].__contains__("Adet"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 3, QStandardItem(yeniliste[3]+"   Has"))
                if yeniliste[1].__contains__("Nakit"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 3, QStandardItem(yeniliste[3]+"   TL"))
                if yeniliste[1].__contains__("Tartı"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 4, QStandardItem(yeniliste[4]+"   Milyem"))
                if yeniliste[1].__contains__("Adet"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 4, QStandardItem(yeniliste[4]+"   Adet"))
                if yeniliste[1].__contains__("Nakit"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 4, QStandardItem(yeniliste[4]+"   TL"))
                self.ui.table_alisverisozet.setItem(sayacrow, 5, QStandardItem(yeniliste[5]+"   Gram"))

                sayac+=1
                sayacrow+=1
                if sayac == 365:
                    break

        self.ui.table_alisverisozet.setHorizontalHeaderLabels(["Tarih", "İşlem", "Ürün", "Gram/Has/Nakit", "Milyem/Adet/Has Fiyatı", "Net Has"])
        font = QFont()
        font.setBold(True)
        font.setPointSize(9)
        for i in range(6):
            self.ui.table_alisverisozet.horizontalHeaderItem(i).setFont(font)


    def modelBelirle(self):

        filterProxyModel2 = QSortFilterProxyModel()
        filterProxyModel2.setSourceModel(self.ui.table_alisverisozet)
        filterProxyModel2.setFilterCaseSensitivity(Qt.CaseInsensitive)
        if self.secilenSiralama == "Tarihe Göre":
            filterProxyModel2.setFilterKeyColumn(0)
        if self.secilenSiralama == "İşleme Göre":
            filterProxyModel2.setFilterKeyColumn(1)
        if self.secilenSiralama == "Ürüne Göre":
            filterProxyModel2.setFilterKeyColumn(2)
        self.ui.lineEdit.textChanged.connect(filterProxyModel2.setFilterRegExp)
        self.ui.table_alisverisozet1.setModel(filterProxyModel2)

    def siralamaBelirle(self):
        if self.ui.radioButton_3.isChecked():
            self.secilenSiralama = "Tarihe Göre"

        if self.ui.radioButton_2.isChecked():
            self.secilenSiralama = "İşleme Göre"

        if self.ui.radioButton.isChecked():
            self.secilenSiralama = "Ürüne Göre"

        self.modelBelirle()


class AtolyeEkleSilEkrani(QWidget):
    def __init__(self):
        super(AtolyeEkleSilEkrani, self).__init__()

        self.ui = Ui_atolyeEkleSil()
        self.ui.setupUi(self)

        self.ui.kaydetButonu.clicked.connect(self.addText)

        self.ui.atolyeListesi.clicked.connect(self.findItem)

        self.ui.silButonu.clicked.connect(self.deleteText)

        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumAtolyeler")
            self.atolyeler = self.cursor.fetchall()

        self.model = QStandardItemModel(len(self.atolyeler), 1)
        self.model.setHorizontalHeaderLabels(['Atölyeler'])

        self.bosliste = []
        for i in self.atolyeler:
            self.bosliste += i

        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)

        self.ui.arama.textChanged.connect(filterProxyModel.setFilterRegExp)

        self.ui.atolyeListesi.setModel(filterProxyModel)

        self.ui.atolyeListesi.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.arama.setPlaceholderText("Ara")

        self.items = []
        for i in range(len(self.atolyeler)):
            self.items.append(self.model.item(i).text())


    def addText(self):
        text = self.ui.atolyeAdi.toPlainText().lower().capitalize()
        text2 = QStandardItem(text)
        for j in self.items:
            if j == text:
                QMessageBox.warning(self, "Hata", "Bu isimle bir atölye kayıtlı!")
                return
        if text == "":
            QMessageBox.warning(self, "Hata", "Herhangi bir isim girmediniz!")
            return
        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS '{text}'(tarih TEXT,islemturu TEXT,satinalinanurun TEXT,satinalinanurungram NUMERIC,satinalinanurunmilyem NUMERIC,satinalinanurunhas NUMERIC,satinalinanurunadet NUMERIC,satinalinannethas NUMERIC,odemeurunu TEXT,odemeurungram NUMERIC,odemeurunmilyem NUMERIC,odemeurunhas NUMERIC,odemeurunadet NUMERIC,odemenakitmiktari NUMERIC,odemenakithasfiyati NUMERIC,odemenethas NUMERIC,iadeurunu TEXT,iadeurunugram NUMERIC,iadeurunumilyem NUMERIC,iadeurunhas NUMERIC,iadeurunadet NUMERIC,iadenethas NUMERIC,iadeodemeurunu TEXT,iadeodemeurungram NUMERIC,iadeodemeurunmilyem NUMERIC,iadeodemeurunhas NUMERIC,iadeodemeurunadet NUMERIC,iadeodemenakitmiktari NUMERIC,iadeodemenakithasfiyati NUMERIC,iadeodemenethas NUMERIC)")
            cursor.execute("INSERT INTO TumAtolyeler VALUES ('{}',{})".format(text,00.00))
            connect.commit()
        self.model.appendRow(text2)
        QMessageBox.information(self, "Kayıt Başarılı", "Atölye eklendi.")
        self.items.append(text)
        self.ui.atolyeAdi.clear()
        return

    def findItem(self):
        self.row = self.ui.atolyeListesi.currentIndex().row()
        item = self.model.item(self.row)
        self.text = item.text()
        return

    def deleteText(self):
        try:
            q = QMessageBox.question(self, "Emin misiniz?", "{} isimli atölye silinecek.".format(self.text))
            if q == QMessageBox.Yes:
                with sqlite3.connect("atolyeler.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("DELETE FROM TumAtolyeler WHERE adi = '{}' ".format(self.text))
                    cursor.execute(f"DROP TABLE '{self.text}'")
                    connect.commit()
                self.model.takeRow(self.row)
                self.items.remove(self.text)
                return
        except:
            return


class MusteriIslemEkrani(QWidget):
    def __init__(self):
        super(MusteriIslemEkrani, self).__init__()

        self.ui = Ui_Form_MusteriEkrani()
        self.ui.setupUi(self)

        self.musteriEkleSil = MusteriEkleSilEkrani()
        self.ui.btnEkleSil.clicked.connect(self.musteriEkleSilEkraniCalistir)

        self.musteriSatisOdemeiade = MusteriSatisOdemeIadeEkrani()
        self.ui.btnSatis.clicked.connect(self.musteriSatisOdemeIadeCalistir)

        self.musteriGenelDurumEkrani = MusteriGenelDurumEkrani()
        self.ui.btnGuncelDurum.clicked.connect(self.musteriGenelDurumEkraniCalistir)


    def musteriEkleSilEkraniCalistir(self):
        self.musteriEkleSil.show()

    def musteriSatisOdemeIadeCalistir(self):
        self.musteriSatisOdemeiade.showMaximized()

    def musteriGenelDurumEkraniCalistir(self):
        self.musteriGenelDurumEkrani.show()


class MusteriGenelDurumEkrani(QWidget):
    def __init__(self):
        super(MusteriGenelDurumEkrani, self).__init__()

        self.ui = Ui_musteriGuncelDurum()
        self.ui.setupUi(self)

        #####  MÜŞTERİ İSİMLERİ ÇAĞIRILIYOR  #####
        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumMusteriler")
            self.musteriler = self.cursor.fetchall()

            self.bosliste = []
            for i in self.musteriler:
                self.bosliste += i

        #####  MÜŞTERİLERİ GÖSTERME VE FİLTRELEME  ####
        self.model = QStandardItemModel(len(self.musteriler), 1)
        self.model.setHorizontalHeaderLabels(['Müşteriler'])


        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        self.filterProxyModel = QSortFilterProxyModel()
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_Arama.textChanged.connect(self.filterProxyModel.setFilterRegExp)
        self.ui.tableView_Musteriler.setModel(self.filterProxyModel)
        self.ui.tableView_Musteriler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.table_alisverisozet = QStandardItemModel()
        self.ui.table_alisverisozet1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.lineEdit.setPlaceholderText("Ara")
        self.ui.lineEdit_Arama.setPlaceholderText("Ara")

        self.ui.tableView_Musteriler.clicked.connect(self.musteriSec)
        self.ui.tableView_Musteriler.clicked.connect(self.bilgileriGoster)
        self.ui.tableView_Musteriler.clicked.connect(self.modelBelirle)
        self.ui.tableView_Musteriler.clicked.connect(self.istatistik)
        self.ui.comboBox.currentTextChanged.connect(self.istatistik)


        self.ui.radioButton_3.click()
        self.siralamaBelirle()
        self.ui.radioButton_3.clicked.connect(self.siralamaBelirle)
        self.ui.radioButton_2.clicked.connect(self.siralamaBelirle)
        self.ui.radioButton.clicked.connect(self.siralamaBelirle)

        self.ui.comboBox.hide()
        self.ui.label_2.hide()


    def istatistik(self):

        self.ui.comboBox.show()
        self.ui.label_2.show()

        if not self.ui.verticalLayout_4.isEmpty():
            self.ui.verticalLayout_4.removeWidget(self.chartView)

        with sqlite3.connect("musteriler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT tarih,satilannethas,odemenethas FROM '{self.secilenMusteri}'")
            liste = cursor.fetchall()


        ocakS,ocakO = 0,0
        subatS,subatO = 0,0
        martS,martO = 0,0
        nisanS,nisanO = 0,0
        mayisS,mayisO = 0,0
        haziranS,haziranO = 0,0
        temmuzS,temmuzO = 0,0
        agustosS,agustosO = 0,0
        eylulS,eylulO = 0,0
        ekimS,ekimO = 0,0
        kasimS,kasimO = 0,0
        aralikS,aralikO = 0,0

        for i,j,k in liste:

            i = i.split(".")
            i[0] =int(i[0])
            i[1] =int(i[1])
            i[2] =int(i[2])

            bugun = datetime.date.today()
            bugununYili = datetime.date.strftime(bugun,'%Y')
            tarih = bugun.replace(i[0],i[1],i[2])
            ay = datetime.date.strftime(tarih,'%B')
            yil = datetime.date.strftime(tarih,'%Y')

            if j == None:
                j=0
            if k == None:
                k=0


            if self.ui.comboBox.currentText() == yil:
                if ay == "Ocak":
                    ocakS += j
                    ocakO +=k
                if ay == "Şubat":
                    subatS += j
                    subatO+=k
                if ay == "Mart":
                    martS += j
                    martO += k
                if ay == "Nisan":
                    nisanS += j
                    nisanO+=k
                if ay == "Mayıs":
                    mayisS += j
                    mayisO+=k
                if ay == "Haziran":
                    haziranS += j
                    haziranO+=k
                if ay == "Temmuz":
                    temmuzS += j
                    temmuzO+=k
                if ay == "Ağustos":
                    agustosS += j
                    agustosO+=k
                if ay == "Eylül":
                    eylulS += j
                    eylulO+=k
                if ay == "Ekim":
                    ekimS += j
                    ekimO+=k
                if ay == "Kasım":
                    kasimS += j
                    kasimO+=k
                if ay == "Aralık":
                    aralikS += j
                    aralikO+=k

        aylar = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım",
        "Aralık"]

        set1 = QBarSet("Toplam Satın Alma (Has Cinsinden Gram)")
        set2 = QBarSet("Toplam Ödeme (Has Cinsinden Gram)")
        set3 = QBarSet("Net Kar (Has Cinsinden Gram)")

        set1.append([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])
        set2.append([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])
        set3.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        series = QBarSeries()
        series.append(set1)
        series.append(set2)
        series.append(set3)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Yıllık Alışveriş Çizelgesi")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(aylar)

        axisY = QValueAxis()

        if max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>700 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>700:
            axisY.setRange(0, 800)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>600 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>600:
            axisY.setRange(0, 700)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>500 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>500:
            axisY.setRange(0, 600)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>400 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>400:
            axisY.setRange(0, 500)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>300 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>300:
            axisY.setRange(0, 400)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>200 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>200:
            axisY.setRange(0,300)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>100 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>100:
            axisY.setRange(0, 200)
        elif max([ocakS, subatS, martS, nisanS, mayisS, haziranS, temmuzS, agustosS, eylulS, ekimS, kasimS, aralikS])>50 or max([ocakO, subatO, martO, nisanO, mayisO, haziranO, temmuzO, agustosO, eylulO, ekimO, kasimO, aralikO])>50:
            axisY.setRange(0, 100)
        else:
            axisY.setRange(0, 50)


        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        series.attachAxis(axisY)
        series.attachAxis(axisX)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.ui.verticalLayout_4.addWidget(self.chartView)


    def musteriSec(self):

        self.secilenMusteri = self.ui.tableView_Musteriler.currentIndex().model().itemData(self.ui.tableView_Musteriler.currentIndex()).get(0)

        with sqlite3.connect("musteriler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT satilannethas FROM '{self.secilenMusteri}'")
            self.satilanToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT odemenethas FROM '{self.secilenMusteri}'")
            self.odemeToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT iadenethas FROM '{self.secilenMusteri}'")
            self.iadeToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT iadeodemenethas FROM '{self.secilenMusteri}'")
            self.iadeOdemeToplamHas = cursor.fetchall()
            cursor.execute(f"SELECT sondurum FROM TumMusteriler WHERE adi='{self.secilenMusteri}'")
            self.sonDurumLine = cursor.fetchall()
            cursor.execute(f"SELECT rowid,tarih,islemturu FROM '{self.secilenMusteri}'")
            self.tarihveislem = cursor.fetchall()

            ###### ALIŞVERİŞ ÇİZELGESİ İÇİN TARİHLER BELİRLENİYOR

            cursor.execute(f"SELECT tarih FROM '{self.secilenMusteri}'")
            self.tarih = cursor.fetchall()
            self.yilListesi = []
            for i in self.tarih:
                ss = i[0].split(".")
                ss[0] = int(ss[0])
                ss[1] = int(ss[1])
                ss[2] = int(ss[2])

                bugun = datetime.date.today()
                bugununYili = datetime.date.strftime(bugun, '%Y')
                tarih = bugun.replace(ss[0], ss[1], ss[2])
                ay = datetime.date.strftime(tarih, '%B')
                self.yil = datetime.date.strftime(tarih, '%Y')
                if not self.yilListesi.__contains__(self.yil):
                    self.yilListesi.append(self.yil)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.yilListesi)

        self.sontarih = "0"
        self.sonislem = ""
        self.sayacs = 1
        self.sayaso = 1
        self.sayaci = 1
        self.sayacio = 1
        for k,i,j in self.tarihveislem:
            if i > self.sontarih:
                if j == "Tartı satış" or j == "Adet satış":
                    self.sontarihsatis = i
                    self.sonislemsatis = j
                    self.sayacs += 1
                if j == "Tartı ödeme" or j == "Adet ödeme" or j =="Nakit ödeme":
                    self.sontarihodeme = i
                    self.sonislemodeme = j
                if j == "Tartı iade" or j == "Adet iade":
                    self.sontarihiade = i
                    self.sonislemiade = j
                if j == "Tartı iade ödeme" or j == "Adet iade ödeme" or j == "Nakit iade ödeme":
                    self.sontarihiadeodeme = i
                    self.sonislemiadeodeme = j


    def bilgileriGoster(self):

        self.ui.label_bakiye.setText(str(self.sonDurumLine[0][0])+" Gram")
        try:
            self.sontarihsatis = self.sontarihsatis.split(".")
            self.ui.label_sonsatis.setText(".".join([i for i in self.sontarihsatis[::-1]]))
            self.sontarihsatis = "-"
        except:
            pass
        try:
            self.sontarihodeme = self.sontarihodeme.split(".")
            self.ui.label_sonodeme.setText(".".join([i for i in self.sontarihodeme[::-1]]))
            self.sontarihodeme = "-"
        except:
            pass
        try:
            self.sontarihiade = self.sontarihiade.split(".")
            self.ui.label_soniade.setText(".".join([i for i in self.sontarihiade[::-1]]))
            self.sontarihiade = "-"
        except:
            pass
        try:
            self.sontarihiadeodeme = self.sontarihiadeodeme.split(".")
            self.ui.label_soniadeodeme.setText(".".join([i for i in self.sontarihiadeodeme[::-1]]))
            self.sontarihiadeodeme = "-"
        except:
            pass

        self.ui.table_alisverisozet = QStandardItemModel()
        with sqlite3.connect("musteriler.db") as connect:
            cursor = connect.cursor()
            self.ui.table_alisverisozet.clear()
            sayac = 1
            sayacrow = 0
            self.ui.table_alisverisozet.setColumnCount(6)
            for r,i,j in self.tarihveislem[::-1]:
                self.ui.table_alisverisozet.setRowCount(sayac)
                cursor.execute(f"SELECT * FROM '{self.secilenMusteri}' WHERE rowid='{r}'")
                liste = cursor.fetchall()
                yeniliste = []
                for k in liste[0]:
                    if k != None:
                        yeniliste.append(f"{k}")

                yeniliste[0] = yeniliste[0].split(".")
                tarih = datetime.date.today()
                tarih = tarih.replace(int(yeniliste[0][0]), int(yeniliste[0][1]), int(yeniliste[0][2]))
                gün = datetime.date.strftime(tarih, '%A')

                self.ui.table_alisverisozet.setItem(sayacrow, 0, QStandardItem(".".join([i for i in yeniliste[0][::-1]]) + "   " + gün))
                self.ui.table_alisverisozet.setItem(sayacrow, 1, QStandardItem(yeniliste[1]))
                self.ui.table_alisverisozet.setItem(sayacrow, 2, QStandardItem(yeniliste[2]))
                if yeniliste[1].__contains__("Tartı"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 3, QStandardItem(yeniliste[3]+"   Gram"))
                if yeniliste[1].__contains__("Adet"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 3, QStandardItem(yeniliste[3]+"   Has"))
                if yeniliste[1].__contains__("Nakit"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 3, QStandardItem(yeniliste[3]+"   TL"))
                if yeniliste[1].__contains__("Tartı"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 4, QStandardItem(yeniliste[4]+"   Milyem"))
                if yeniliste[1].__contains__("Adet"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 4, QStandardItem(yeniliste[4]+"   Adet"))
                if yeniliste[1].__contains__("Nakit"):
                    self.ui.table_alisverisozet.setItem(sayacrow, 4, QStandardItem(yeniliste[4]+"   TL"))
                self.ui.table_alisverisozet.setItem(sayacrow, 5, QStandardItem(yeniliste[5]+"   Gram"))

                sayac+=1
                sayacrow+=1
                if sayac == 365:
                    break

        self.ui.table_alisverisozet.setHorizontalHeaderLabels(["Tarih", "İşlem", "Ürün", "Gram/Has/Nakit", "Milyem/Adet/Has Fiyatı", "Net Has"])

        font = QFont()
        font.setBold(True)
        font.setPointSize(9)
        for i in range(6):
            self.ui.table_alisverisozet.horizontalHeaderItem(i).setFont(font)

    def modelBelirle(self):

        filterProxyModel2 = QSortFilterProxyModel()
        filterProxyModel2.setSourceModel(self.ui.table_alisverisozet)
        filterProxyModel2.setFilterCaseSensitivity(Qt.CaseInsensitive)
        if self.secilenSiralama == "Tarihe Göre":
            filterProxyModel2.setFilterKeyColumn(0)
        if self.secilenSiralama == "İşleme Göre":
            filterProxyModel2.setFilterKeyColumn(1)
        if self.secilenSiralama == "Ürüne Göre":
            filterProxyModel2.setFilterKeyColumn(2)
        self.ui.lineEdit.textChanged.connect(filterProxyModel2.setFilterRegExp)
        self.ui.table_alisverisozet1.setModel(filterProxyModel2)

    def siralamaBelirle(self):
        if self.ui.radioButton_3.isChecked():
            self.secilenSiralama = "Tarihe Göre"

        if self.ui.radioButton_2.isChecked():
            self.secilenSiralama = "İşleme Göre"

        if self.ui.radioButton.isChecked():
            self.secilenSiralama = "Ürüne Göre"

        self.modelBelirle()


class MusteriEkleSilEkrani(QWidget):
    def __init__(self):
        super(MusteriEkleSilEkrani, self).__init__()

        self.ui = Ui_Form_MusteriEkleSil()
        self.ui.setupUi(self)


        self.ui.kaydetButonu.clicked.connect(self.addText)
        self.ui.musteriListesi.clicked.connect(self.findItem)
        self.ui.silButonu.clicked.connect(self.deleteText)


        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumMusteriler")
            self.atolyeler = self.cursor.fetchall()



        self.model = QStandardItemModel(len(self.atolyeler), 1)
        self.model.setHorizontalHeaderLabels(['Müşteriler'])

        self.bosliste = []
        for i in self.atolyeler:
            self.bosliste += i

        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)
        self.ui.arama.textChanged.connect(filterProxyModel.setFilterRegExp)
        self.ui.musteriListesi.setModel(filterProxyModel)
        self.ui.musteriListesi.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.ui.arama.setPlaceholderText("Ara")

        self.items = []
        for i in range(len(self.atolyeler)):
            self.items.append(self.model.item(i).text())


    def addText(self):
        text = self.ui.musteriAdi.toPlainText().lower().capitalize()
        text2 = QStandardItem(text)
        for j in self.items:
            if j == text:
                QMessageBox.warning(self,"Hata","Bu isimle bir müşteri kayıtlı!")
                return
        if text == "":
            QMessageBox.warning(self,"Hata","Herhangi bir isim girmediniz!")
            return
        with sqlite3.connect("musteriler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS '{text}'(tarih TEXT,islemturu TEXT,satilanurun TEXT,satilanurungram NUMERIC,satilanurunmilyem NUMERIC,satilanurunhas NUMERIC,satilanurunadet NUMERIC,satilannethas NUMERIC,odemeurunu TEXT,odemeurungram NUMERIC,odemeurunmilyem NUMERIC,odemeurunhas NUMERIC,odemeurunadet NUMERIC,odemenakitmiktari NUMERIC,odemenakithasfiyati NUMERIC,odemenethas NUMERIC,iadeurunu TEXT,iadeurunugram NUMERIC,iadeurunumilyem NUMERIC,iadeurunhas NUMERIC,iadeurunadet NUMERIC,iadenethas NUMERIC,iadeodemeurunu TEXT,iadeodemeurungram NUMERIC,iadeodemeurunmilyem NUMERIC,iadeodemeurunhas NUMERIC,iadeodemeurunadet NUMERIC,iadeodemenakitmiktari NUMERIC,iadeodemenakithasfiyati NUMERIC,iadeodemenethas NUMERIC)")
            cursor.execute("INSERT INTO TumMusteriler VALUES ('{}',{})".format(text,00.00))
            connect.commit()
        self.model.appendRow(text2)
        QMessageBox.information(self,"Kayıt Başarılı","Müşteri eklendi.")
        self.items.append(text)
        self.ui.musteriAdi.clear()
        return


    def findItem(self):

        self.text = self.secilenMusteri = self.ui.musteriListesi.currentIndex().model().itemData(self.ui.musteriListesi.currentIndex()).get(0)
        return


    def deleteText(self):
        try:
            q = QMessageBox.question(self,"Emin misiniz?","{} isimli müşteri silinecek.".format(self.text))
            if q == QMessageBox.Yes:
                with sqlite3.connect("musteriler.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("DELETE FROM TumMusteriler WHERE adi = '{}' ".format(self.text))
                    connect.commit()
                self.model.takeRow(self.row)
                self.items.remove(self.text)
                return
        except:
            return


class MusteriSatisOdemeIadeEkrani(QWidget):
    def __init__(self):
        super(MusteriSatisOdemeIadeEkrani, self).__init__()

        self.ui = Ui_musteriSatisOdemeIade()
        self.ui.setupUi(self)

        self.ui.lineEdit_Arama.setPlaceholderText("Müşteri Ara")

        # RADİOBOX DEFAULT SEÇİMLER
        self.ui.radioB_MusteriSatisGram.click()
        self.ui.radioB_MusteriSatisMilyem.click()
        self.ui.radioB_MusteriOdemeGram.click()
        self.ui.radioB_MusteriOdemeMilyem.click()
        self.ui.radioB_MusteriIadeGram.click()
        self.ui.radioB_MusteriIadeMilyem.click()
        self.ui.radioB_MusteriIadeOdemeGram.click()
        self.ui.radioB_MusteriIadeOdemeMilyem.click()

        ####   RADİOBOX DEĞİŞTİRME   ####
        self.ui.radioB_MusteriSatisGram.clicked.connect(lambda: self.ui.radioB_MusteriSatisMilyem.click())
        self.ui.radioB_MusteriSatisHas.clicked.connect(lambda: self.ui.radioB_MusteriSatisAdet.click())

        self.ui.radioB_MusteriOdemeGram.clicked.connect(lambda: self.ui.radioB_MusteriOdemeMilyem.click())
        self.ui.radioB_MusteriOdemeHas.clicked.connect(lambda: self.ui.radioB_MusteriOdemeAdet.click())
        self.ui.radioB_MusteriOdemeNakit.clicked.connect(lambda: self.ui.radioB_MusteriOdemeHFiyati.click())

        self.ui.radioB_MusteriIadeGram.clicked.connect(lambda: self.ui.radioB_MusteriIadeMilyem.click())
        self.ui.radioB_MusteriIadeHas.clicked.connect(lambda: self.ui.radioB_MusteriIadeAdet.click())

        self.ui.radioB_MusteriIadeOdemeGram.clicked.connect(lambda: self.ui.radioB_MusteriIadeOdemeMilyem.click())
        self.ui.radioB_MusteriIadeOdemeHas.clicked.connect(lambda: self.ui.radioB_MusteriIadeOdemeAdet.click())
        self.ui.radioB_MusteriIadeOdemeNakit.clicked.connect(lambda: self.ui.radioB_MusteriIadeOdemeHFiyati.click())

        # MÜŞTERİ İSİMLERİ FETCH EDİLİYOR
        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumMusteriler")
            self.musteriler = self.cursor.fetchall()

            self.bosliste = []
            for i in self.musteriler:
                self.bosliste += i


        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model = QStandardItemModel(len(self.musteriler), 1)
        self.model.setHorizontalHeaderLabels(['Müşteriler'])

        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        self.filterProxyModel = QSortFilterProxyModel()
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_Arama.textChanged.connect(self.filterProxyModel.setFilterRegExp)
        self.ui.tableView_Musteriler.setModel(self.filterProxyModel)
        self.ui.tableView_Musteriler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #TARİH VE SON DURUM
        self.ui.tableView_Musteriler.clicked.connect(self.sonDurumGoster)
        self.ui.calendarWidget_Takvim.clicked.connect(self.tarihGoster)
        self.ui.pushButtonYenile.clicked.connect(self.musteriListesiYenile)
        self.ui.tableView_Musteriler.clicked.connect(self.odemeUrunleri)
        self.ui.tableView_Musteriler.clicked.connect(self.satisUrunleri)
        self.ui.tableView_Musteriler.clicked.connect(self.iadeUrunleri)


        #HESAPLAMA İŞLEMLERİ
        self.ui.pushB_MusteriSatisHesapla.clicked.connect(self.satisHesapla)
        self.ui.pushB_MusteriOdemeHesapla.clicked.connect(self.odemeHesapla)
        self.ui.pushB_MusteriIadeHesapla.clicked.connect(self.iadeHesapla)
        self.ui.pushB_MusteriIadeOdemeHesapla.clicked.connect(self.iadeOdemeHesapla)

        #KAYIT İŞLEMLERİ
        self.ui.pushB_MusteriSatisKaydet.clicked.connect(self.satisKaydet)
        self.ui.pushB_MusteriOdemeKaydet.clicked.connect(self.odemeKaydet)
        self.ui.pushB_MusteriIadeKaydet.clicked.connect(self.iadeKaydet)
        self.ui.pushB_MusteriIadeOdemeKaydet.clicked.connect(self.iadeOdemeKaydet)

    def iadeOdemeHesapla(self):
        self.gramiadeodeme = self.ui.radioB_MusteriIadeOdemeGram.isChecked()
        self.milyemiadeodeme = self.ui.radioB_MusteriIadeOdemeMilyem.isChecked()
        self.hasiadeodeme = self.ui.radioB_MusteriIadeOdemeHas.isChecked()
        self.adetiadeodeme = self.ui.radioB_MusteriIadeOdemeAdet.isChecked()
        self.nakitiadeodeme = self.ui.radioB_MusteriIadeOdemeNakit.isChecked()
        self.hasfiyatiiadeodeme = self.ui.radioB_MusteriIadeOdemeHFiyati.isChecked()

        try:
            self.lineGramHasiadeOdeme = float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
            self.lineMilyemAdetiadeOdeme = float(self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.text())
        except:
            QMessageBox.warning(self, "Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return

        if self.gramiadeodeme and self.milyemiadeodeme:
            self.satinalmasonuciadeodeme = self.lineGramHasiadeOdeme * self.lineMilyemAdetiadeOdeme / 1000
            self.satinalmasonuciadeodeme = round(self.satinalmasonuciadeodeme, 2)
            self.ui.line_MusteriIadeOdemeHasKarsiligi.setText(str(self.satinalmasonuciadeodeme))
            self.lineGramiadeodeme = float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
            self.lineMilyemiadeodeme = float(self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.text())
            return
        if self.hasiadeodeme and self.adetiadeodeme:
            self.satinalmasonuciadeodeme = self.lineGramHasiadeOdeme * self.lineMilyemAdetiadeOdeme
            self.satinalmasonuciadeodeme = round(self.satinalmasonuciadeodeme, 2)
            self.ui.line_MusteriIadeOdemeHasKarsiligi.setText(str(self.satinalmasonuciadeodeme))
            self.lineHasiadeodeme = float(self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.text())
            self.lineAdetiadeodeme = float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
            return
        if self.nakitiadeodeme and self.hasfiyatiiadeodeme:
            self.satinalmasonuciadeodeme = self.lineGramHasiadeOdeme / self.lineMilyemAdetiadeOdeme
            self.satinalmasonuciadeodeme = round(self.satinalmasonuciadeodeme, 2)
            self.ui.line_MusteriIadeOdemeHasKarsiligi.setText(str(self.satinalmasonuciadeodeme))
            self.lineNakitiadeOdeme = float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
            self.lineHasFiyatiiadeOdeme = float(self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.text())
            return

    def iadeOdemeKaydet(self):

        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumMusteriler WHERE adi ='{}'".format(self.musteriadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__MusteriSonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_MusteriIadeOdemeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_MusteriIadeOdemeHasKarsiligi.text())
                sonuc = float(self.ui.label__MusteriSonDurum.text()) + kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:

                self.kaydedilecekiadeodemeurunu = self.ui.tableView_3.currentIndex().model().itemData(self.ui.tableView_3.currentIndex()).get(0)

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nAtölye: {}\n\nİade edilen ödeme ürünü: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.musteriadi,self.kaydedilecekiadeodemeurunu,self.ui.line_MusteriIadeOdemeHasKarsiligi.text(),self.ui.label__MusteriSonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramiadeodeme and self.milyemiadeodeme:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,iadeodemeurunu,iadeodemeurungram,iadeodemeurunmilyem,iadeodemenethas) VALUES('{self.tarih}','Tartı iade ödeme','{self.kaydedilecekiadeodemeurunu}',{self.lineGramiadeodeme},{self.lineMilyemiadeodeme},{float(self.ui.line_MusteriIadeOdemeHasKarsiligi.text())})")
                        elif self.hasiadeodeme and self.adetiadeodeme:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,iadeodemeurunu,iadeodemeurunhas,iadeodemeurunadet,iadeodemenethas) VALUES('{self.tarih}','Adet iade Ödeme','{self.kaydedilecekiadeodemeurunu}',{self.lineHasiadeodeme},{self.lineAdetiadeodeme},{float(self.ui.line_MusteriIadeOdemeHasKarsiligi.text())})")
                        elif self.nakitiadeodeme and self.hasfiyatiiadeodeme:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,iadeodemeurunu,iadeodemenakitmiktari,iadeodemenakithasfiyati,iadeodemenethas) VALUES('{self.tarih}','Nakit iade ödeme','{self.kaydedilecekiadeodemeurunu}',{self.lineNakitiadeOdeme},{self.lineHasFiyatiiadeOdeme},{float(self.ui.line_MusteriIadeOdemeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()

                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumMusteriler SET sondurum={sonuc} WHERE adi='{self.musteriadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return

            try:
                with sqlite3.connect("nethurda.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("SELECT urunadi FROM TumHurdalar")
                    urunler = cursor.fetchall()

                    for urun in urunler:
                        for i in urun:
                            if i == self.kaydedilecekiadeodemeurunu:
                                if self.gramodeme and self.milyemodeme:
                                    cursor.execute(
                                        f"SELECT urungrami FROM TumHurdalar WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    urungrami = cursor.fetchall()
                                    try:
                                        kayit = float(urungrami[0][0]) - float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
                                    except:
                                        kayit = 0-float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.clear()
                                    self.ui.line_MusteriIadeOdemeGramHasNakit.clear()
                                    self.ui.line_MusteriIadeOdemeHasKarsiligi.clear()
                                    return
                                if self.hasodeme and self.adetodeme:
                                    cursor.execute(f"SELECT urunadeti FROM TumHurdalar WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    urunadeti = cursor.fetchall()
                                    try:
                                        kayit = float(urunadeti[0][0]) - float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
                                    except:
                                        kayit = 0-float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.clear()
                                    self.ui.line_MusteriIadeOdemeGramHasNakit.clear()
                                    self.ui.line_MusteriIadeOdemeHasKarsiligi.clear()
                                    return
                                if self.nakitodeme and self.hasfiyati:
                                    cursor.execute(f"SELECT nakit FROM TumHurdalar WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    urunadeti = cursor.fetchall()
                                    try:
                                        kayit = float(urunadeti[0][0]) - float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
                                    except:
                                        kayit = 0-float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET nakit={kayit} WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.clear()
                                    self.ui.line_MusteriIadeOdemeGramHasNakit.clear()
                                    self.ui.line_MusteriIadeOdemeHasKarsiligi.clear()
                                    return
                    if self.gramiadeodeme and self.milyemiadeodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,urungrami) VALUES('{self.kaydedilecekiadeodemeurunu}',{-float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())})")
                        connect.commit()

                    if self.hasiadeodeme and self.adetiadeodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,urunadeti) VALUES('{self.kaydedilecekiadeodemeurunu}',{-float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())})")
                        connect.commit()

                    if self.nakitiadeodeme and self.hasfiyatiiadeodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,nakit) VALUES('{self.kaydedilecekiadeodemeurunu}',{-float(self.ui.line_MusteriIadeOdemeGramHasNakit.text())})")
                        connect.commit()

                    self.ui.line_MusteriIadeOdemeMilyemAdetHFiyati.clear()
                    self.ui.line_MusteriIadeOdemeGramHasNakit.clear()
                    self.ui.line_MusteriIadeOdemeHasKarsiligi.clear()
                    return
            except:
                pass

    def iadeHesapla(self):

        self.gramiade = self.ui.radioB_MusteriIadeGram.isChecked()
        self.milyemiade = self.ui.radioB_MusteriIadeMilyem.isChecked()
        self.hasiade = self.ui.radioB_MusteriIadeHas.isChecked()
        self.adetiade = self.ui.radioB_MusteriIadeAdet.isChecked()
        try:
            self.lineGramHasiade = float(self.ui.line_MusteriIadeGramHas.text())
            self.lineMilyemAdetiade = float(self.ui.line_MusteriIadeMilyemAdet.text())
        except:
            QMessageBox.warning(self, "Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return
        if self.gramiade and self.milyemiade:
            self.satinalmasonuc = self.lineGramHasiade * self.lineMilyemAdetiade / 1000
            self.satinalmasonuc = round(self.satinalmasonuc, 2)
            self.ui.line_MusteriIadeHasKarsiligi.setText(str(self.satinalmasonuc))
            self.lineGramiade = float(self.ui.line_MusteriIadeGramHas.text())
            self.lineMilyemiade = float(self.ui.line_MusteriIadeMilyemAdet.text())
            return
        if self.hasiade and self.adetiade:
            self.satinalmasonuc = self.lineGramHasiade * self.lineMilyemAdetiade
            self.satinalmasonuc = round(self.satinalmasonuc, 2)
            self.ui.line_MusteriIadeHasKarsiligi.setText(str(self.satinalmasonuc))
            self.lineHasiade = float(self.ui.line_MusteriIadeMilyemAdet.text())
            self.lineAdetiade = float(self.ui.line_MusteriIadeGramHas.text())
            return

    def iadeKaydet(self):

        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumMusteriler WHERE adi ='{}'".format(self.musteriadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__MusteriSonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_MusteriIadeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_MusteriIadeHasKarsiligi.text())
                sonuc = float(self.ui.label__MusteriSonDurum.text()) - kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:
                self.kaydedilecekuruniade = self.ui.tableView_2.currentIndex().model().itemData(self.ui.tableView_2.currentIndex()).get(0)

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nMüşteri: {}\n\nİade edilen ürün: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.musteriadi,self.kaydedilecekuruniade,self.ui.line_MusteriIadeHasKarsiligi.text(),self.ui.label__MusteriSonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramiade and self.milyemiade:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,iadeurunu,iadeurunugram,iadeurunumilyem,iadenethas) VALUES('{self.tarih}','Tartı iade','{self.kaydedilecekuruniade}',{self.lineGramiade},{self.lineMilyemiade},{float(self.ui.line_MusteriIadeHasKarsiligi.text())})")
                        elif self.hasiade and self.adetiade:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,iadeurunu,iadeurunhas,iadeurunadet,iadenethas) VALUES('{self.tarih}','Adet iade','{self.kaydedilecekuruniade}',{self.lineHasiade},{self.lineAdetiade},{float(self.ui.line_MusteriIadeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()
                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumMusteriler SET sondurum={sonuc} WHERE adi='{self.musteriadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return
        else:
            QMessageBox.warning(self, "Hata", "Hesaplama yapılmadan kayıt yapılamaz!")

        try:
            with sqlite3.connect("neturun.db") as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT urunadi FROM TumUrunler")
                urunler = cursor.fetchall()

                for urun in urunler:
                    for i in urun:
                        if i == f"{self.kaydedilecekuruniade}":
                            if self.gramiade and self.milyemiade:
                                cursor.execute(f"SELECT urungrami FROM TumUrunler WHERE urunadi='{self.kaydedilecekuruniade}'")
                                urungrami = cursor.fetchall()
                                try:
                                    kayit = float(urungrami[0][0]) + float(self.ui.line_MusteriIadeGramHas.text())
                                except:
                                    kayit = float(self.ui.line_MusteriIadeGramHas.text())
                                cursor.execute(f"UPDATE TumUrunler SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekuruniade}'")
                                connect.commit()
                                self.ui.line_MusteriIadeGramHas.clear()
                                self.ui.line_MusteriIadeMilyemAdet.clear()
                                self.ui.line_MusteriIadeHasKarsiligi.clear()
                                return
                            if self.hasiade and self.adetiade:
                                cursor.execute(
                                    f"SELECT urunadeti FROM TumUrunler WHERE urunadi='{self.kaydedilecekuruniade}'")
                                urunadeti = cursor.fetchall()
                                try:
                                    kayit = float(urunadeti[0][0]) + float(self.ui.line_MusteriIadeGramHas.text())
                                except:
                                    kayit = float(self.ui.line_MusteriIadeGramHas.text())
                                cursor.execute(
                                    f"UPDATE TumUrunler SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekuruniade}'")
                                connect.commit()
                                self.ui.line_MusteriIadeGramHas.clear()
                                self.ui.line_MusteriIadeMilyemAdet.clear()
                                self.ui.line_MusteriIadeHasKarsiligi.clear()
                                return

                self.ui.line_MusteriIadeGramHas.clear()
                self.ui.line_MusteriIadeMilyemAdet.clear()
                self.ui.line_MusteriIadeHasKarsiligi.clear()
                return
        except:
            pass

    def odemeHesapla(self):

        self.gramodeme = self.ui.radioB_MusteriOdemeGram.isChecked()
        self.milyemodeme = self.ui.radioB_MusteriOdemeMilyem.isChecked()
        self.hasodeme = self.ui.radioB_MusteriOdemeHas.isChecked()
        self.adetodeme = self.ui.radioB_MusteriOdemeAdet.isChecked()
        self.nakitodeme = self.ui.radioB_MusteriOdemeNakit.isChecked()
        self.hasfiyati = self.ui.radioB_MusteriOdemeHFiyati.isChecked()

        try:
            self.lineGramHasOdeme = float(self.ui.line_MusteriOdemeGramHasNakit.text())
            self.lineMilyemAdetOdeme = float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())
        except:
            QMessageBox.warning(self, "Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return

        if self.gramodeme and self.milyemodeme:
            self.satinalmasonucodeme = self.lineGramHasOdeme * self.lineMilyemAdetOdeme / 1000
            self.satinalmasonucodeme = round(self.satinalmasonucodeme, 2)
            self.ui.line_MusteriOdemeHasKarsiligi.setText(str(self.satinalmasonucodeme))
            self.lineGramodeme = float(self.ui.line_MusteriOdemeGramHasNakit.text())
            self.lineMilyemodeme = float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())
            return
        if self.hasodeme and self.adetodeme:
            self.satinalmasonucodeme = self.lineGramHasOdeme * self.lineMilyemAdetOdeme
            self.satinalmasonucodeme = round(self.satinalmasonucodeme, 2)
            self.ui.line_MusteriOdemeHasKarsiligi.setText(str(self.satinalmasonucodeme))
            self.lineHasodeme = float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())
            self.lineAdetodeme = float(self.ui.line_MusteriOdemeGramHasNakit.text())
            return
        if self.nakitodeme and self.hasfiyati:
            self.satinalmasonucodeme = self.lineGramHasOdeme / self.lineMilyemAdetOdeme
            self.satinalmasonucodeme = round(self.satinalmasonucodeme, 2)
            self.ui.line_MusteriOdemeHasKarsiligi.setText(str(self.satinalmasonucodeme))
            self.lineNakitOdeme = float(self.ui.line_MusteriOdemeGramHasNakit.text())
            self.lineHasFiyatiOdeme = float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())
            return

    def odemeKaydet(self):

        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumMusteriler WHERE adi ='{}'".format(self.musteriadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__MusteriSonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_MusteriOdemeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_MusteriOdemeHasKarsiligi.text())
                sonuc = float(self.ui.label__MusteriSonDurum.text()) - kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:

                self.kaydedilecekodemeurunu = self.ui.comboB_MusteriOdemeUrunu.currentText()

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nMüşteri: {}\n\nÖdeme alınan ürün: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.musteriadi,self.kaydedilecekodemeurunu,self.ui.line_MusteriOdemeHasKarsiligi.text(),self.ui.label__MusteriSonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramodeme and self.milyemodeme:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,odemeurunu,odemeurungram,odemeurunmilyem,odemenethas) VALUES('{self.tarih}','Tartı ödeme','{self.kaydedilecekodemeurunu}',{self.lineGramodeme},{self.lineMilyemodeme},{float(self.ui.line_MusteriOdemeHasKarsiligi.text())})")
                        elif self.hasodeme and self.adetodeme:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,odemeurunu,odemeurunhas,odemeurunadet,odemenethas) VALUES('{self.tarih}','Adet ödeme','{self.kaydedilecekodemeurunu}',{self.lineHasodeme},{self.lineAdetodeme},{float(self.ui.line_MusteriOdemeHasKarsiligi.text())})")
                        elif self.nakitodeme and self.hasfiyati:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,odemeurunu,odemenakitmiktari,odemenakithasfiyati,odemenethas) VALUES('{self.tarih}','Nakit ödeme','{self.kaydedilecekodemeurunu}',{self.lineNakitOdeme},{self.lineHasFiyatiOdeme},{float(self.ui.line_MusteriOdemeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()

                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumMusteriler SET sondurum={sonuc} WHERE adi='{self.musteriadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return

            try:
                with sqlite3.connect("nethurda.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("SELECT urunadi,birimfiyati FROM TumHurdalar")
                    urunler = cursor.fetchall()

                    for urun,fiyat in urunler:
                        if urun == f"{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}":
                            if self.gramodeme and self.milyemodeme:
                                cursor.execute(f"SELECT urungrami FROM TumHurdalar WHERE urunadi='{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}'")
                                urungrami = cursor.fetchall()
                                try:
                                    kayit = float(urungrami[0][0]) + float(self.ui.line_MusteriOdemeGramHasNakit.text())
                                except:
                                    kayit = float(self.ui.line_MusteriOdemeGramHasNakit.text())
                                cursor.execute(f"UPDATE TumHurdalar SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}'")
                                connect.commit()
                                self.ui.line_MusteriOdemeGramHasNakit.clear()
                                self.ui.line_MusteriOdemeMilyemAdetHFiyati.clear()
                                self.ui.line_MusteriOdemeHasKarsiligi.clear()
                                return
                            if self.hasodeme and self.adetodeme:
                                cursor.execute(f"SELECT urunadeti FROM TumHurdalar WHERE urunadi='{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}'")
                                urunadeti = cursor.fetchall()
                                try:
                                    kayit = float(urunadeti[0][0]) + float(self.ui.line_MusteriOdemeGramHasNakit.text())
                                except:
                                    kayit = float(self.ui.line_MusteriOdemeGramHasNakit.text())
                                cursor.execute(f"UPDATE TumHurdalar SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}'")
                                connect.commit()
                                self.ui.line_MusteriOdemeGramHasNakit.clear()
                                self.ui.line_MusteriOdemeMilyemAdetHFiyati.clear()
                                self.ui.line_MusteriOdemeHasKarsiligi.clear()
                                return
                            if self.nakitodeme and self.hasfiyati:
                                cursor.execute(f"SELECT nakit FROM TumHurdalar WHERE urunadi='{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}'")
                                urunadeti = cursor.fetchall()
                                try:
                                    kayit = float(urunadeti[0][0]) + float(self.ui.line_MusteriOdemeGramHasNakit.text())
                                except:
                                    kayit = float(self.ui.line_MusteriOdemeGramHasNakit.text())
                                cursor.execute(f"UPDATE TumHurdalar SET nakit={kayit} WHERE urunadi='{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}'")
                                connect.commit()
                                self.ui.line_MusteriOdemeGramHasNakit.clear()
                                self.ui.line_MusteriOdemeMilyemAdetHFiyati.clear()
                                self.ui.line_MusteriOdemeHasKarsiligi.clear()
                                return

                    if self.gramodeme and self.milyemodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,urungrami,birimfiyati) VALUES('{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}',{float(self.ui.line_MusteriOdemeGramHasNakit.text())},{float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())})")
                        connect.commit()

                    if self.hasodeme and self.adetodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,urunadeti,birimfiyati) VALUES('{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}',{float(self.ui.line_MusteriOdemeGramHasNakit.text())},{float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())})")
                        connect.commit()

                    if self.nakitodeme and self.hasfiyati:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,nakit,birimfiyati) VALUES('{self.kaydedilecekodemeurunu} {float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())}',{float(self.ui.line_MusteriOdemeGramHasNakit.text())},{float(self.ui.line_MusteriOdemeMilyemAdetHFiyati.text())})")
                        connect.commit()

                    self.ui.line_MusteriOdemeGramHasNakit.clear()
                    self.ui.line_MusteriOdemeMilyemAdetHFiyati.clear()
                    self.ui.line_MusteriOdemeHasKarsiligi.clear()
                    return
            except:
                pass

    def satisHesapla(self):
        self.gramsatis = self.ui.radioB_MusteriSatisGram.isChecked()
        self.milyemsatis = self.ui.radioB_MusteriSatisMilyem.isChecked()
        self.hassatis = self.ui.radioB_MusteriSatisHas.isChecked()
        self.adetsatis = self.ui.radioB_MusteriSatisAdet.isChecked()
        try:
            self.lineGramHassatis = float(self.ui.line_MusteriSatisGramHas.text())
            self.lineMilyemAdetsatis = float(self.ui.line_MusteriSatisMilyemAdet.text())
        except:
            QMessageBox.warning(self,"Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return
        if self.gramsatis and self.milyemsatis:
            self.satissonuc = self.lineGramHassatis * self.lineMilyemAdetsatis /1000
            self.satissonuc = round(self.satissonuc, 2)
            self.ui.line_MusteriSatisHasKarsiligi.setText(str(self.satissonuc))
            self.lineGramSatis = float(self.ui.line_MusteriSatisGramHas.text())
            self.lineMilyemSatis = float(self.ui.line_MusteriSatisMilyemAdet.text())
            return
        if self.hassatis and self.adetsatis:
            self.satissonuc = self.lineGramHassatis * self.lineMilyemAdetsatis
            self.satissonuc = round(self.satissonuc, 2)
            self.ui.line_MusteriSatisHasKarsiligi.setText(str(self.satissonuc))
            self.lineHasSatis = float(self.ui.line_MusteriSatisMilyemAdet.text())
            self.lineAdetSatis = float(self.ui.line_MusteriSatisGramHas.text())
            return


    def satisKaydet(self):

        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumMusteriler WHERE adi ='{}'".format(self.musteriadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__MusteriSonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_MusteriSatisHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_MusteriSatisHasKarsiligi.text())
                sonuc = float(self.ui.label__MusteriSonDurum.text()) + kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:
                self.kaydedilecekurun = self.ui.tableView.currentIndex().model().itemData(self.ui.tableView.currentIndex()).get(0)

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nMüşteri: {}\n\nSatılan ürün: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.musteriadi,self.kaydedilecekurun,self.ui.line_MusteriSatisHasKarsiligi.text(),self.ui.label__MusteriSonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramsatis and self.milyemsatis:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,satilanurun,satilanurungram,satilanurunmilyem,satilannethas) VALUES('{self.tarih}','Tartı satış','{self.kaydedilecekurun}',{self.lineGramSatis},{self.lineMilyemSatis},{float(self.ui.line_MusteriSatisHasKarsiligi.text())})")
                        elif self.hassatis and self.adetsatis:
                            cursor.execute(f"INSERT INTO '{self.musteriadi}'(tarih,islemturu,satilanurun,satilanurunhas,satilanurunadet,satilannethas) VALUES('{self.tarih}','Adet satış','{self.kaydedilecekurun}',{self.lineHasSatis},{self.lineAdetSatis},{float(self.ui.line_MusteriSatisHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()
                    with sqlite3.connect("musteriler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumMusteriler SET sondurum={sonuc} WHERE adi='{self.musteriadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return
        else:
            QMessageBox.warning(self, "Hata", "Hesaplama yapılmadan kayıt yapılamaz!")

        try:
            with sqlite3.connect("neturun.db") as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT urunadi FROM TumUrunler")
                urunler = cursor.fetchall()

                for urun in urunler:
                    for i in urun:
                        if i == f"{self.kaydedilecekurun}":
                            if self.gramsatis and self.milyemsatis:
                                cursor.execute(f"SELECT urungrami FROM TumUrunler WHERE urunadi='{self.kaydedilecekurun}'")
                                urungrami = cursor.fetchall()
                                try:
                                    kayit = float(urungrami[0][0]) - float(self.ui.line_MusteriSatisGramHas.text())
                                except:
                                    kayit = 0-float(self.ui.line_MusteriSatisGramHas.text())
                                cursor.execute(f"UPDATE TumUrunler SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekurun}'")
                                connect.commit()
                                self.ui.line_MusteriSatisGramHas.clear()
                                self.ui.line_MusteriSatisMilyemAdet.clear()
                                self.ui.line_MusteriSatisHasKarsiligi.clear()
                                return
                            if self.hassatis and self.adetsatis:
                                cursor.execute(
                                    f"SELECT urunadeti FROM TumUrunler WHERE urunadi='{self.kaydedilecekurun}'")
                                urunadeti = cursor.fetchall()
                                try:
                                    kayit = float(urunadeti[0][0]) - float(self.ui.line_MusteriSatisGramHas.text())
                                except:
                                    kayit = 0-float(self.ui.line_MusteriSatisGramHas.text())
                                cursor.execute(
                                    f"UPDATE TumUrunler SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekurun}'")
                                connect.commit()
                                self.ui.line_MusteriSatisGramHas.clear()
                                self.ui.line_MusteriSatisMilyemAdet.clear()
                                self.ui.line_MusteriSatisHasKarsiligi.clear()
                                return

                self.ui.line_MusteriSatisGramHas.clear()
                self.ui.line_MusteriSatisMilyemAdet.clear()
                self.ui.line_MusteriSatisHasKarsiligi.clear()
                return
        except:
            pass


    def odemeUrunleri(self):

        self.musteriadi = self.ui.tableView_Musteriler.currentIndex().model().itemData(self.ui.tableView_Musteriler.currentIndex()).get(0)
        self.ui.comboB_MusteriOdemeUrunu.clear()

        odemeUrunleri = ["8 Ayar Hurda","10 Ayar Hurda","14 Ayar Hurda","18 Ayar Hurda","22 Ayar Hurda","Has","Nakit","Çeyrek","Yarım","Tam","Diğer"]

        with sqlite3.connect("nethurda.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT urunadi,urungrami,urunadeti,nakit FROM TumHurdalar")
            hurdalar = cursor.fetchall()

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model4 = QStandardItemModel(len(hurdalar), 2)
        self.model4.setHorizontalHeaderLabels(['Ürünler', 'Miktarı'])

        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model4)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_3.textChanged.connect(filterProxyModel.setFilterRegExp)
        self.ui.tableView_3.setModel(filterProxyModel)
        self.ui.tableView_3.setColumnWidth(0, 200)

        sayac = 0
        for i, j, k,m in hurdalar:
            if j != 0 and k != 0 and m !=0:
                if k == None and m == None:
                    self.model4.setItem(sayac, 0, QStandardItem(i))
                    self.model4.setItem(sayac, 1, QStandardItem(str(j) + " Gram"))
                    sayac += 1
                if j == None and m==None:
                    self.model4.setItem(sayac, 0, QStandardItem(i))
                    self.model4.setItem(sayac, 1, QStandardItem(str(k) + " Adet"))
                    sayac += 1
                if j==None and k==None:
                    self.model4.setItem(sayac, 0, QStandardItem(i))
                    self.model4.setItem(sayac, 1, QStandardItem(str(m) + " TL"))
                    sayac += 1


        with sqlite3.connect("musteriler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT odemeurunu FROM '{self.musteriadi}'")
            iadeEdilebilenOdeme = cursor.fetchall()


        for urun in odemeUrunleri:
            self.ui.comboB_MusteriOdemeUrunu.addItem(urun)


    def musteriListesiYenile(self):

        # MÜŞTERİ İSİMLERİ FETCH EDİLİYOR
        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumMusteriler")
            self.musteriler = self.cursor.fetchall()

            self.bosliste = []
            for i in self.musteriler:
                self.bosliste += i

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model = QStandardItemModel(len(self.musteriler), 1)
        self.model.setHorizontalHeaderLabels(['Müşteriler'])

        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        self.filterProxyModel = QSortFilterProxyModel()
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_Arama.textChanged.connect(self.filterProxyModel.setFilterRegExp)
        self.ui.tableView_Musteriler.setModel(self.filterProxyModel)
        self.ui.tableView_Musteriler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def tarihGoster(self):
        tarih = self.ui.calendarWidget_Takvim.selectedDate().getDate()
        self.tarih = f"{tarih[0]}.{tarih[1]}.{tarih[2]}"

    def sonDurumGoster(self):


        self.musteriadi = self.ui.tableView_Musteriler.currentIndex().model().itemData(self.ui.tableView_Musteriler.currentIndex()).get(0)

        with sqlite3.connect("musteriler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumMusteriler WHERE adi ='{}'".format(self.musteriadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()

        self.ui.label__MusteriSonDurum.setText(str(self.sondurum[0][0]))

    def iadeUrunleri(self):

        self.musteriadi = self.ui.tableView_Musteriler.currentIndex().model().itemData(self.ui.tableView_Musteriler.currentIndex()).get(0)

        with sqlite3.connect("neturun.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT urunadi,urungrami,urunadeti FROM TumUrunler")
            satisUrunleri = cursor.fetchall()

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model3 = QStandardItemModel(len(satisUrunleri[0]), 2)
        self.model3.setHorizontalHeaderLabels(['Ürünler','Miktarı'])


        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model3)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_2.textChanged.connect(filterProxyModel.setFilterRegExp)
        self.ui.tableView_2.setModel(filterProxyModel)
        self.ui.tableView_2.setColumnWidth(0,285)

        sayac = 0
        for i,j,k in satisUrunleri:
            if j != 0 and k!=0:
                if k == None:
                    self.model3.setItem(sayac,0,QStandardItem(i))
                    self.model3.setItem(sayac,1,QStandardItem(str(j)+" Gram"))
                    sayac +=1
                if j == None:
                    self.model3.setItem(sayac,0,QStandardItem(i))
                    self.model3.setItem(sayac,1,QStandardItem(str(k) + " Adet"))
                    sayac+=1
        return

    def satisUrunleri(self):

        with sqlite3.connect("neturun.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT urunadi,urungrami,urunadeti FROM TumUrunler")
            satisUrunleri = cursor.fetchall()

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model2 = QStandardItemModel(len(satisUrunleri[0]), 2)
        self.model2.setHorizontalHeaderLabels(['Ürünler','Miktarı'])


        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model2)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit.textChanged.connect(filterProxyModel.setFilterRegExp)
        self.ui.tableView.setModel(filterProxyModel)
        self.ui.tableView.setColumnWidth(0,285)

        sayac = 0
        for i,j,k in satisUrunleri:
            if j != 0 and k!=0:
                if k == None:
                    self.model2.setItem(sayac,0,QStandardItem(i))
                    self.model2.setItem(sayac,1,QStandardItem(str(j)+" Gram"))
                    sayac +=1
                if j == None:
                    self.model2.setItem(sayac,0,QStandardItem(i))
                    self.model2.setItem(sayac,1,QStandardItem(str(k) + " Adet"))
                    sayac+=1

        return

class AtolyeSatinalmaOdemeEkrani(QWidget):
    def __init__(self):
        super(AtolyeSatinalmaOdemeEkrani, self).__init__()

        self.ui = Ui_AtolyeSatinalmaOdemeIade()
        self.ui.setupUi(self)

        self.ui.lineEdit_Arama.setPlaceholderText("Atölye Ara")

        #RADİOBOX DEFAULT SEÇİMLER
        self.ui.radioB_SatinalmaGram.click()
        self.ui.radioB_SatinalmaMilyem.click()
        self.ui.radioB_OdemeGram.click()
        self.ui.radioB_OdemeMilyem.click()
        self.ui.radioB_AtolyeIadeGram.click()
        self.ui.radioB_AtolyeIadeMilyem.click()
        self.ui.radioB_AtolyeIadeOdemeGram.click()
        self.ui.radioB_AtolyeIadeOdemeMilyem.click()

        ####   RADİOBOX DEĞİŞTİRME   ####
        self.ui.radioB_SatinalmaGram.clicked.connect(lambda: self.ui.radioB_SatinalmaMilyem.click())
        self.ui.radioB_SatinalmaHas.clicked.connect(lambda :self.ui.radioB_SatinalmaAdet.click())

        self.ui.radioB_OdemeGram.clicked.connect(lambda: self.ui.radioB_OdemeMilyem.click())
        self.ui.radioB_OdemeHas.clicked.connect(lambda: self.ui.radioB_OdemeAdet.click())
        self.ui.radioB_OdemeNakit.clicked.connect(lambda: self.ui.radioB_OdemeHFiyati.click())

        self.ui.radioB_AtolyeIadeGram.clicked.connect(lambda: self.ui.radioB_AtolyeIadeMilyem.click())
        self.ui.radioB_AtolyeIadeHas.clicked.connect(lambda: self.ui.radioB_AtolyeIadeAdet.click())

        self.ui.radioB_AtolyeIadeOdemeGram.clicked.connect(lambda: self.ui.radioB_AtolyeIadeOdemeMilyem.click())
        self.ui.radioB_AtolyeIadeOdemeHas.clicked.connect(lambda: self.ui.radioB_AtolyeIadeOdemeAdet.click())
        self.ui.radioB_AtolyeIadeOdemeNakit.clicked.connect(lambda: self.ui.radioB_AtolyeIadeOdemeHFiyati.click())


        #ATÖLYE İSİMLERİ FETCH EDİLİYOR
        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumAtolyeler")
            self.atolyeler = self.cursor.fetchall()

        self.bosliste = []
        for i in self.atolyeler:
            self.bosliste += i


        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model = QStandardItemModel(len(self.atolyeler), 1)
        self.model.setHorizontalHeaderLabels(['Atölyeler'])

        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        self.filterProxyModel = QSortFilterProxyModel()
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_Arama.textChanged.connect(self.filterProxyModel.setFilterRegExp)
        self.ui.tableView_Atolyeler.setModel(self.filterProxyModel)
        self.ui.tableView_Atolyeler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #TARİH VE SON DURUM
        self.ui.tableView_Atolyeler.clicked.connect(self.sonDurumGoster)
        self.ui.calendarWidget_Takvim.clicked.connect(self.tarihGoster)
        self.ui.pushButtonYenile.clicked.connect(self.atolyeListesiYenile)
        self.ui.tableView_Atolyeler.clicked.connect(self.IadeOdemeUrunleri)
        self.ui.tableView_Atolyeler.clicked.connect(self.odemeUrunleri)


        #HESAPLAMA İŞLEMLERİ
        self.ui.pushB_AtolyeSatinalmaHesapla.clicked.connect(self.satinalimHesapla)
        self.ui.pushB_AtolyeOdemeHesapla.clicked.connect(self.odemeHesapla)
        self.ui.pushB_AtolyeIadeHesapla.clicked.connect(self.iadeHesapla)
        self.ui.pushB_AtolyeIadeOdemeHesapla.clicked.connect(self.iadeOdemeHesapla)

        #KAYIT İŞLEMLERİ
        self.ui.pushB_AtolyeSatinalmaKaydet.clicked.connect(self.urunKaydet)
        self.ui.pushB_AtolyeOdemeKaydet.clicked.connect(self.odemeKaydet)
        self.ui.pushB_AtolyeIadeKaydet.clicked.connect(self.iadeKaydet)
        self.ui.pushB_AtolyeIadeOdemeKaydet.clicked.connect(self.iadeOdemeKaydet)


        #YENİ ÜRÜN CHECKBOX
        self.ui.checkBoxYeniUrun.clicked.connect(self.yeniUrunKontrol)
        self.check = self.ui.checkBoxYeniUrun.isChecked()
        self.ui.line_AtolyeAlinanYeniUrun.setDisabled(True)
        self.ui.label_34.setDisabled(True)


    def iadeOdemeHesapla(self):
        self.gramiadeodeme = self.ui.radioB_AtolyeIadeOdemeGram.isChecked()
        self.milyemiadeodeme = self.ui.radioB_AtolyeIadeOdemeMilyem.isChecked()
        self.hasiadeodeme = self.ui.radioB_AtolyeIadeOdemeHas.isChecked()
        self.adetiadeodeme = self.ui.radioB_AtolyeIadeOdemeAdet.isChecked()
        self.nakitiadeodeme = self.ui.radioB_AtolyeIadeOdemeNakit.isChecked()
        self.hasfiyatiiadeodeme = self.ui.radioB_AtolyeIadeOdemeHFiyati.isChecked()

        try:
            self.lineGramHasiadeOdeme = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
            self.lineMilyemAdetiadeOdeme = float(self.ui.line_AtolyeIadeOdemeMilyemAdet.text())
        except:
            QMessageBox.warning(self, "Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return

        if self.gramiadeodeme and self.milyemiadeodeme:
            self.satinalmasonuciadeodeme = self.lineGramHasiadeOdeme * self.lineMilyemAdetiadeOdeme / 1000
            self.satinalmasonuciadeodeme = round(self.satinalmasonuciadeodeme, 2)
            self.ui.line_AtolyeIadeOdemeHasKarsiligi.setText(str(self.satinalmasonuciadeodeme))
            self.lineGramiadeodeme = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
            self.lineMilyemiadeodeme = float(self.ui.line_AtolyeIadeOdemeMilyemAdet.text())
            return
        if self.hasiadeodeme and self.adetiadeodeme:
            self.satinalmasonuciadeodeme = self.lineGramHasiadeOdeme * self.lineMilyemAdetiadeOdeme
            self.satinalmasonuciadeodeme = round(self.satinalmasonuciadeodeme, 2)
            self.ui.line_AtolyeIadeOdemeHasKarsiligi.setText(str(self.satinalmasonuciadeodeme))
            self.lineHasiadeodeme = float(self.ui.line_AtolyeIadeOdemeMilyemAdet.text())
            self.lineAdetiadeodeme = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
            return
        if self.nakitiadeodeme and self.hasfiyatiiadeodeme:
            self.satinalmasonuciadeodeme = self.lineGramHasiadeOdeme / self.lineMilyemAdetiadeOdeme
            self.satinalmasonuciadeodeme = round(self.satinalmasonuciadeodeme, 2)
            self.ui.line_AtolyeIadeOdemeHasKarsiligi.setText(str(self.satinalmasonuciadeodeme))
            self.lineNakitiadeOdeme = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
            self.lineHasFiyatiiadeOdeme = float(self.ui.line_AtolyeIadeOdemeMilyemAdet.text())
            return

    def iadeOdemeKaydet(self):

        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumAtolyeler WHERE adi ='{}'".format(self.atolyeadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__SonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_AtolyeIadeOdemeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_AtolyeIadeOdemeHasKarsiligi.text())
                sonuc = float(self.ui.label__SonDurum.text()) + kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:

                self.kaydedilecekiadeodemeurunu = self.ui.tableView_2.currentIndex().model().itemData(self.ui.tableView_2.currentIndex()).get(0)

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nAtölye: {}\n\nİade alınan ödeme ürünü: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.atolyeadi,self.kaydedilecekiadeodemeurunu,self.ui.line_AtolyeIadeOdemeHasKarsiligi.text(),self.ui.label__SonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramiadeodeme and self.milyemiadeodeme:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,iadeodemeurunu,iadeodemeurungram,iadeodemeurunmilyem,iadeodemenethas) VALUES('{self.tarih}','Tartı iade ödeme','{self.kaydedilecekiadeodemeurunu}',{self.lineGramiadeodeme},{self.lineMilyemiadeodeme},{float(self.ui.line_AtolyeIadeOdemeHasKarsiligi.text())})")
                        elif self.hasiadeodeme and self.adetiadeodeme:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,iadeodemeurunu,iadeodemeurunhas,iadeodemeurunadet,iadeodemenethas) VALUES('{self.tarih}','Adet iade ödeme','{self.kaydedilecekiadeodemeurunu}',{self.lineHasiadeodeme},{self.lineAdetiadeodeme},{float(self.ui.line_AtolyeIadeOdemeHasKarsiligi.text())})")
                        elif self.nakitiadeodeme and self.hasfiyatiiadeodeme:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,iadeodemeurunu,iadeodemenakitmiktari,iadeodemenakithasfiyati,iadeodemenethas) VALUES('{self.tarih}','Nakit iade ödeme','{self.kaydedilecekiadeodemeurunu}',{self.lineNakitiadeOdeme},{self.lineHasFiyatiiadeOdeme},{float(self.ui.line_AtolyeIadeOdemeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()

                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumAtolyeler SET sondurum={sonuc} WHERE adi='{self.atolyeadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return

            try:
                with sqlite3.connect("nethurda.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("SELECT urunadi FROM TumHurdalar")
                    urunler = cursor.fetchall()

                    for urun in urunler:
                        for i in urun:
                            if i == self.kaydedilecekiadeodemeurunu:
                                if self.gramodeme and self.milyemodeme:
                                    cursor.execute(
                                        f"SELECT urungrami FROM TumHurdalar WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    urungrami = cursor.fetchall()
                                    try:
                                        kayit = float(urungrami[0][0]) + float(self.ui.line_AtolyeIadeOdemeGramHas.text())
                                    except:
                                        kayit = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_AtolyeIadeOdemeMilyemAdet.clear()
                                    self.ui.line_AtolyeIadeOdemeGramHas.clear()
                                    self.ui.line_AtolyeIadeOdemeHasKarsiligi.clear()
                                    return
                                if self.hasodeme and self.adetodeme:
                                    cursor.execute(f"SELECT urunadeti FROM TumHurdalar WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    urunadeti = cursor.fetchall()
                                    try:
                                        kayit = float(urunadeti[0][0]) + float(self.ui.line_AtolyeIadeOdemeGramHas.text())
                                    except:
                                        kayit = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_AtolyeIadeOdemeMilyemAdet.clear()
                                    self.ui.line_AtolyeIadeOdemeGramHas.clear()
                                    self.ui.line_AtolyeIadeOdemeHasKarsiligi.clear()
                                    return
                                if self.nakitodeme and self.hasfiyati:
                                    cursor.execute(f"SELECT nakit FROM TumHurdalar WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    urunadeti = cursor.fetchall()
                                    try:
                                        kayit = float(urunadeti[0][0]) + float(self.ui.line_AtolyeIadeOdemeGramHas.text())
                                    except:
                                        kayit = float(self.ui.line_AtolyeIadeOdemeGramHas.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET nakit={kayit} WHERE urunadi='{self.kaydedilecekiadeodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_AtolyeIadeOdemeMilyemAdet.clear()
                                    self.ui.line_AtolyeIadeOdemeGramHas.clear()
                                    self.ui.line_AtolyeIadeOdemeHasKarsiligi.clear()
                                    return
                    if self.gramiadeodeme and self.milyemiadeodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,urungrami) VALUES('{self.kaydedilecekiadeodemeurunu}',{float(self.ui.line_AtolyeIadeOdemeGramHas.text())})")
                        connect.commit()

                    if self.hasiadeodeme and self.adetiadeodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,urunadeti) VALUES('{self.kaydedilecekiadeodemeurunu}',{float(self.ui.line_AtolyeIadeOdemeGramHas.text())})")
                        connect.commit()

                    if self.nakitiadeodeme and self.hasfiyatiiadeodeme:
                        cursor.execute(f"INSERT INTO TumHurdalar(urunadi,nakit) VALUES('{self.kaydedilecekiadeodemeurunu}',{float(self.ui.line_AtolyeIadeOdemeGramHas.text())})")
                        connect.commit()

                    self.ui.line_AtolyeIadeOdemeMilyemAdet.clear()
                    self.ui.line_AtolyeIadeOdemeGramHas.clear()
                    self.ui.line_AtolyeIadeOdemeHasKarsiligi.clear()
                    return
            except:
                pass


    def iadeHesapla(self):
        self.gramiade = self.ui.radioB_AtolyeIadeGram.isChecked()
        self.milyemiade = self.ui.radioB_AtolyeIadeMilyem.isChecked()
        self.hasiade = self.ui.radioB_AtolyeIadeHas.isChecked()
        self.adetiade = self.ui.radioB_AtolyeIadeAdet.isChecked()
        try:
            self.lineGramHasiade = float(self.ui.line_AtolyeIadeGramHas.text())
            self.lineMilyemAdetiade = float(self.ui.line_AtolyeIadeMilyemAdet.text())
        except:
            QMessageBox.warning(self, "Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return
        if self.gramiade and self.milyemiade:
            self.satinalmasonuc = self.lineGramHasiade * self.lineMilyemAdetiade / 1000
            self.satinalmasonuc = round(self.satinalmasonuc, 2)
            self.ui.line_AtolyeIadeHasKarsiligi.setText(str(self.satinalmasonuc))
            self.lineGramiade = float(self.ui.line_AtolyeIadeGramHas.text())
            self.lineMilyemiade = float(self.ui.line_AtolyeIadeMilyemAdet.text())
            return
        if self.hasiade and self.adetiade:
            self.satinalmasonuc = self.lineGramHasiade * self.lineMilyemAdetiade
            self.satinalmasonuc = round(self.satinalmasonuc, 2)
            self.ui.line_AtolyeIadeHasKarsiligi.setText(str(self.satinalmasonuc))
            self.lineHasiade = float(self.ui.line_AtolyeIadeMilyemAdet.text())
            self.lineAdetiade = float(self.ui.line_AtolyeIadeGramHas.text())
            return

    def iadeKaydet(self):

        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumAtolyeler WHERE adi ='{}'".format(self.atolyeadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__SonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_AtolyeIadeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_AtolyeIadeHasKarsiligi.text())
                sonuc = float(self.ui.label__SonDurum.text()) - kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:
                self.kaydedilecekuruniade = f"{self.ui.comboB_AtolyeIadeUrunler.currentText()} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}"

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nAtölye: {}\n\nİade edilen ürün: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.atolyeadi,self.kaydedilecekuruniade,self.ui.line_AtolyeIadeHasKarsiligi.text(),self.ui.label__SonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramiade and self.milyemiade:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,iadeurunu,iadeurungram,iadeurunmilyem,iadenethas) VALUES('{self.tarih}','Tartı iade','{self.kaydedilecekuruniade}',{self.lineGramiade},{self.lineMilyemiade},{float(self.ui.line_AtolyeIadeHasKarsiligi.text())})")
                        elif self.hasiade and self.adetiade:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,iadeurunu,iadeurunhas,iadeurunadet,iadenethas) VALUES('{self.tarih}','Adet iade','{self.kaydedilecekuruniade}',{self.lineHasiade},{self.lineAdetiade},{float(self.ui.line_AtolyeIadeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()
                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumAtolyeler SET sondurum={sonuc} WHERE adi='{self.atolyeadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return
        else:
            QMessageBox.warning(self, "Hata", "Hesaplama yapılmadan kayıt yapılamaz!")

        try:
            with sqlite3.connect("neturun.db") as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT urunadi FROM TumUrunler")
                urunler = cursor.fetchall()

                for urun in urunler:
                    for i in urun:
                        if i == f"{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}":
                            if self.gramiade and self.milyemiade:
                                cursor.execute(f"SELECT urungrami FROM TumUrunler WHERE urunadi='{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}'")
                                urungrami = cursor.fetchall()
                                try:
                                    kayit = float(urungrami[0][0]) - float(self.ui.line_AtolyeIadeGramHas.text())
                                except:
                                    kayit = 0-float(self.ui.line_AtolyeIadeGramHas.text())
                                cursor.execute(f"UPDATE TumUrunler SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}'")
                                connect.commit()
                                self.ui.line_AtolyeIadeGramHas.clear()
                                self.ui.line_AtolyeIadeMilyemAdet.clear()
                                self.ui.line_AtolyeIadeHasKarsiligi.clear()
                                return
                            if self.hasiade and self.adetiade:
                                cursor.execute(
                                    f"SELECT urunadeti FROM TumUrunler WHERE urunadi='{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}'")
                                urunadeti = cursor.fetchall()
                                try:
                                    kayit = float(urunadeti[0][0]) - float(self.ui.line_AtolyeIadeGramHas.text())
                                except:
                                    kayit = 0-float(self.ui.line_AtolyeIadeGramHas.text())
                                cursor.execute(
                                    f"UPDATE TumUrunler SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}'")
                                connect.commit()
                                self.ui.line_AtolyeIadeGramHas.clear()
                                self.ui.line_AtolyeIadeMilyemAdet.clear()
                                self.ui.line_AtolyeIadeHasKarsiligi.clear()
                                return
                if self.gramiade and self.milyemiade:
                    cursor.execute(f"INSERT INTO TumUrunler(urunadi,urungrami) VALUES('{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}',{-float(self.ui.line_AtolyeIadeGramHas.text())})")
                    connect.commit()

                if self.hasiade and self.adetiade:
                    cursor.execute(f"INSERT INTO TumUrunler(urunadi,urunadeti) VALUES('{self.kaydedilecekuruniade} {float(self.ui.line_AtolyeIadeMilyemAdet.text())} {self.atolyeadi}',{-float(self.ui.line_AtolyeIadeGramHas.text())})")
                    connect.commit()

                self.ui.line_AtolyeIadeGramHas.clear()
                self.ui.line_AtolyeIadeMilyemAdet.clear()
                self.ui.line_AtolyeIadeHasKarsiligi.clear()
                return
        except:
            pass


    def odemeHesapla(self):
        self.gramodeme = self.ui.radioB_OdemeGram.isChecked()
        self.milyemodeme = self.ui.radioB_OdemeMilyem.isChecked()
        self.hasodeme = self.ui.radioB_OdemeHas.isChecked()
        self.adetodeme = self.ui.radioB_OdemeAdet.isChecked()
        self.nakitodeme = self.ui.radioB_OdemeNakit.isChecked()
        self.hasfiyati = self.ui.radioB_OdemeHFiyati.isChecked()

        try:
            self.lineGramHasOdeme = float(self.ui.line_AtolyeOdemeGramHasNakit.text())
            self.lineMilyemAdetOdeme = float(self.ui.line_AtolyeOdemeMilyemAdetFiyat.text())
        except:
            QMessageBox.warning(self,"Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return

        if self.gramodeme and self.milyemodeme:
            self.satinalmasonucodeme = self.lineGramHasOdeme * self.lineMilyemAdetOdeme /1000
            self.satinalmasonucodeme = round(self.satinalmasonucodeme, 2)
            self.ui.line_AtolyeOdemeHasKarsiligi.setText(str(self.satinalmasonucodeme))
            self.lineGramodeme = float(self.ui.line_AtolyeOdemeGramHasNakit.text())
            self.lineMilyemodeme = float(self.ui.line_AtolyeOdemeMilyemAdetFiyat.text())
            return
        if self.hasodeme and self.adetodeme:
            self.satinalmasonucodeme = self.lineGramHasOdeme * self.lineMilyemAdetOdeme
            self.satinalmasonucodeme = round(self.satinalmasonucodeme, 2)
            self.ui.line_AtolyeOdemeHasKarsiligi.setText(str(self.satinalmasonucodeme))
            self.lineHasodeme = float(self.ui.line_AtolyeOdemeMilyemAdetFiyat.text())
            self.lineAdetodeme = float(self.ui.line_AtolyeOdemeGramHasNakit.text())
            return
        if self.nakitodeme and self.hasfiyati:
            self.satinalmasonucodeme = self.lineGramHasOdeme / self.lineMilyemAdetOdeme
            self.satinalmasonucodeme = round(self.satinalmasonucodeme, 2)
            self.ui.line_AtolyeOdemeHasKarsiligi.setText(str(self.satinalmasonucodeme))
            self.lineNakitOdeme = float(self.ui.line_AtolyeOdemeGramHasNakit.text())
            self.lineHasFiyatiOdeme = float(self.ui.line_AtolyeOdemeMilyemAdetFiyat.text())
            return


    def odemeKaydet(self):

        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumAtolyeler WHERE adi ='{}'".format(self.atolyeadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__SonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.line_AtolyeOdemeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.line_AtolyeOdemeHasKarsiligi.text())
                sonuc = float(self.ui.label__SonDurum.text()) - kullanicidegeri
                sonuc = round(sonuc, 2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:

                self.kaydedilecekodemeurunu = self.ui.tableView.currentIndex().model().itemData(self.ui.tableView.currentIndex()).get(0)

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nAtölye: {}\n\nÖdeme ürünü: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.atolyeadi,self.kaydedilecekodemeurunu,self.ui.line_AtolyeOdemeHasKarsiligi.text(),self.ui.label__SonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        if self.gramodeme and self.milyemodeme:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,odemeurunu,odemeurungram,odemeurunmilyem,odemenethas) VALUES('{self.tarih}','Tartı ödeme','{self.kaydedilecekodemeurunu}',{self.lineGramodeme},{self.lineMilyemodeme},{float(self.ui.line_AtolyeOdemeHasKarsiligi.text())})")
                        elif self.hasodeme and self.adetodeme:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,odemeurunu,odemeurunhas,odemeurunadet,odemenethas) VALUES('{self.tarih}','Adet ödeme','{self.kaydedilecekodemeurunu}',{self.lineHasodeme},{self.lineAdetodeme},{float(self.ui.line_AtolyeOdemeHasKarsiligi.text())})")
                        elif self.nakitodeme and self.hasfiyati:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,odemeurunu,odemenakitmiktari,odemenakithasfiyati,odemenethas) VALUES('{self.tarih}','Nakit ödeme','{self.kaydedilecekodemeurunu}',{self.lineNakitOdeme},{self.lineHasFiyatiOdeme},{float(self.ui.line_AtolyeOdemeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()

                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumAtolyeler SET sondurum={sonuc} WHERE adi='{self.atolyeadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return

            try:
                with sqlite3.connect("nethurda.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("SELECT urunadi FROM TumHurdalar")
                    urunler = cursor.fetchall()

                    for urun in urunler:
                        for i in urun:
                            if i == f"{self.kaydedilecekodemeurunu}":
                                if self.gramodeme and self.milyemodeme:
                                    cursor.execute(
                                        f"SELECT urungrami FROM TumHurdalar WHERE urunadi='{self.kaydedilecekodemeurunu}'")
                                    urungrami = cursor.fetchall()
                                    try:
                                        kayit = float(urungrami[0][0]) - float(self.ui.line_AtolyeOdemeGramHasNakit.text())
                                        print(kayit)
                                    except:
                                        kayit = 0- float(self.ui.line_AtolyeOdemeGramHasNakit.text())
                                        print(kayit)
                                    cursor.execute(f"UPDATE TumHurdalar SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_AtolyeOdemeGramHasNakit.clear()
                                    self.ui.line_AtolyeOdemeMilyemAdetFiyat.clear()
                                    self.ui.line_AtolyeOdemeHasKarsiligi.clear()
                                    return
                                if self.hasodeme and self.adetodeme:
                                    cursor.execute(f"SELECT urunadeti FROM TumHurdalar WHERE urunadi='{self.kaydedilecekodemeurunu}'")
                                    urunadeti = cursor.fetchall()
                                    try:
                                        kayit = float(urunadeti[0][0]) - float(self.ui.line_AtolyeOdemeGramHasNakit.text())
                                    except:
                                        kayit = 0-float(self.ui.line_AtolyeOdemeGramHasNakit.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_AtolyeOdemeGramHasNakit.clear()
                                    self.ui.line_AtolyeOdemeMilyemAdetFiyat.clear()
                                    self.ui.line_AtolyeOdemeHasKarsiligi.clear()
                                    return
                                if self.nakitodeme and self.hasfiyati:
                                    cursor.execute(f"SELECT nakit FROM TumHurdalar WHERE urunadi='{self.kaydedilecekodemeurunu}'")
                                    urunadeti = cursor.fetchall()
                                    try:
                                        kayit = float(urunadeti[0][0]) - float(self.ui.line_AtolyeOdemeGramHasNakit.text())
                                    except:
                                        kayit = 0-float(self.ui.line_AtolyeOdemeGramHasNakit.text())
                                    cursor.execute(f"UPDATE TumHurdalar SET nakit={kayit} WHERE urunadi='{self.kaydedilecekodemeurunu}'")
                                    connect.commit()
                                    self.ui.line_AtolyeOdemeGramHasNakit.clear()
                                    self.ui.line_AtolyeOdemeMilyemAdetFiyat.clear()
                                    self.ui.line_AtolyeOdemeHasKarsiligi.clear()
                                    return

                    self.ui.line_AtolyeOdemeGramHasNakit.clear()
                    self.ui.line_AtolyeOdemeMilyemAdetFiyat.clear()
                    self.ui.line_AtolyeOdemeHasKarsiligi.clear()
                    return
            except:
                pass

    def yeniUrunKontrol(self):
        self.check = self.ui.checkBoxYeniUrun.isChecked()
        if self.check:
            self.ui.comboBoxAtolyeSatinAlinanVarUrun.setDisabled(True)
            self.ui.label.setDisabled(True)
            self.ui.line_AtolyeAlinanYeniUrun.setEnabled(True)
            self.ui.label_34.setEnabled(True)

        if not self.check:
            self.ui.comboBoxAtolyeSatinAlinanVarUrun.setEnabled(True)
            self.ui.label.setEnabled(True)
            self.ui.line_AtolyeAlinanYeniUrun.setDisabled(True)
            self.ui.label_34.setDisabled(True)


    def satinalimHesapla(self):
        self.gram = self.ui.radioB_SatinalmaGram.isChecked()
        self.milyem = self.ui.radioB_SatinalmaMilyem.isChecked()
        self.has = self.ui.radioB_SatinalmaHas.isChecked()
        self.adet = self.ui.radioB_SatinalmaAdet.isChecked()
        try:
            self.lineGramHas = float(self.ui.lineAtolyeGramHas.text())
            self.lineMilyemAdet = float(self.ui.lineAtolyeMilyemAdet.text())
        except:
            QMessageBox.warning(self,"Hata","Eksik veya hatalı bilgi!\n(VİRGÜL yerine NOKTA ile hesaplama yapmayı unutmayın)")
            return
        if self.gram and self.milyem:
            self.satinalmasonuc = self.lineGramHas * self.lineMilyemAdet /1000
            self.satinalmasonuc = round(self.satinalmasonuc, 2)
            self.ui.lineAtolyeHasKarsiligi.setText(str(self.satinalmasonuc))
            self.lineGram = float(self.ui.lineAtolyeGramHas.text())
            self.lineMilyem = float(self.ui.lineAtolyeMilyemAdet.text())
            return
        if self.has and self.adet:
            self.satinalmasonuc = self.lineGramHas * self.lineMilyemAdet
            self.satinalmasonuc = round(self.satinalmasonuc,2)
            self.ui.lineAtolyeHasKarsiligi.setText(str(self.satinalmasonuc))
            self.lineHas = float(self.ui.lineAtolyeMilyemAdet.text())
            self.lineAdet = float(self.ui.lineAtolyeGramHas.text())
            return


    def urunKaydet(self):

        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumAtolyeler WHERE adi ='{}'".format(self.atolyeadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
            self.ui.label__SonDurum.setText(str(self.sondurum[0][0]))

        if self.ui.lineAtolyeHasKarsiligi.text() != "":
            try:
                kullanicidegeri = float(self.ui.lineAtolyeHasKarsiligi.text())
                kullanicidegeri = round(kullanicidegeri,2)
                sonuc = float(self.ui.label__SonDurum.text()) + kullanicidegeri
                sonuc = round(sonuc,2)
            except:
                QMessageBox.warning(self,"Hata","Herhangi bir seçim yapılmadı!")
                return

            try:
                if not self.check:
                    self.kaydedilecekurun = self.ui.comboBoxAtolyeSatinAlinanVarUrun.currentText().lower().capitalize()
                if self.check:
                    self.kaydedilecekurun = self.ui.line_AtolyeAlinanYeniUrun.text().lower().capitalize()

                q = QMessageBox.question(self,"Kayıt yapılacak","Tarih: {}\n\nAtölye: {}\n\nAlınan ürün: {}\n\nHas karşılığı: {}\n\nEski son durum: {}\n\nYeni son durum: {}\n\nEmin misiniz?".format(self.tarih,self.atolyeadi,self.kaydedilecekurun,self.ui.lineAtolyeHasKarsiligi.text(),self.ui.label__SonDurum.text(),sonuc))
                if q == QMessageBox.Yes:
                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        if self.gram and self.milyem:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,satinalinanurun,satinalinanurungram,satinalinanurunmilyem,satinalinannethas) VALUES('{self.tarih}','Tartı satın alma','{self.kaydedilecekurun}',{self.lineGram},{self.lineMilyem},{float(self.ui.lineAtolyeHasKarsiligi.text())})")
                        elif self.has and self.adet:
                            cursor.execute(f"INSERT INTO '{self.atolyeadi}'(tarih,islemturu,satinalinanurun,satinalinanurunhas,satinalinanurunadet,satinalinannethas) VALUES('{self.tarih}','Adet satın alma','{self.kaydedilecekurun}',{self.lineHas},{self.lineAdet},{float(self.ui.lineAtolyeHasKarsiligi.text())})")
                        else:
                            QMessageBox.warning(self,"Hata","Kutucuklar uyuşmuyor!")
                            return
                        connect.commit()
                    with sqlite3.connect("atolyeler.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"UPDATE TumAtolyeler SET sondurum={sonuc} WHERE adi='{self.atolyeadi}'")
                        connect.commit()

                    QMessageBox.information(self,"Kayıt başarılı","Bilgiler kaydedildi.")
                else:
                    return
            except:
                QMessageBox.warning(self,"Hata","Tarih veya müşteri seçimi yapılmadı!")
                return
        else:
            QMessageBox.warning(self, "Hata", "Hesaplama yapılmadan kayıt yapılamaz!")

        try:
            with sqlite3.connect("neturun.db") as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT urunadi,birimfiyati FROM TumUrunler")
                urunler = cursor.fetchall()

                for i,j in urunler:

                    if i == f"{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}":
                        if self.gram and self.milyem:
                            cursor.execute(f"SELECT urungrami FROM TumUrunler WHERE urunadi='{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}'")
                            urungrami = cursor.fetchall()

                            try:
                                kayit = float(urungrami[0][0]) + float(self.ui.lineAtolyeGramHas.text())
                            except:
                                kayit = float(self.ui.lineAtolyeGramHas.text())

                            cursor.execute(f"UPDATE TumUrunler SET urungrami={kayit} WHERE urunadi='{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}'")
                            connect.commit()

                            self.ui.lineAtolyeGramHas.clear()
                            self.ui.lineAtolyeMilyemAdet.clear()
                            self.ui.lineAtolyeHasKarsiligi.clear()
                            self.ui.line_AtolyeAlinanYeniUrun.clear()
                            return

                        if self.has and self.adet:
                            cursor.execute(f"SELECT urunadeti FROM TumUrunler WHERE urunadi='{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}'")
                            urunadeti = cursor.fetchall()

                            try:
                                kayit = float(urunadeti[0][0]) + float(self.ui.lineAtolyeGramHas.text())
                            except:
                                kayit = float(self.ui.lineAtolyeGramHas.text())

                            cursor.execute(f"UPDATE TumUrunler SET urunadeti={kayit} WHERE urunadi='{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}'")
                            connect.commit()

                            self.ui.lineAtolyeGramHas.clear()
                            self.ui.lineAtolyeMilyemAdet.clear()
                            self.ui.lineAtolyeHasKarsiligi.clear()
                            self.ui.line_AtolyeAlinanYeniUrun.clear()
                            return

                if self.gram and self.milyem:
                    cursor.execute(f"INSERT INTO TumUrunler(urunadi,urungrami,birimfiyati) VALUES('{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}',{float(self.ui.lineAtolyeGramHas.text())},{float(self.ui.lineAtolyeMilyemAdet.text())})")
                    connect.commit()

                if self.has and self.adet:
                    cursor.execute(f"INSERT INTO TumUrunler(urunadi,urunadeti,birimfiyati) VALUES('{self.kaydedilecekurun} {float(self.ui.lineAtolyeMilyemAdet.text())} {self.atolyeadi}',{float(self.ui.lineAtolyeGramHas.text())},{float(self.ui.lineAtolyeMilyemAdet.text())})")
                    connect.commit()

                self.ui.lineAtolyeGramHas.clear()
                self.ui.lineAtolyeMilyemAdet.clear()
                self.ui.lineAtolyeHasKarsiligi.clear()
                self.ui.line_AtolyeAlinanYeniUrun.clear()
                return

        except:
            pass


    #YENİLE BUTONU
    def atolyeListesiYenile(self):

        # ATÖLYE İSİMLERİ FETCH EDİLİYOR
        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT adi FROM TumAtolyeler")
            self.atolyeler = self.cursor.fetchall()

        self.bosliste = []
        for i in self.atolyeler:
            self.bosliste += i

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model = QStandardItemModel(len(self.atolyeler), 1)
        self.model.setHorizontalHeaderLabels(['Atölyeler'])

        for row, musteri in enumerate(self.bosliste):
            item = QStandardItem(musteri)
            self.model.setItem(row, 0, item)

        self.filterProxyModel = QSortFilterProxyModel()
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit_Arama.textChanged.connect(self.filterProxyModel.setFilterRegExp)
        self.ui.tableView_Atolyeler.setModel(self.filterProxyModel)
        self.ui.tableView_Atolyeler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def tarihGoster(self):
        tarih = self.ui.calendarWidget_Takvim.selectedDate().getDate()
        self.tarih = f"{tarih[0]}.{tarih[1]}.{tarih[2]}"


    def odemeUrunleri(self):


        with sqlite3.connect("nethurda.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT urunadi,urungrami,urunadeti,nakit FROM TumHurdalar")
            odemeUrunleri = cursor.fetchall()

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model1 = QStandardItemModel(len(odemeUrunleri), 2)
        self.model1.setHorizontalHeaderLabels(['Ürünler','Miktarı'])


        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model1)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit.textChanged.connect(filterProxyModel.setFilterRegExp)
        self.ui.tableView.setModel(filterProxyModel)
        self.ui.tableView.setColumnWidth(0,165)

        sayac = 0
        for i,j,k,m in odemeUrunleri:
            if j != 0 and k!=0 and m!=0:
                if k == None and m==None:
                    self.model1.setItem(sayac,0,QStandardItem(i))
                    self.model1.setItem(sayac,1,QStandardItem(str(j)+" Gram"))
                    sayac +=1
                if j == None and m==None:
                    self.model1.setItem(sayac,0,QStandardItem(i))
                    self.model1.setItem(sayac,1,QStandardItem(str(k) + " Adet"))
                    sayac+=1
                if j == None and k == None:
                    self.model1.setItem(sayac, 0, QStandardItem(i))
                    self.model1.setItem(sayac,1,QStandardItem(str(m) +" TL"))
                    sayac += 1
        return

    def IadeOdemeUrunleri(self):

        self.atolyeadi = self.ui.tableView_Atolyeler.currentIndex().model().itemData(self.ui.tableView_Atolyeler.currentIndex()).get(0)

        with sqlite3.connect("nethurda.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT urunadi,urungrami,urunadeti,nakit FROM TumHurdalar")
            odemeUrunleri = cursor.fetchall()
        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT tarih,odemeurunu,odemeurungram,odemeurunhas,odemenakitmiktari FROM '{self.atolyeadi}'")
            alinanHurdalar = cursor.fetchall()
        try:
            iadeHurdalar= []
            for n,i,j,k,m in alinanHurdalar:
                if n>self.tarih:
                    if i != None:
                        iadeHurdalar.append(i)
        except AttributeError:
            tarih = str(datetime.date.today())
            tarih = tarih.split("-")
            tarih0 = f"{tarih[0]}.{tarih[1]}.{tarih[2]}"
            iadeHurdalar = []
            for n, i, j, k, m in alinanHurdalar:
                if n > tarih0:
                    if i != None:
                        iadeHurdalar.append(i)

        # FİLTRE İÇİN KULLANILAN MODÜL
        self.model2 = QStandardItemModel(len(iadeHurdalar), 2)
        self.model2.setHorizontalHeaderLabels(['Ürünler','Miktarı'])


        filterProxyModel = QSortFilterProxyModel()
        filterProxyModel.setSourceModel(self.model2)
        filterProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filterProxyModel.setFilterKeyColumn(0)
        self.ui.lineEdit.textChanged.connect(filterProxyModel.setFilterRegExp)
        self.ui.tableView_2.setModel(filterProxyModel)
        self.ui.tableView_2.setColumnWidth(0,165)

        sayac = 0
        try:
            for n,i,j,k,m in alinanHurdalar:
                if n > self.tarih:
                    if j != 0 and k!=0 and m!=0 and i != None:
                        if k == None and m==None:
                            self.model2.setItem(sayac,0,QStandardItem(i))
                            self.model2.setItem(sayac,1,QStandardItem(str(j)+" Gram"))
                            sayac +=1
                        if j == None and m==None:
                            self.model2.setItem(sayac,0,QStandardItem(i))
                            self.model2.setItem(sayac,1,QStandardItem(str(k) + " Adet"))
                            sayac+=1
                        if j == None and k == None:
                            self.model2.setItem(sayac, 0, QStandardItem(i))
                            self.model2.setItem(sayac,1,QStandardItem(str(m) +" TL"))
                            sayac += 1
        except AttributeError:
            tarih = str(datetime.date.today())
            tarih = tarih.split("-")
            tarih0 = f"{tarih[0]}.{tarih[1]}.{tarih[2]}"
            for n,i,j,k,m in alinanHurdalar:
                if n > tarih0:
                    if j != 0 and k!=0 and m!=0 and i != None:
                        if k == None and m==None:
                            self.model2.setItem(sayac,0,QStandardItem(i))
                            self.model2.setItem(sayac,1,QStandardItem(str(j)+" Gram"))
                            sayac +=1
                        if j == None and m==None:
                            self.model2.setItem(sayac,0,QStandardItem(i))
                            self.model2.setItem(sayac,1,QStandardItem(str(k) + " Adet"))
                            sayac+=1
                        if j == None and k == None:
                            self.model2.setItem(sayac, 0, QStandardItem(i))
                            self.model2.setItem(sayac,1,QStandardItem(str(m) +" TL"))
                            sayac += 1


    def sonDurumGoster(self):

        self.ui.comboBoxAtolyeSatinAlinanVarUrun.clear()


        self.atolyeadi =self.ui.tableView_Atolyeler.currentIndex().model().itemData(self.ui.tableView_Atolyeler.currentIndex()).get(0)

        with sqlite3.connect("atolyeler.db") as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT sondurum FROM TumAtolyeler WHERE adi ='{}'".format(self.atolyeadi))
            self.sondurum = self.cursor.fetchall()
            self.connect.commit()
        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT satinalinanurun FROM '{self.atolyeadi}'")
            self.satinalinanurunler = cursor.fetchall()
            connect.commit()
        with sqlite3.connect("atolyeler.db") as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT satinalinanurun FROM '{self.atolyeadi}'")
            self.iadeEdilebilenUrunler = cursor.fetchall()
            connect.commit()

            self.satinalinanurunler = set(self.satinalinanurunler)
            self.iadeEdilebilenUrunler = set(self.iadeEdilebilenUrunler)


        for i in self.satinalinanurunler:
            if i[0] != None:
                self.ui.comboBoxAtolyeSatinAlinanVarUrun.addItem(i[0])



        self.ui.label__SonDurum.setText(str(self.sondurum[0][0]))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GirisEkrani()
    sys.exit(app.exec_())