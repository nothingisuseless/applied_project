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
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode





def start_client():
    ## THIS IS CALLING A DIFFERENT FILE WHICH GENERATES THE PUBLIC KEYS USING OPENSSL AND EXCHANGING THE PUBLIC KEYS
    from clien_side_key_exchange import client_side_exchange
    server_public_key, client_private_key = client_side_exchange()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sleep(10)
#    print("Here")
    client_socket.connect(('localhost', 11564))


    # Receive server's public key
#    server_public_key = RSA.import_key(client_socket.recv(4096))

    client_hello = 'HELLO!!!!'
    encode_client_hello = client_hello.encode("utf-8")
    print("===========CLIENT===============", encode_client_hello, "\n")
    client_socket.sendall(encode_client_hello)
    print("\n")

    server_ackn = client_socket.recv(40)
    decode_server_ackn = server_ackn.decode("utf-8")
    print("===========SERVER===============", decode_server_ackn, "\n")



    client_ack = "ACK!!!!"
    encode_client_ack = client_ack.encode("utf-8")
    print("===========CLIENT===============", encode_client_ack, "\n")
    client_socket.sendall(encode_client_ack)
    print("\n")

#    exit(0)


#    client_ack = "Ack!!!!"
    
#    client_socket.sendall(client_ack.encode("utf-8"))
    
    
    # Send client's public key to the server
#    client_socket.sendall(client_public_key.export_key())
#    print("\nPublic key is of ", sys.getsizeof(client_public_key), " bytes!!!!")
#    print("\nPublic key has been sent to server!!!!")
    
    # Generate AES session key
    session_key = os.urandom(16)
    
    # Encrypt the session key with the server's public key
    cipher_rsa = PKCS1_OAEP.new(server_public_key)
    encrypted_session_key = cipher_rsa.encrypt(session_key)
#    print("\nEncrypted session key is of ", sys.getsizeof(encrypted_session_key), " bytes!!!!")
    client_socket.sendall(encrypted_session_key)
    print("===========CLIENT===============", encrypted_session_key, "\n")
#    print("SESSION KEY SIZE ", sys.getsizeof(encrypted_session_key))
    print("\nSession key sent!!!!")

    # Now, let's send an encrypted and signed message to the server
    message = "This is a secret message"
    print("===============MESSAGE ", message, "\n")
    
    # Encrypt the message using the session key
    #print("===============STEP1a\n")
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    #print("===============STEP1b\n")
    nonce = cipher_aes.nonce 
    #print("===============NONCE ", nonce, "\n")
    encoded_message = message.encode("utf-8")
    #print("===============EM ", encoded_message, "\n")
    ciphertext, tag = cipher_aes.encrypt_and_digest(encoded_message)
    #print("===============STEP1c\n")
    encrypted_message = nonce + ciphertext
    

    #sending encrypted message
    client_socket.sendall(encrypted_message)
    #print("==============ENCRYPTED MESSAGE ", encrypted_message, "\n")
#    print("\nEncrypted message is of ", sys.getsizeof(encrypted_message), " bytes!!!!")
    # Sign the message
    h = SHA256.new(message.encode('utf-8'))
    signature = pkcs1_15.new(client_private_key).sign(h)
#    print(sys.getsizeof(signature))
#    print("Signature is : ", signature)
    
    # Send the encrypted message and the signature to the server
    #client_socket.sendall(encrypted_message)
    client_socket.sendall(signature)
#    print("\nSignature is of ", sys.getsizeof(signature), " bytes!!!!")
    #print("===========CLIENT===============", signature, "\n")
#    print("\nSignature has been sent!!!!")

    
    
    client_close = "CLOSE!!!!"
    client_socket.sendall(client_close.encode("utf-8"))
    print("\n===========CLIENT CLOSE===============")
     
    client_socket.close()
    del client_socket
    exit(0)

if __name__ == "__main__":
#    generate_client_keys()
    start_client()
