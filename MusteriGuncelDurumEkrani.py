# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MusteriGuncelDurumEkrani.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_musteriGuncelDurum(object):
    def setupUi(self, musteriGuncelDurum):
        musteriGuncelDurum.setObjectName("musteriGuncelDurum")
        musteriGuncelDurum.resize(1419, 890)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(musteriGuncelDurum.sizePolicy().hasHeightForWidth())
        musteriGuncelDurum.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(musteriGuncelDurum)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(musteriGuncelDurum)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_Arama = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_Arama.setMinimumSize(QtCore.QSize(650, 50))
        self.lineEdit_Arama.setMaximumSize(QtCore.QSize(650, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_Arama.setFont(font)
        self.lineEdit_Arama.setObjectName("lineEdit_Arama")
        self.verticalLayout.addWidget(self.lineEdit_Arama)
        self.tableView_Musteriler = QtWidgets.QTableView(self.tab)
        self.tableView_Musteriler.setMinimumSize(QtCore.QSize(650, 0))
        self.tableView_Musteriler.setMaximumSize(QtCore.QSize(650, 16777215))
        self.tableView_Musteriler.setObjectName("tableView_Musteriler")
        self.verticalLayout.addWidget(self.tableView_Musteriler)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QtWidgets.QFrame.Box)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_bakiye = QtWidgets.QLabel(self.tab)
        self.label_bakiye.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_bakiye.setFont(font)
        self.label_bakiye.setFrameShape(QtWidgets.QFrame.Box)
        self.label_bakiye.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bakiye.setObjectName("label_bakiye")
        self.verticalLayout_3.addWidget(self.label_bakiye)
        self.label_sonsatis = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_sonsatis.setFont(font)
        self.label_sonsatis.setFrameShape(QtWidgets.QFrame.Box)
        self.label_sonsatis.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sonsatis.setObjectName("label_sonsatis")
        self.verticalLayout_3.addWidget(self.label_sonsatis)
        self.label_sonodeme = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_sonodeme.setFont(font)
        self.label_sonodeme.setFrameShape(QtWidgets.QFrame.Box)
        self.label_sonodeme.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sonodeme.setObjectName("label_sonodeme")
        self.verticalLayout_3.addWidget(self.label_sonodeme)
        self.label_soniade = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_soniade.setFont(font)
        self.label_soniade.setFrameShape(QtWidgets.QFrame.Box)
        self.label_soniade.setAlignment(QtCore.Qt.AlignCenter)
        self.label_soniade.setObjectName("label_soniade")
        self.verticalLayout_3.addWidget(self.label_soniade)
        self.label_soniadeodeme = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_soniadeodeme.setFont(font)
        self.label_soniadeodeme.setFrameShape(QtWidgets.QFrame.Box)
        self.label_soniadeodeme.setAlignment(QtCore.Qt.AlignCenter)
        self.label_soniadeodeme.setObjectName("label_soniadeodeme")
        self.verticalLayout_3.addWidget(self.label_soniadeodeme)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout.addWidget(self.radioButton_3)
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.table_alisverisozet1 = QtWidgets.QTableView(self.tab_3)
        self.table_alisverisozet1.setObjectName("table_alisverisozet1")
        self.gridLayout_4.addWidget(self.table_alisverisozet1, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox.setBaseSize(QtCore.QSize(0, 0))
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 3, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 0, 1, 5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 0, 1, 3)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.retranslateUi(musteriGuncelDurum)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(musteriGuncelDurum)

    def retranslateUi(self, musteriGuncelDurum):
        _translate = QtCore.QCoreApplication.translate
        musteriGuncelDurum.setWindowTitle(_translate("musteriGuncelDurum", "M????teri Genel Durum"))
        self.label.setText(_translate("musteriGuncelDurum", "G??ncel Bakiye:"))
        self.label_3.setText(_translate("musteriGuncelDurum", "Son ??r??n sat???? tarihi:"))
        self.label_5.setText(_translate("musteriGuncelDurum", "Son ??deme tarihi:"))
        self.label_7.setText(_translate("musteriGuncelDurum", "Son iade tarihi:"))
        self.label_8.setText(_translate("musteriGuncelDurum", "Son iade edilen ??deme tarihi:"))
        self.label_bakiye.setText(_translate("musteriGuncelDurum", "-"))
        self.label_sonsatis.setText(_translate("musteriGuncelDurum", "-"))
        self.label_sonodeme.setText(_translate("musteriGuncelDurum", "-"))
        self.label_soniade.setText(_translate("musteriGuncelDurum", "-"))
        self.label_soniadeodeme.setText(_translate("musteriGuncelDurum", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("musteriGuncelDurum", "M????teri G??ncel Durum"))
        self.radioButton_3.setText(_translate("musteriGuncelDurum", "Tarihe G??re"))
        self.radioButton_2.setText(_translate("musteriGuncelDurum", "????leme G??re"))
        self.radioButton.setText(_translate("musteriGuncelDurum", "??r??ne G??re"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("musteriGuncelDurum", "Al????veri?? ??zeti"))
        self.label_2.setText(_translate("musteriGuncelDurum", "Y??l:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("musteriGuncelDurum", "??statistik"))
