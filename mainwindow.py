# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 654)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.selectedPrinterComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.selectedPrinterComboBox.setObjectName("selectedPrinterComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.selectedPrinterComboBox)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelFileLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.labelFileLineEdit.setReadOnly(True)
        self.labelFileLineEdit.setObjectName("labelFileLineEdit")
        self.horizontalLayout.addWidget(self.labelFileLineEdit)
        self.browsePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.browsePushButton.setObjectName("browsePushButton")
        self.horizontalLayout.addWidget(self.browsePushButton)
        self.horizontalLayout.setStretch(0, 1)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.searchPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchPushButton.setObjectName("searchPushButton")
        self.verticalLayout.addWidget(self.searchPushButton)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.total_label = QtWidgets.QLabel(self.centralwidget)
        self.total_label.setObjectName("total_label")
        self.horizontalLayout_3.addWidget(self.total_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.selected_label_total = QtWidgets.QLabel(self.centralwidget)
        self.selected_label_total.setObjectName("selected_label_total")
        self.horizontalLayout_3.addWidget(self.selected_label_total)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.printPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.printPushButton.setObjectName("printPushButton")
        self.horizontalLayout_2.addWidget(self.printPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.printSelectedPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.printSelectedPushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.printSelectedPushButton.setObjectName("printSelectedPushButton")
        self.horizontalLayout_2.addWidget(self.printSelectedPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMySQL_Settings = QtWidgets.QAction(MainWindow)
        self.actionMySQL_Settings.setObjectName("actionMySQL_Settings")
        self.menuFile.addAction(self.actionMySQL_Settings)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fishbowl Label Printer"))
        self.label.setText(_translate("MainWindow", "Printer:"))
        self.selectedPrinterComboBox.setToolTip(_translate("MainWindow", "What Dymo printer to use. This is all printers available."))
        self.label_2.setText(_translate("MainWindow", "Label Template:"))
        self.labelFileLineEdit.setToolTip(_translate("MainWindow", "File path to the .label file to use."))
        self.browsePushButton.setText(_translate("MainWindow", "Browse"))
        self.label_3.setText(_translate("MainWindow", "Manufacture Order #:"))
        self.searchPushButton.setText(_translate("MainWindow", "Search"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "WO Number"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Part Number"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Description"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Total Qty Used"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "BOM Qty"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "UOM"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Label Quantity"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Material Thickness"))
        self.total_label.setText(_translate("MainWindow", "Total Labels: VALUE"))
        self.selected_label_total.setText(_translate("MainWindow", "Selected Total: VALUE"))
        self.printPushButton.setText(_translate("MainWindow", "Print All"))
        self.printSelectedPushButton.setText(_translate("MainWindow", "Print Selected"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionMySQL_Settings.setText(_translate("MainWindow", "MySQL Settings"))
        self.actionMySQL_Settings.setToolTip(_translate("MainWindow", "Settings for connecting to Fishbowls MySQL instance."))
        self.actionMySQL_Settings.setStatusTip(_translate("MainWindow", "Settings for connecting to Fishbowls MySQL instance."))
