import hashlib
from web3 import Web3
import core
import base64
import os
from hexbytes import HexBytes
import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode

class Authenticate:
	def __init__(self,cor):
		self.cor = cor
		self.f = open("database",'r')
		self.database = list(eval(self.f.read()))
		self.f.close()
		f = open("doctors",'r')
		self.doctors = list(eval(f.read()))
		f.close()
		self.records = self.cor.records
		self.rand = os.open('/dev/urandom',os.O_RDONLY)
		self.access = False
		self.thash = 0
		self.hash = 0


	def signup(self):
		print("\t\tSIGNUP")
		d = input("\t\tDoctor(D) or patient(P)?")
		username = input("\t\tEnter the username:")
		fl =0
		while fl==0:
			userid = os.read(self.rand,4)
			print(userid)
			if len(self.database) == 0:
				break
			for i in self.database:
				id = i['userid']
				print(id)
				if bytes.fromhex(id) != userid:
					fl=1
					break
		fl = 0
		if d == 'p' or d=='P':
			while fl==0:
				doctorname = input("\t\tEnter the attending doctorname:")
				for i in self.doctors:
					if i['doctor'] == doctorname:
						i['patients'].append({'patientid':userid.hex(),'patientname':username})
						fl = 1
						self.cor.records.append({'patientid':userid.hex(),'records': [] })
						f = open('records','w')
						f.write(str(self.cor.records))
						f.close()
						break
				if fl==0:
					print("Doctor name not found")

		random = os.read(self.rand,64)
		hash = hashlib.sha3_256(userid+random).digest()
		transaction = self.cor.build_transaction(hash)
		tid = self.cor.send_transaction(transaction)
		if tid == None:
			print("[-]Unable to signup,error occured")
			return
#		tid = 'AAAAAAAAAAAAAA'
		self.hash = hash
		self.database.append(dict({"userid":userid.hex(),"cat":d,"info":dict({"username":username,"trid":tid})}))
		if d=='D' or d=='d':
			self.doctors.append({'doctor':username,'id':userid.hex(),'patients':[]})

		print("Your Signup Successfull");
		print("Your User Id:",userid.hex());
		print("Your 64byte random id:",random.hex())
		print("Your Qrcode image path:",self.encode_qrcode(random))
		f = open("database",'w')
		f.write(str(self.database))
		f.close()
		f = open('doctors','w')
		f.write(str(self.doctors))
		f.close()
	
	def login(self):
		print("\t\tLOGIN")
		userid = bytes.fromhex(input("\t\tEnter the userid:"));
		path = input("\t\tEnter the path of QR code image:")
		rand = self.decode_qrcode(path)
		if self.check_hash(userid,rand) == True:
			self.access = True
			self.cor.currentid = userid.hex()
			print("Autentication successful")
		else:
			self.access = False
			print("Authentication denied")
		return self.access
	def check_hash(self,userid,rand):
		tid = 0
		for i in self.database:
			if bytes.fromhex(i['userid']) == userid:
				tid = i['info']['trid']
				self.cor.currinfo = i
		print(tid)
		hash = hashlib.sha3_256(userid+rand).digest()
		thash = self.cor.get_transaction(tid)
		thash = bytes.fromhex(thash[2:])
		self.thash = thash
		if self.thash == hash:
			return True
		else:
			return False
	def exit(self):
		f = open('database','w')
		f.write(str(self.database))
		f.close()
		f = open('doctors','w')
		f.write(str(self.doctors))
		f.close()
		f = open('records','w')
		f.write(str(self.cor.records))
		f.close()
	def encode_qrcode(self,data):
		path  = "/home/sutheesh/workout/blockchain/auth.png"
		qr = pyqrcode.create(data.hex())
		qr.png(path,scale=6)
		return path
	
	def decode_qrcode(self,path):
		data = decode(Image.open(path))
		return data[0].data
