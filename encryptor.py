"""
*  This module contains methods to encrypt and desencrypt any file given using base64 library to encode and decode file content.
*  In order to avoid any decoding using external tools all files encrypted by this tools will contain a key (given by user) encoded and a default key flag 
*  written in different parts of document doing possible desencrypting them only using this module.
*  Developed by Rodrigo Higareda <rhs_21@hotmail.com>
"""


__authors__ = ['Rodrigo Higareda']
__contact__ = ['rhs_21@hotmail.com']



import base64
import os
import os.path
import shutil
import random



# this key is added to encrypted file to avoid encrypt a file already encrypted
ENCRYPT_FLAG = 'EnCrYpTeD'


class Encrypter:

	
	def __init__(self, path):
		self.path = path
		# get OS temp folder path in order to be used on encyption/desencryption process
		self.tmpPath = os.environ['TMP']


	def __isFile(self):
		return os.path.isfile(self.path)

	
	def __returnLinesNumber(self):
		try:
			with open(self.path, 'rb') as file:
				count = 0 
				for i in file:
					count +=1
				return count
		except IOError:
			return -1
	

	def __getFileName(self):
		return self.path.split('\\')[-1]

	
	def __copyFile(self, source, dest):
		try:
			shutil.copyfile(source, dest)
			os.remove(source)
			return True
		except IOError:
			return False



	def encrypt(self, key):
		tmpFile = os.path.join(self.tmpPath, self.__getFileName())
		try:
			if self.__isFile():
				"""
				# create random numbers in order to put both user key  and encrypted key in different places into encrypted document
				# trying avoid any hack attack 
				"""
				fileLong = self.__returnLinesNumber()
				keyLine = random.randint(0, fileLong)
				alreadyEncryptedKeyLine = random.randint(0, fileLong)
				cLine = 0 
				# read file
				with open(self.path, 'rb') as fd, open(tmpFile, 'wb') as file:
					for line in fd:
						if cLine == keyLine:
							file.write(base64.b64encode(key.encode()) + b'\n')
						if cLine == alreadyEncryptedKeyLine:
							file.write(base64.b64encode(ENCRYPT_FLAG.encode()) + b'\n')
						file.write(base64.b64encode(line) + b'\n')

			return self.__copyFile(tmpFile, self.path)
		except IOError:
			print('Error opening file')
			return False

	
	def desencript(self, key):
		tmpFile = os.path.join(self.tmpPath, self.__getFileName())
		keyEncoded = base64.b64encode(key.encode())
		encryptedKeyEncoded = base64.b64encode(ENCRYPT_FLAG.encode())
		try:
			if self.__isFile():
				with open(self.path, 'rb') as fd, open(tmpFile, 'wb') as file:
					for line in fd:
						if not line == keyEncoded + b'\n' and not line == encryptedKeyEncoded + b'\n':
							file.write(base64.b64decode(line))
				return self.__copyFile(tmpFile, self.path)

		except IOError:
			print('Error opening file')
			return False
