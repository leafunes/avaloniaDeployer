import os, errno
import shutil
import socket               # Import socket module
import zipfile
import subprocess
from multiprocessing import Process

cwd = os.getcwd()
dllFile = "AvaloniaPOC.dll"

def createFile():
	try:
		os.remove('deploy.zip')
		shutil.rmtree('Deploy')
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

	fl = open('deploy.zip','wb')
	return fl

def unzip():
	zipf = zipfile.ZipFile('deploy.zip', 'r')
	zipf.extractall('.')
	zipf.close()

def shell():
	subprocess.call(['dotnet', cwd + "/Deploy/" + dllFile])

def execute():
	return subprocess.Popen('dotnet ' + cwd + "/Deploy/" + dllFile, shell = True)
	#p = Process(target=shell)
	#p.start()
	#return p

def terminate(proc):
	if(proc is not None):
		print("Terminar")
		proc.terminate()

s = socket.socket()
host = "0.0.0.0"
port = 12345
s.bind((host, port))
s.listen(1)
p = None

while True:
	c, addr = s.accept()
	print "Receiving..."
	l = c.recv(1024)
	terminate(p)
	f = createFile()
	while (l):
		f.write(l)
		l = c.recv(1024)
	f.close()
	print "Done Receiving"
	c.close()
	unzip()
	p = execute()