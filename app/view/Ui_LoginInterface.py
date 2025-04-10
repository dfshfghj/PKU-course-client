# Form implementation generated from reading ui file 'app/view/Ui_login.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LoginInterface(object):
    def setupUi(self, LoginInterface):
        LoginInterface.setObjectName("LoginInterface")
        LoginInterface.resize(701, 501)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginInterface.sizePolicy().hasHeightForWidth())
        LoginInterface.setSizePolicy(sizePolicy)
        LoginInterface.setMinimumSize(QtCore.QSize(700, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(LoginInterface)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = LoginPanelCard(parent=LoginInterface)
        self.widget.setMinimumSize(QtCore.QSize(360, 0))
        self.widget.setMaximumSize(QtCore.QSize(360, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exitButton = TransparentPushButton(parent=self.widget)
        self.exitButton.setText("")
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout_2.addWidget(self.exitButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.PKULogoLabel = QtWidgets.QLabel(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PKULogoLabel.sizePolicy().hasHeightForWidth())
        self.PKULogoLabel.setSizePolicy(sizePolicy)
        self.PKULogoLabel.setText("")
        self.PKULogoLabel.setPixmap(QtGui.QPixmap(":/images/icons/PKUFull_black.svg"))
        self.PKULogoLabel.setScaledContents(False)
        self.PKULogoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PKULogoLabel.setObjectName("PKULogoLabel")
        self.verticalLayout.addWidget(self.PKULogoLabel)
        self.usernameLabel = BodyLabel(parent=self.widget)
        self.usernameLabel.setMinimumSize(QtCore.QSize(360, 0))
        self.usernameLabel.setObjectName("usernameLabel")
        self.verticalLayout.addWidget(self.usernameLabel)
        self.usernameEdit = LineEdit(parent=self.widget)
        self.usernameEdit.setClearButtonEnabled(True)
        self.usernameEdit.setObjectName("usernameEdit")
        self.verticalLayout.addWidget(self.usernameEdit)
        self.passwordLabel = BodyLabel(parent=self.widget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.verticalLayout.addWidget(self.passwordLabel)
        self.passwordEdit = LineEdit(parent=self.widget)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordEdit.setClearButtonEnabled(True)
        self.passwordEdit.setObjectName("passwordEdit")
        self.verticalLayout.addWidget(self.passwordEdit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.checkBox = CheckBox(parent=self.widget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.pushButton = PrimaryPushButton(parent=self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout.addWidget(self.widget)
        spacerItem5 = QtWidgets.QSpacerItem(313, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)

        self.retranslateUi(LoginInterface)
        QtCore.QMetaObject.connectSlotsByName(LoginInterface)

    def retranslateUi(self, LoginInterface):
        _translate = QtCore.QCoreApplication.translate
        LoginInterface.setWindowTitle(_translate("LoginInterface", "Form"))
        self.usernameLabel.setText(_translate("LoginInterface", "用户名"))
        self.passwordLabel.setText(_translate("LoginInterface", "密码"))
        self.passwordEdit.setPlaceholderText(_translate("LoginInterface", "••••••••••••"))
        self.checkBox.setText(_translate("LoginInterface", "记住密码"))
        self.pushButton.setText(_translate("LoginInterface", "登录"))
from ..components.card import LoginPanelCard
from qfluentwidgets import BodyLabel, CheckBox, LineEdit, PrimaryPushButton, TransparentPushButton
