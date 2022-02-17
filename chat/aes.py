import os.path
import pickle
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP




def aes_encrypt(message):
    key = get_random_bytes(16)
    cipher_aes = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode('utf-8'))
    return key, ciphertext, cipher_aes.nonce, tag


def aes_decrypt(aes_key, ciphertext, nonce, tag):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
    decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode('utf-8')


def rsa_encrypt(user, message):
    recipient_key = RSA.importKey(open(f'./rsa_keys/{user}_public.pem').read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    return cipher_rsa.encrypt(message)


def rsa_decrypt(cipher, user):
    recipient_key = RSA.importKey(open(f'./rsa_keys/{user}_private.pem').read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    return cipher_rsa.decrypt(cipher)


def encrypt_message(message, user):
    aes_key, aes_cipher, aes_nonce, aes_tag = aes_encrypt(message)
    encrypted_aes_key = rsa_encrypt(user, aes_key)
    return (encrypted_aes_key, aes_nonce, aes_tag, aes_cipher)


def decrypt_message(user, encrypted_aes_key, aes_nonce, aes_tag, aes_cipher):
    aes_key = rsa_decrypt(encrypted_aes_key, user)
    plaintext = aes_decrypt(aes_key, aes_cipher, aes_nonce, aes_tag)
    return plaintext


def receive_message(received_message_encrypted, user):
    encrypted_aes_key = received_message_encrypted['encryptedAesKey']
    aes_nonce = received_message_encrypted['aesNonce']
    aes_tag = received_message_encrypted['aesTag']
    aes_cipher = received_message_encrypted['aesCipher']
    plaintext = decrypt_message(user, encrypted_aes_key, aes_nonce, aes_tag, aes_cipher)
    return plaintext


def send_message(client_message, user):
    encrypted_aes_key, aes_nonce, aes_tag, aes_cipher = encrypt_message(client_message, user)
    data_to_send = {
        'encryptedAesKey': encrypted_aes_key,
        'aesNonce': aes_nonce,
        'aesTag': aes_tag,
        'aesCipher': aes_cipher
    }
    data_to_send = pickle.dumps(data_to_send)
    return data_to_send

