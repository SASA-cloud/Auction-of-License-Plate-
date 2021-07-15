# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openauctiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import server_message

class Ui_openauctiondialog(object):
    def setupUi(self, openauctiondialog,server):
        openauctiondialog.setObjectName("openauctiondialog")
        openauctiondialog.resize(400, 300)
        self.openbuttonbox = QtWidgets.QDialogButtonBox(openauctiondialog)
        self.openbuttonbox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.openbuttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.openbuttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.openbuttonbox.setObjectName("openbuttonbox")
        self.open_groupbox = QtWidgets.QGroupBox(openauctiondialog)
        self.open_groupbox.setGeometry(QtCore.QRect(30, 40, 341, 201))
        self.open_groupbox.setObjectName("open_groupbox")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.open_groupbox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(50, 30, 241, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.usernamehl = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.usernamehl.setContentsMargins(0, 0, 0, 0)
        self.usernamehl.setObjectName("usernamehl")
        self.num_label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.num_label.setStyleSheet("QPushButton{\n"
"background-color: rgb(179, 214, 230);\n"
"color: white;\n"
"border:2px solid #000000;\n"
"padding: 16px 32px;\n"
"text-align: center;\n"
"font-size: 16px;\n"
"margin:4px 2px;\n"
"border-radius: 12px;\n"
"hover{color: black};\n"
"hover{background-color: white};\n"
"hover{border: 2px solid #000000}\n"
"}")
        self.num_label.setObjectName("num_label")
        self.usernamehl.addWidget(self.num_label)
        self.num_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.num_text.setToolTip("")
        self.num_text.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.num_text.setInputMask("")
        self.num_text.setText("")
        self.num_text.setMaxLength(100000)
        self.num_text.setObjectName("num_text")
        self.usernamehl.addWidget(self.num_text)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.open_groupbox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(50, 60, 241, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.userkeyhl = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.userkeyhl.setContentsMargins(0, 0, 0, 0)
        self.userkeyhl.setObjectName("userkeyhl")
        self.num_range_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.num_range_label.setObjectName("num_range_label")
        self.userkeyhl.addWidget(self.num_range_label)
        self.num_range_l_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.num_range_l_text.setObjectName("num_range_l_text")
        self.userkeyhl.addWidget(self.num_range_l_text)
        self.num_range_h_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.num_range_h_text.setObjectName("num_range_h_text")
        self.userkeyhl.addWidget(self.num_range_h_text)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.open_groupbox)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(50, 90, 241, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.userkeyhl_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.userkeyhl_2.setContentsMargins(0, 0, 0, 0)
        self.userkeyhl_2.setObjectName("userkeyhl_2")
        self.floor_price_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.floor_price_label.setObjectName("floor_price_label")
        self.userkeyhl_2.addWidget(self.floor_price_label)
        self.floor_price_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.floor_price_text.setObjectName("floor_price_text")
        self.userkeyhl_2.addWidget(self.floor_price_text)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.open_groupbox)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(50, 120, 241, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.userkeyhl_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.userkeyhl_3.setContentsMargins(0, 0, 0, 0)
        self.userkeyhl_3.setObjectName("userkeyhl_3")
        self.reasonable_price_label = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.reasonable_price_label.setObjectName("reasonable_price_label")
        self.userkeyhl_3.addWidget(self.reasonable_price_label)
        self.price_low_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.price_low_text.setObjectName("price_low_text")
        self.userkeyhl_3.addWidget(self.price_low_text)
        self.price_high_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.price_high_text.setObjectName("price_high_text")
        self.userkeyhl_3.addWidget(self.price_high_text)

        self.retranslateUi(openauctiondialog)
        self.openbuttonbox.accepted.connect(openauctiondialog.accept)
        self.openbuttonbox.rejected.connect(openauctiondialog.reject)
        QtCore.QMetaObject.connectSlotsByName(openauctiondialog)
        # 绑定事件
        self.openbuttonbox.accepted.connect(lambda:self.open_ok_handler(server))

    def retranslateUi(self, openauctiondialog):
        _translate = QtCore.QCoreApplication.translate
        openauctiondialog.setWindowTitle(_translate("openauctiondialog", "Dialog"))
        self.open_groupbox.setTitle(_translate("openauctiondialog", "设定本次拍卖信息"))
        self.num_label.setText(_translate("openauctiondialog", "车牌总数"))
        self.num_text.setWhatsThis(_translate("openauctiondialog", "id"))
        self.num_text.setPlaceholderText(_translate("openauctiondialog", "请输入车牌总数..."))
        self.num_range_label.setText(_translate("openauctiondialog", "车牌范围"))
        self.num_range_l_text.setPlaceholderText(_translate("openauctiondialog", "最小号码..."))
        self.num_range_h_text.setPlaceholderText(_translate("openauctiondialog", "最大号码..."))
        self.floor_price_label.setText(_translate("openauctiondialog", "起拍价  "))
        self.floor_price_text.setPlaceholderText(_translate("openauctiondialog", "请输入起拍价..."))
        self.reasonable_price_label.setText(_translate("openauctiondialog", "合理投标价格区间"))
        self.price_low_text.setPlaceholderText(_translate("openauctiondialog", "最低价..."))
        self.price_high_text.setPlaceholderText(_translate("openauctiondialog", "最高价..."))

    # opennewauction
    def open_ok_handler(self,server):
        server.licence_num = int(self.num_text.text())
        server.licence_range = (int(self.num_range_l_text.text()),
                                int(self.num_range_h_text.text()))
        server.floor_price = int(self.floor_price_text.text())
        server.price_range = [int(self.price_low_text.text()),
                              int(self.price_high_text.text())]

        # 差一个检验输入合理性
        server.open_new_auction()