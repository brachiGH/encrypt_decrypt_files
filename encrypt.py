from cryptography.fernet import Fernet
from hashlib import sha512
from binascii import hexlify, unhexlify

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

class main:
	def __init__(self, userinput, file):
		if userinput["isTrue"]:
			self.input_ = userinput["pw"]
		else:
			self.input_ = input('Enter Key: ')


		self.password = sha512(self.input_.encode('utf-8')).hexdigest()


		try:
			key = bytes(self.input_, 'utf-8')
			self.cipher_suite = Fernet(key)
		except:
			print(bcolors.FAIL+"INVALID KEY"+bcolors.ENDC)

		self.file = file


	def encrypt(self):
		try:
			with open(self.file, 'rb') as f:
				content = f.read()

			hexValue = hexlify(content)
			cipher_text = self.cipher_suite.encrypt(hexValue)


			with open(self.file+".crypt", 'w') as f:
				f.write(self.password+"\n"+self.file[:self.file.rfind(".")]+"\n."+self.file[self.file.rfind(".")+1:]+"\n")

			with open(self.file+".crypt", 'ab') as f:
				f.write(cipher_text)

			with open(self.file+".key.txt", 'w') as f:
				f.write(self.input_)

			print(bcolors.OKGREEN+"DONE"+bcolors.ENDC)
		except:
			print(bcolors.FAIL+"FAILED"+bcolors.ENDC)

	def decrypt(self):
		try:
			try:
				with open(self.file+".crypt", 'rb') as f:
					self.content = f.readlines()
			except:
				with open(self.file, 'rb') as f:
					self.content = f.readlines()

			if self.password == str(self.content[0])[2:-5]:
				print(bcolors.OKGREEN+"DONE"+bcolors.ENDC)
				decrypt = self.cipher_suite.decrypt(self.content[3])

				f = open(str(self.content[1])[2:-5]+"_out"+str(self.content[2])[2:-5], "wb")
				f.write(unhexlify(decrypt))
				f.close()
			else:
				print(bcolors.FAIL+"FAILED"+bcolors.ENDC)

		except:
			print(bcolors.FAIL+"FAILED"+bcolors.ENDC)


def generate(ie):
	i= 0
	while i<ie:
		print(str(Fernet.generate_key())[2:-1])
		i+=1

if __name__ == "__main__": 
	from sys import argv

	if len(argv) >= 2:
		if argv[1] == "generate":
			generate(10)
		elif argv[1] == "help":
			msg = (
				'encrypt: encrypt a file.\n'
				'	{x} encrypt {s}$file_name{e}\n'
				'	OR\n'
				'	{x} encrypt {s}$file_name $key{e}\n\n'
				'decrypt: decrypt a file.\n'
				'	{x} decrypt {s}$file_name{e}\n'
				'	OR\n'
				'	{x} decrypt {s}$file_name $key{e}\n\n'
				'generate: generate keys.\n'
				'	{x} generate{e}\n'
				'	OR\n'
				'	{x} generate {s}$nb_of_keys{e}\n\n'
				'help:\n'
				'	{x} help{e}').format(x="encrypt.py"+bcolors.OKGREEN, s=bcolors.WARNING, e=bcolors.ENDC)
			print(msg)
		elif argv[1] == "encrypt" or argv[1] == "decrypt":
			if len(argv) >= 4:
				file = main({"isTrue":True,"pw":argv[3]}, argv[2])
			elif len(argv) == 3:
				file = main({"isTrue":False}, argv[2])


			if argv[1] == "encrypt":
				file.encrypt()
			if argv[1] == "decrypt":
				file.decrypt()