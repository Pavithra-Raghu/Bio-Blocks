import core
import authenticate
import operations
from hexbytes import HexBytes

file = open("/home/sutheesh/Downloads/UTC--2020-02-27T03-05-23.147Z--ff0d1eb74f0864ad203c1a127871f5d6c870a29d")
url = "https://mainnet.infura.io/v3/e544a643f49e43539ee0b2322413ce62"


def start_menu():
	print("MENU")
	print("1.Signup")
	print("2.Login")
	print("3.Exit")
def opsmenu(d):
	print("OPERATIONS")
	print("1.View")
	print("2.Update")
	print("3.logout")
def main():
	cor = core.core(url,file)
	authen = authenticate.Authenticate(cor)
	while True:
		start_menu()
		ch = input("Enter your choise:")
		if ch == '1':
			authen.signup()
		elif ch=='2':
			if authen.login() == True:
				ops = operations.Operations(cor,authen.doctors)
				while True:
					opsmenu(cor.currinfo['cat'])
					ch  = input("Enter your choise:")
					if ch == '1':
						ops.view()
					elif ch == '2':
						ops.update()
					elif ch=='3':
						authen.exit()
						break;
		elif ch =='3':
			authen.exit()
			print("BYE")
			exit(0)
									
if __name__ == '__main__':
	main()
				
			
