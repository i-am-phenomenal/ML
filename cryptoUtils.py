from cryptography.fernet import Fernet

def generateKey(): 
    key = Fernet.generate_key()
    with open("secret1.key", "wb") as keyFile: 
        keyFile.write(key)

def loadKey():
    return open("secret1.key", "rb").read()

def encryptMessage(email, password): 
    key=loadKey()
    encodedMail = email.encode()
    f = Fernet(key)
    encryptedMail = f.encrypt(encodedMail)
    encodedPass = password.encode()
    encryptedPass = f.encrypt(encodedPass)
    with open("emailCreds.txt", "wb") as file: 
        file.write(encryptedMail)
        file.write("\n".encode("utf-8"))
        file.write(encryptedPass)
    return [encryptedMail, encryptedPass]

def decryptMessage(email, password):
    key = loadKey()
    f = Fernet(key)
    email = f.decrypt(email)
    password =f.decrypt(password)
    return [email.decode("utf-8"), password.decode("utf-8")]

# generateKey()
# email, password = encryptMessage()
# decryptMessage(email, password)