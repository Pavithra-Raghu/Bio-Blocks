from web3 import Web3
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import base64
import sys
from PIL import Image
from pyzbar.pyzbar import decode
from hexbytes import HexBytes
import qrcode
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class core:
	def __init__(self,url,keyfile):
		self.web3 = Web3(Web3.HTTPProvider(url))
		if self.web3.isConnected() is False:
			print("Unable to connect to Ethereum node")
			sys.exit(0)
		key = keyfile.read()
		self.private_key = self.web3.eth.account.decrypt(key,"m0p3d1ng@#$*")
		self.wallet = dict(eval(key))['address']
		self.nonce =0
		self.transaction_id = 0
		self.data = 0
		self.currinfo = {}
		self.currentid = 0
		self.currentbits = ''
		self.userids = []
		self.records = list(eval(open("records").read()))

	def build_transaction(self,data):
		self.nonce = self.get_nonce()
		self.transaction = {'nonce': self.nonce,'to':self.web3.toChecksumAddress(self.wallet), 'value':0,'gas':200000,'gasPrice':self.web3.eth.gasPrice,'data':data}
		self.signed = self.web3.eth.account.signTransaction(self.transaction,self.private_key)
		self.transaction=0
		return self.signed
	def send_transaction(self,data):
		print("\t\t[+]Accessing Blockchain")
		try:
			self.transaction_id = self.web3.eth.sendRawTransaction(data.rawTransaction)
		except:
			print("Error unable to send transaction")
			return None
		return self.transaction_id
	
	def get_transaction(self,transactionid):
		print("[+]Retreiving records")
		transaction = self.web3.eth.getTransaction(transactionid)
		self.data = transaction['input']
		return self.data
	def check_access(self):
		user =  self.data[:4]
		doctor = self.data[4:8]
		cipher = self.data[24:-3]
		if self.currentid  == user or self.currentid == doctor:
			return True
		else:
			return False

	def encryptdata(self,passphrase,record):
		passphrase = passphrase.encode('ascii')
#		print(passphrase)
		self.key = hashlib.sha3_256(passphrase).digest()
		self.iv = Random.new().read(16)
#		print(self.iv)
		cipher = AES.new(self.key,AES.MODE_CBC,self.iv)
		data = cipher.encrypt(pad(record).encode('ascii'))
		print(data)
		return self.iv+data
	
	def decryptdata(self,passphrase,data,iv):
#		print(passphrase)
		key = hashlib.sha3_256(passphrase).digest()
		plain = AES.new(key,AES.MODE_CBC,iv)
		return unpad(plain.decrypt(data))
	def get_nonce(self):
		return self.web3.eth.getTransactionCount(self.web3.toChecksumAddress(self.wallet))
