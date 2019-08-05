"""
* This is a simple User Interface that use encryptor module
"""


import PyQt5.QtWidgets
import encryptor


__authors__=['Rodrigo Higareda']
__contact__=['rhs_21@hotmail.com']


class Window():


    def __init__(self):
        self.__initializeComponents()       


    """ Initiliazes and Draws all windows components needed """
    def __initializeComponents(self):
        self.appContext = PyQt5.QtWidgets.QApplication([])
        self.window = PyQt5.QtWidgets.QWidget()
        self.window.setWindowTitle('Encrypter/Desencrypter tool')
        self.window.setFixedSize(400,200)
        self.pathLabel = PyQt5.QtWidgets.QLabel('Insert Path to Encrypt/Desencrypt:')
        self.pathTextBox = PyQt5.QtWidgets.QLineEdit(readOnly=True)
        self.btnExplore = PyQt5.QtWidgets.QPushButton('...')
        self.pathLabel2 = PyQt5.QtWidgets.QLabel('Insert key to Encypt/Desencrypt:')
        self.pathKeyBox = PyQt5.QtWidgets.QLineEdit()
        self.btnEncrypt = PyQt5.QtWidgets.QPushButton('Encrypt')
        self.btnDesencrypt = PyQt5.QtWidgets.QPushButton('Desencrypt')

        """ Adding components to layout in order to be shown into Window """
        self.layout = PyQt5.QtWidgets.QGridLayout()
        self.layout.addWidget(self.pathLabel, 0, 0)
        self.layout.addWidget(self.pathTextBox, 1, 0)
        self.layout.addWidget(self.btnExplore, 1, 1)
        self.layout.addWidget(self.pathLabel2, 2, 0)
        self.layout.addWidget(self.pathKeyBox, 3, 0)
        self.layout.addWidget(self.btnEncrypt, 4, 1)
        self.layout.addWidget(self.btnDesencrypt, 4, 0)
        self.window.setLayout(self.layout)

        """ Buttons Actions """
        self.btnEncrypt.clicked.connect(self.__encrypt)
        self.btnDesencrypt.clicked.connect(self.__desencrypt)
        self.btnExplore.clicked.connect(self.__browseDirectory)

        """ Draws components """
        self.appContext.setStyle('windowsvista')
        self.window.show()
        self.appContext.exec()


    """ Shows File Dialog window to select file/directory to encrypt/desencrypt """
    def __browseDirectory(self):
        """ Create a new message question  in order to know if user wants to select file or directory """
        msgQuestion = PyQt5.QtWidgets.QMessageBox()
        msgQuestion.setIcon(PyQt5.QtWidgets.QMessageBox.Question)
        msgQuestion.setText('Do you want to encrypt/desencrypt a File?')
        msgQuestion.setWindowTitle('File or Directory?')
        msgQuestion.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Yes | PyQt5.QtWidgets.QMessageBox.No)

        if msgQuestion.exec_() == 16384: # button 'Yes' represents 0x4000 (16384 converted to integer)
            fileDir = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self.window, 'Select File')
            self.pathTextBox.setText(fileDir[0])
        else :
            fileDir = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self.window, 'Select File/Dir')
            self.pathTextBox.setText(fileDir)


    def __encrypt(self):
        self.btnEncrypt.setText('Encrypting.....')
        encrypterObj = encryptor.Encrypter(self.pathTextBox.text().replace('/', '\\'))
        if not encrypterObj.encrypt(self.pathKeyBox.text()):
            self.__showMessage('Error', 'Something went wrong, please verify python console for more details')
        else:
            self.__showMessage('Success', 'Proccess completed!')
        self.btnEncrypt.setText('Encrypt')


    def __desencrypt(self):
        self.btnDesencrypt.setText('Desencrypting....')
        encrypterObj = encryptor.Encrypter(self.pathTextBox.text().replace('/', '\\'))
        if not encrypterObj.desencrypt(self.pathKeyBox.text()):
            self.__showMessage('Error', 'Something went wrong, please verify python console for more details')
        else:
            self.__showMessage('Success', 'Proccess completed!')
        self.btnDesencrypt.setText('Desencrypt')


    def __showMessage(self, title, message):
        msgBox = PyQt5.QtWidgets.QMessageBox()
        if title == 'Error':
            msgBox.setIcon(PyQt5.QtWidgets.QMessageBox.Critical)
        else:
            msgBox.setIcon(PyQt5.QtWidgets.QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.exec_()
