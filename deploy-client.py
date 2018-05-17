import tkinter
import os, errno
import shutil
import zipfile
import socket 
from threading import Thread

cwd = os.getcwd()

def disableButton():
	button['state'] = 'disabled'


def enableButton():
	button['state'] = 'normal'

def setStateLabel(state):
	labelState['text'] = state

def doDeploy():
	disableButton()

	proy = entryPro.get()

	try:
		shutil.rmtree("Deploy")
		os.remove('deploy.zip')
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

	setStateLabel("Compiling...")
	os.system("dotnet publish " + proy + " --framework netcoreapp2.0 -r linux-x64 -o " + cwd + "\\Deploy")


	setStateLabel("Zipping...")
	zipf = zipfile.ZipFile('deploy.zip', 'w', zipfile.ZIP_DEFLATED)
	zipdir("Deploy", zipf)
	zipf.close()

	setStateLabel("Sending...")
	send()

	setStateLabel("")
	enableButton()

def zipdir(path, ziph):
	# ziph is zipfile handle
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))

def send():
	s = socket.socket()
	host = entryIp.get()
	port = 12345

	s.connect((host, port))
	f = open('deploy.zip','rb')
	print ('Sending...')
	l = f.read(1024)
	while (l):
	    s.send(l)
	    l = f.read(1024)
	f.close()
	print ("Done Sending")
	s.close

def threading():
	t = Thread(target = doDeploy)
	t.start()
		
top = tkinter.Tk()
top.title("Deploy to linux")
top.geometry("300x200")

button = tkinter.Button(top, text ="Deploy", command = threading)
labelState = tkinter.Label(top, text="")
labelPro = tkinter.Label(top, text="Proyecto")
entryPro = tkinter.Entry(top)
labelIp = tkinter.Label(top, text="Ip linux")
entryIp = tkinter.Entry(top)

entryPro.place(x=100, y=20)
labelPro.place(x=20, y=20)

entryIp.place(x=100, y=60)
labelIp.place(x=20, y=60)

button.place(x=125, y = 100)
labelState.place(x=125, y = 130)

top.mainloop()

