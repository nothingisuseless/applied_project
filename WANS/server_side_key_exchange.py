## ************************************GROUP 6 ASSIGNMENT************************************************
## ************************************CHAKRAVORTY DEVOPRIYA DEVASHISH************************************************
## ************************************SUMIT MUKHERJEE****************************************************************
## ************************************SOUAGATA DUTTA*****************************************************************
## ************************************VINEET SINHA*******************************************************************
## ************************************VIJAY KUMAR********************************************************************
## ************************************SUNIL SINGH********************************************************************


## Importing the libraries
import os
from time import sleep
import sys
import socket
from Crypto.PublicKey import RSA


## Run the shell commands in python
def exec_shell_cmd(cmd):
    import subprocess
    subprocess.Popen(cmd, shell=True)
    return 0



## This function generates the server private key and public key
def generate_server_keys():

#    exec_shell_cmd('pwd')
    path = os.getcwd() + '/'
    if os.path.exists(path + 'server_private_key.pem'):
        pass
    else:
        exec_shell_cmd('openssl genrsa -out {path}server_private_key.pem 2048'.format(path=path))
        sleep(10)
        #This command generates a 2048-bit RSA private key in the file `server_private_key.pem`.

        #To generate a public key from the private key:
        exec_shell_cmd('openssl rsa -pubout -in {path}server_private_key.pem -out server_public_key.pem'.format(path=path))
        sleep(10)
    #This command generates the corresponding public key and saves it in the file `server_public_key.pem`.
    return path

## This function sends the server's public key and receives client's public key
def server_key_exchange():
    path = generate_server_keys()
	# Load server RSA keys generated with OpenSSL
    full_path = path + "server_private_key.pem"
    with open(full_path, "rb") as key_file:
        server_private_key = RSA.import_key(key_file.read())
    full_path = path + "server_public_key.pem"
    with open(full_path, "rb") as key_file:
        server_public_key = RSA.import_key(key_file.read())

#    print("\nServer's public key is : ", server_public_key)
#    print("\nServer's private key is : ", server_private_key) 
    
    server_sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sockets.bind(('localhost', 65432))
    server_sockets.listen(5)
#    print("Server is listening...")

    conns, addr = server_sockets.accept()
#    print(f"Connected by {addr}")

    # Send server's public key to the client
    conns.sendall(server_public_key.export_key())
#    print("\nPublic key has been sent to client!!!!")

    # Receive client's public key
    client_public_key = RSA.import_key(conns.recv(4096))
    print("\n")
    server_sockets.shutdown(2)
    server_sockets.close()
    conns.shutdown(2)
    conns.close()
    del server_sockets
    del conns
#    print("!!!Success")
    return client_public_key, server_private_key
    
#if __name__ == "__main__":

#    print(server_key_exchange())
