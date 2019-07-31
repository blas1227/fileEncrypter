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


	def __encryptIt(self, key, file=None):
		if not file:
			file = self.path
		else:
			file = os.path.join(self.path, file)
		if not self.__isEncrypted(file):
			"""
			# create random numbers in order to put both user key  and encrypted key in different places into encrypted document
			# trying avoid any hack attack 
			"""
			fileLong = self.__returnLinesNumber(file)
			keyLine = random.randint(0, fileLong)
			alreadyEncryptedKeyLine = random.randint(0, fileLong)
			cLine = 0
			tmpFile = os.path.join(self.tmpPath, self.__getFileName(file))
			# read file
			with open(file, 'rb') as fd, open(tmpFile, 'wb') as tempFile:
				# Writes default encrypted key in the beginning of file in order to identify whether or not is encrypted
				tempFile.write(base64.b64encode(ENCRYPT_FLAG.encode()) + b'\n')
				for line in fd:
					if cLine == keyLine:
						tempFile.write(base64.b64encode(key.encode()) + b'\n')
					tempFile.write(base64.b64encode(line) + b'\n')
					cLine += 1

			return self.__copyFile(tmpFile, file)
		else:
			print('file its already encrypted using this module')
			return False


	def __desencryptIt(self, key, file=None):
		if not file:
			file = self.path
		else:
			file = os.path.join(self.path, file)
		if self.__isEncrypted(file):
			tmpFile = os.path.join(self.tmpPath, self.__getFileName(file))
			keyEncoded = base64.b64encode(key.encode())
			encryptedKeyEncoded = base64.b64encode(ENCRYPT_FLAG.encode())
			if self.__isRightKey(file, key):
				with open(file, 'rb') as fd, open(tmpFile, 'wb') as tempFile:
					for line in fd:
						if not line == keyEncoded + b'\n' and not line == encryptedKeyEncoded + b'\n':
							tempFile.write(base64.b64decode(line))
				return self.__copyFile(tmpFile, file)
			else:
				print('Key inserted its not correct')
				return False
		else:
			print('This file its not encrypted or not was encrypted using this module')
			return False


	def __isFile(self):
		return os.path.isfile(self.path)


	def __isDir(self):
		return os.path.isdir(self.path)


	def __returnLinesNumber(self, file):
		try:
			with open(file, 'rb') as fd:
				count = 0 
				for i in fd:
					count +=1
				return count
		except IOError:
			return -1
	

	def __getFileName(self, file):
		return file.split('\\')[-1]

	
	def __copyFile(self, source, dest):
		try:
			shutil.copyfile(source, dest)
			os.remove(source)
			return True
		except IOError:
			return False


	""" Returns True if the file was encrypted using this module otherwise return False """
	def __isEncrypted(self, file):
		try:
			with open(file, 'rb') as fd:
				firstLine = fd.readline()
				return True if base64.b64decode(firstLine) == ENCRYPT_FLAG.encode() else False
		except base64.binascii.Error:
			""" This exception occurrs when module is trying to decode a file not encrypted """
			return False


	""" Returns True if the key inserted is correct otherwise return False """
	def __isRightKey(self, file, key):
		with open(file, 'rb') as fd:
			for line in fd:
				if base64.b64decode(line) == key.encode():
					return True
			return False


	def encrypt(self, key):
		try:
			if self.__isFile():
				return self.__encryptIt(key)
			elif self.__isDir():
				for element in os.listdir(self.path):
					if not self.__encryptIt(key, file=element):
						return False
				return True
		except IOError:
			print('Error opening file')
			return False


	def desencript(self, key):
		try:
			if self.__isFile():
				return self.__desencryptIt(key)
			elif self.__isDir():
				for element in os.listdir(self.path):
					if not self.__desencryptIt(key, file=element):
						return False
			return True
		except IOError:
			print('Error opening file')
			return False
