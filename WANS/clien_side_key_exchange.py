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

## Function to run the shell commands
def exec_shell_cmd(cmd):
    import subprocess
    output = subprocess.Popen(cmd, shell=True)
    return output


## This function will generate the client's private key and public key
def generate_client_keys():


    path = os.getcwd() + "/"
    if os.path.exists('{path}client_private_key.pem'.format(path=path)):
        pass
    else:
        exec_shell_cmd('openssl genrsa -out {path}client_private_key.pem 2048'.format(path=path))
        #This command generates a 2048-bit RSA private key in the file `client_private_key.pem`.
        sleep(10)

        #To generate a public key from the private key:
    
        exec_shell_cmd('openssl rsa -pubout -in {path}client_private_key.pem -out {path}client_public_key.pem'.format(path=path))
        sleep(10)
    
        #This command generates the corresponding public key and saves it in the file `client_public_key.pem`.
    return path
    
## This function will exchange the keys, will receive the server's public key and send the client's public key
def client_side_exchange():
    path = generate_client_keys()
# Load client RSA keys generated with OpenSSL
    full_path = path + "client_private_key.pem"
    with open(full_path, "rb") as key_file:
        client_private_key = RSA.import_key(key_file.read())
    full_path = path + "client_public_key.pem"
    with open(full_path, "rb") as key_file:
        client_public_key = RSA.import_key(key_file.read())

    
    client_sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_sockets.connect(('localhost', 65432))

    # Receive server's public key
    server_public_key = RSA.import_key(client_sockets.recv(4096))
    
    # Send client's public key to the server
    client_sockets.sendall(client_public_key.export_key())
    print("\n")
    
    client_sockets.close()
    
    del client_sockets
   
    print("")

    return server_public_key, client_private_key
