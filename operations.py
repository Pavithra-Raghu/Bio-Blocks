import core
import authenticate
from hexbytes import HexBytes
import time
import hashlib

class Operations:
	def __init__(self,cor,doctors):
		self.cor = cor
		self.cat = 0
		self.doctors = doctors
		self.doctor = 0
		self.flag = 0
		

	def view(self):
		self.cat = self.cor.currinfo['cat']
		if len(self.cor.records) == 0:
			print("[-]No records to view")
			return False
		if self.flag == 0:
			if self.cat == 'd' or self.cat == 'D':
				for i in self.doctors:
					if i['id'] == self.cor.currentid:
						self.doctor = i
						self.flag  =1
						break
				if self.doctor == 0:
					print("[-]Doctor Id unknown")


		rec = 0
		print("[+]Records",self.cor.records)
		if self.cat == 'd' or self.cat == 'D':
			ch = input("Enter the patientname:")
			for i in self.doctor['patients']:
				for j in self.cor.records:
					if j['patientid'] ==  i['patientid']:
						rec = j['records']
						id = i['patientid']
						break
				if rec !=0:
					break
		else:
			for i in self.cor.records:
				if i['patientid'] == self.cor.currentid:
					rec = i['records']
					break
		if len(rec) == 0:
			print("[-] No records to view")
			return False
		else:
			for i in rec:
				data = self.cor.get_transaction(i)
				print(len(data))
				data = data[2:]
				data = bytes.fromhex(data)
				patient = data[:8]
				print(patient)
				doct = data[8:16]
				print(doct)
				iv = data[16:32]
				print("IV:",len(iv))
				record = self.cor.decryptdata(doct+patient,data[32:],iv)
				print("\t\t",record)
				print("\t\tRecord hash:",hashlib.sha3_256(record).digest().hex())
				
	def update(self):
		self.cat = self.cor.currinfo['cat']
		rec = 0
		id = 0
		if self.flag == 0:
			if self.cat == 'd' or self.cat == 'D':
				for i in self.doctors:
					if i['id'] == self.cor.currentid:
						self.doctor = i
						self.flag = 1
						break
				if self.doctor == 0:
					print("[-]Doctor Id unknown")

	
		if self.cat == 'd' or self.cat == 'D':
			name = input("Enter the patientname:")
			for i in self.doctor['patients']:
				if i['patientname'] == name:
					id = i['patientid']
					break
			if id == 0:
				print("[-]Id not found")
				return False
			data = input("Enter the new Record:")
			cipher = self.cor.encryptdata(self.doctor['id']+id,data)
#	print("cipher len:",len(cipher))
#			print("Cipher:",HexBytes(cipher))
			signed = self.cor.build_transaction(id.encode('ascii')+self.doctor['id'].encode('ascii')+cipher)
			tid = self.cor.send_transaction(signed)
			if tid == None:
				print("[-]Previous transaction not mined yet,Try after some time")
				return False
			for i in self.cor.records:
#				print(i['patientid'])
				if i['patientid'] == id:
					print(self.cor.records)
					i['records'].append(tid)
					print("[+]Record Updated")
					print(self.cor.records)
					f = open("records",'w')
					f.write(str(self.cor.records))
					f.close()
					break
			return True
		else:
			print("[-]You dont have permission to update records")
			return False
