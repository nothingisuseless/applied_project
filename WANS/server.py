## ************************************GROUP 6 ASSIGNMENT************************************************
## ************************************CHAKRAVORTY DEVOPRIYA DEVASHISH************************************************
## ************************************SUMIT MUKHERJEE****************************************************************
## ************************************SOUAGATA DUTTA*****************************************************************
## ************************************VINEET SINHA*******************************************************************
## ************************************VIJAY KUMAR********************************************************************
## ************************************SUNIL SINGH********************************************************************

import os
from time import sleep
import sys
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15, PKCS1_v1_5 
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

def exec_shell_cmd(cmd):
    import subprocess
    subprocess.Popen(cmd, shell=True)
    return 0



def start_server():
    ## THIS IS CALLING A DIFFERENT FILE WHICH GENERATES THE PUBLIC KEYS USING OPENSSL AND EXCHANGING THE PUBLIC KEYS
    from server_side_key_exchange import server_key_exchange

    client_public_key, server_private_key = server_key_exchange()

    # SOCKET CREATION
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('localhost', 11564))
    server_socket.listen(2)


    conn, addr = server_socket.accept()



    ## RECEIVING CLIENT HELLO
    client_hello = conn.recv(256)
    decode_client_hello = client_hello.decode("utf-8")
    print("===========CLIENT===============", decode_client_hello, "\n")

    ## SENDING HELLO + ACK TO CLIENT
    server_ackn = "Hello+Ack!!!!"
    conn.sendall(server_ackn.encode("utf-8"))
    print("===========SERVER===============", server_ackn, "\n")


    ## RECEIVING CLIENT ACK
    client_ack =  conn.recv(256)
    decode_client_ack = client_ack.decode("utf-8")
    print("===========CLIENT===============", decode_client_ack, "\n")


    


    

    
    # Receive the encrypted AES key from the client
    encrypted_session_key = conn.recv(256)
    print("\n")
#    print("\nEncrypted session key is of ", sys.getsizeof(encrypted_session_key), " bytes!!!!")
#    print("encrypted session key is : ", encrypted_session_key)
    cipher_rsa = PKCS1_OAEP.new(server_private_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    print("\n====================Session key received and decrypted.")
    print('\n==========CLIENT===============', encrypted_session_key, "\n")
    print("===========CLIENT===============", session_key, "\n")

    # Now, let's receive an encrypted and signed message from the client
    encrypted_message = conn.recv(40)
    print("=====================ENCRYPTED MESSAGE STEP 1", encrypted_message)
    print("\n")
#    print("\nEncrypted message is of ", sys.getsizeof(encrypted_message), " bytes!!!!")
    signature = conn.recv(256)
    print("\n")
#    print("\nSignature is of ", sys.getsizeof(signature), " bytes!!!!")
#    print("\nEncrypted Message received is : ", encrypted_message)
#    print("\nSignature is : ", signature)

    # Decrypt the message using the session key
    print("=====================ENCRYPTED MESSAGE", encrypted_message)
    nonce = encrypted_message[:16]
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher_aes.decrypt(encrypted_message[16:])

    
    # Verify the signature using the client's public key
    h = SHA256.new(decrypted_message)
    #print(h)
    try:
#        print("hash value : ", h)
#        print("Ran here fine !!!!")
#       print(pkcs1_15.new(client_public_key))
        pkcs1_15.new(client_public_key).verify(h, signature)
#        print("Ran here fine post ver !!!!")
        print("Signature verified.")
        print("===========CLIENT===============\n")
        print(f"Decrypted message: {decrypted_message.decode('utf-8')}")
    except (ValueError, TypeError):
        print("Signature verification failed.")

    client_close = conn.recv(40)
    decode_client_close = client_close.decode("utf-8")
    print("===========CLIENT===============", decode_client_close, "\n")
    print("\n\n", decode_client_close)

    conn.close()
    server_socket.close()
    
    del conn
    del server_socket
    return 0 

if __name__ == "__main__":

    start_server()
