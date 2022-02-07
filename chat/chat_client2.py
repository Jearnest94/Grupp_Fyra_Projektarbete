import pickle
import socket
import threading
from tkinter import *
from tkinter import simpledialog
from aes import send_message, receive_message


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
LOCALHOST = '127.0.0.1'
port = 9002
user_name_client = 'Dan'
server_user = ''
root = Tk()


def message_dialog():
    rsa = simpledialog.askstring("Input private RSA key", f'Hello {user_name_client}! Enter private RSA')
    with open(f'./rsa_keys/{user_name_client.lower()}_private.pem', 'w') as out_file:
        out_file.write(rsa)


def thread_sending():
    while True:
        client_message = input(f'> ')
        encrypted_message_to_send = send_message(client_message, server_user)
        client_socket.send(encrypted_message_to_send)


def thread_receiving():
    from chat_server import user_name_server
    while True:
        received_message_encrypted = pickle.loads(client_socket.recv(2048))
        plaintext = receive_message(received_message_encrypted, user_name_client)
        print(f'{user_name_server}: {plaintext}')


def main():
    client_socket.connect((LOCALHOST, port))
    print("New client created:")
    global server_user
    server_user = input('Enter name for other chat user: ').lower()
    Button(root, text="RSA", command=message_dialog()).pack
    root.mainloop()
    thread_send = threading.Thread(target=thread_sending)
    thread_receive = threading.Thread(target=thread_receiving)
    thread_send.start()
    thread_receive.start()

if __name__ == '__main__':
    main()

