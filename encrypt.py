from cryptography.fernet import Fernet
from hashlib import sha512
from binascii import hexlify, unhexlify


class main:
	def __init__(self, userinput, file):
		if userinput["isTrue"]:
			self.input_ = userinput["pw"]
		else:
			self.input_ = str(Fernet.generate_key())[2:-1]


		self.password = sha512(self.input_.encode('utf-8')).hexdigest()


		try:
			key = bytes(self.input_, 'utf-8')
			self.cipher_suite = Fernet(key)
		except:
			print("INVALID KEY")

		self.file = file


	def encrypt(self):
		try:
			with open(self.file, 'rb') as f:
				content = f.read()

			hexValue = hexlify(content)
			cipher_text = self.cipher_suite.encrypt(hexValue)


			with open(self.file+".crypt", 'w') as f:
				f.write(self.password+"\n"+self.file[self.file.rfind(".")+1:]+"\n")

			with open(self.file+".crypt", 'ab') as f:
				f.write(cipher_text)

			with open(self.file+".key.txt", 'w') as f:
				f.write(self.input_)

			print("DONE")
		except:
			print("FAILED")

	def decrypt(self):
		try:
			try:
				with open(self.file+".crypt", 'rb') as f:
					self.content = f.readlines()
			except:
				with open(self.file, 'rb') as f:
					self.content = f.readlines()

			if self.password == str(self.content[0])[2:-5]:
				print("DONE")
				decrypt = self.cipher_suite.decrypt(self.content[2])

				f = open("_out."+str(self.content[1])[2:-5], "wb")
				f.write(unhexlify(decrypt))
				f.close()
			else:
				print("FAILED")
		except NameError:
			print("FAILED", NameError)


def generate(ie):
	i= 0
	while i<ie:
		print(str(Fernet.generate_key())[2:-1])
		i+=1

def commands(arg):
	if len(arg) >= 2:
		if arg[1] == "generate":
			if len(arg) >= 3:
				generate(int(arg[2]))
			else:
				generate(10)
		elif arg[1] == "help":
			msg = (
				'encrypt: encrypt a file.\n'
				'	{x} encrypt $file_name\n'
				'	OR\n'
				'	{x} encrypt $file_name $key\n\n'
				'decrypt: decrypt a file.\n'
				'	{x} decrypt $file_name $key\n\n'
				'generate: generate keys.\n'
				'	{x} generate\n'
				'	OR\n'
				'	{x} generate $nb_of_keys\n\n'
				'help:\n'
				'	{x} help').format(x="encrypt.py")
			print(msg)
		elif arg[1] == "encrypt" or arg[1] == "decrypt":
			if len(arg) >= 4:
				file = main({"isTrue":True,"pw":arg[3]}, arg[2])
			elif len(arg) == 3:
				file = main({"isTrue":False}, arg[2])


			if arg[1] == "encrypt":
				file.encrypt()
			if arg[1] == "decrypt":
				file.decrypt()

if __name__ == "__main__":
	commands(["nothing", "help"])

	from sys import argv
	commands(argv)


	while True:
		input_ = "encrypt.py "
		input_ += input("Enter command:")
		print(input_)
		commands(input_.split())
