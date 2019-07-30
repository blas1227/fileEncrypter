"""
*  This module is used for testing purposes and will be deleted on release version
*
*
*  Developed by Rodrigo Higareda <rhs_21@hotmail.com>
"""


__authors__ = ['Rodrigo Higareda']
__contact__ = ['rhs_21@hotmail.com']



import encryptor



# file = encryptor.Encrypter('C:\\Users\\uib58279\\Desktop\\tutorials\\python\\Urllib - GET Requests  Python Tutorial  Learn Python Programming.mp4')
# file = encryptor.Encrypter('C:\\Users\\uib58279\\Desktop\\tutorials\\ubuntu-18.04.2-desktop-amd64.iso')
file =encryptor.Encrypter('C:\\Users\\uib58279\\Desktop\\tutorials\\toEncrypt') 
print('Encrypting......')
if file.encrypt('rodrigo123'):
	print('File Encrypted properly')
input('Press any key to continue.....')
print('Desencrypting.....')
if file.desencript('rodrigo123'):
	print('File desencripted properly')