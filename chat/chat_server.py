import pickle
import socket
import threading
from tkinter import *
from tkinter import simpledialog
from aes import receive_message, send_message

HOST = '127.0.0.1'
PORT = 9002
ADDR = (HOST, PORT)
user_name_server = 'Bob'
client_user = ''
root = Tk()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def message_dialog():
    rsa = simpledialog.askstring("Input private RSA key", f'Hello {user_name_server}! Enter private RSA')
    with open(f'./rsa_keys/{user_name_server.lower()}_private.pem', 'w') as out_file:
        out_file.write(rsa)


def thread_receiving(client, addr):
    from chat_client2 import user_name_client
    while True:
        received_message_encrypted = pickle.loads(client.recv(2048))
        plaintext = receive_message(received_message_encrypted, user_name_server)
        print(f'{user_name_client}: {plaintext}')


def main():
    global client_user
    client_user = input('Enter name for other chat user: ').lower()
    Button(root, text="RSA", command=message_dialog()).pack
    root.mainloop()
    print("Server started")
    server_socket.bind(ADDR)
    server_socket.listen()
    client, addr = server_socket.accept()

    while True:
        thread_receive = threading.Thread(target=thread_receiving, args=(client, addr))
        thread_receive.start()
        client_message = input(f'> ')
        encrypted_message_to_send = send_message(client_message, client_user)
        client.send(encrypted_message_to_send)

if __name__ == '__main__':
    main()
