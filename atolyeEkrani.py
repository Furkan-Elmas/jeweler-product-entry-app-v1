# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'atolyeEkrani.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_AtolyeEkrani(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(468, 379)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 431, 331))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSatinAl = QtWidgets.QPushButton(self.layoutWidget)
        self.btnSatinAl.setObjectName("btnSatinAl")
        self.verticalLayout.addWidget(self.btnSatinAl)
        self.btnGuncelDurum = QtWidgets.QPushButton(self.layoutWidget)
        self.btnGuncelDurum.setObjectName("btnGuncelDurum")
        self.verticalLayout.addWidget(self.btnGuncelDurum)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnEkleSil = QtWidgets.QPushButton(self.layoutWidget)
        self.btnEkleSil.setObjectName("btnEkleSil")
        self.verticalLayout.addWidget(self.btnEkleSil)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Atölye İşlemleri"))
        self.label.setText(_translate("Form", "Hangi işlemi yapmak istiyorsunuz:"))
        self.btnSatinAl.setText(_translate("Form", "Satın Alma/İade/Ödeme Girişi"))
        self.btnGuncelDurum.setText(_translate("Form", "Güncel Durumu Öğren"))
        self.btnEkleSil.setText(_translate("Form", "Atölye Ekle/Sil"))
