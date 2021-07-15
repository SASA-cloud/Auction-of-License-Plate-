# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msgdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import server_message

class Ui_Dialog(object):
    def setupUi(self, Dialog,server):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.msg_groupbox = QtWidgets.QGroupBox(Dialog)
        self.msg_groupbox.setGeometry(QtCore.QRect(40, 50, 341, 201))
        self.msg_groupbox.setObjectName("msg_groupbox")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.msg_groupbox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 20, 271, 121))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.usernamehl = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.usernamehl.setContentsMargins(0, 0, 0, 0)
        self.usernamehl.setObjectName("usernamehl")
        self.text_label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.text_label.setStyleSheet("QPushButton{\n"
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
        self.text_label.setObjectName("text_label")
        self.usernamehl.addWidget(self.text_label)
        self.msg_text = QtWidgets.QTextEdit(self.horizontalLayoutWidget_3)
        self.msg_text.setObjectName("msg_text")
        self.usernamehl.addWidget(self.msg_text)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.msg_groupbox)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(30, 140, 271, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.usernamehl_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.usernamehl_2.setContentsMargins(0, 0, 0, 0)
        self.usernamehl_2.setObjectName("usernamehl_2")
        self.id_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.id_label.setStyleSheet("QPushButton{\n"
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
        self.id_label.setObjectName("id_label")
        self.usernamehl_2.addWidget(self.id_label)
        self.id_text = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.id_text.setToolTip("")
        self.id_text.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.id_text.setInputMask("")
        self.id_text.setText("")
        self.id_text.setMaxLength(100000)
        self.id_text.setObjectName("id_text")
        self.usernamehl_2.addWidget(self.id_text)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # 绑定事件
        self.buttonBox.accepted.connect(lambda:self.msg_ok_handler(server))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.msg_groupbox.setTitle(_translate("Dialog", "发消息"))
        self.text_label.setText(_translate("Dialog", "消息内容"))
        self.msg_text.setPlaceholderText(_translate("Dialog", "此处可为空（表示只发送当前的拍卖状态）"))
        self.id_label.setText(_translate("Dialog", "接收者id"))
        self.id_text.setWhatsThis(_translate("Dialog", "id"))
        self.id_text.setPlaceholderText(_translate("Dialog", "请输入id（-1表示群发）..."))

    def msg_ok_handler(self,server):
        data = self.msg_text.toPlainText()
        id = int(self.id_text.text())
        server.msg(data=data, bidderID=id)  # 发消息