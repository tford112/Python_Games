'''
Caesar Cipher is a simple exercise in cryptography.
User inputs a message and a key and an encrypted message will be generated.
The key will be a simple one in which there will be a consistent shift of letters.
For example, if the key is 3, then the letter "A" will move 3 spots to the right in the
alphabet and become "D". Numbers also will be shifted to the right; so, 1 becomes 4.

'''
alpha = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
nums = [0, 1, 2 ,3 ,4 ,5 ,6 ,7 ,8, 9]


## Get the user's message and convert into a list and consider integers within list
def getMessage():
    user = list(input("What is the message you want to encrypt?\n"))
    # making sure to account for punctuation while checking for int capability
    punc = [",", "!", "?", ".", "\'", "\"", ""]
    for i in range(len(user)):
        ## Check if integers are in message
        if user[i].isalpha() == False and user[i] != " " and user[i] not in punc:
            user[i] = int(user[i])
    return user

def getKey():
    while True:
        try:
            key = int(input("What kind of key do you want?\n"))
            break
        except ValueError as e:
            print("Sorry, needs to be an integer key. Try again!")
    return key

def encrypt(message, key):
    print("\nEncrypting message")
    for i in range(len(message)):
        if type(message[i]) == int:
            message[i] += key
            message[i] = str(message[i])
        else:
            message[i] = ord(message[i])  ## returns the character into an integer
            message[i] += key    ## shift the integer with the key
            message[i] = chr(message[i])  ## return the character form of the integer
    message = "".join(message)
    encrypted = message.replace("\"", " ")
    return encrypted

def decrypt(message, key):
    print("\nDecrypting message")
    message = list(message)
    for i in range(len(message)):
        if type(message[i]) == int:
            message[i] -= key
            message[i] = str(message[i])
        else:
            message[i] = ord(message[i])
            message[i] -= key
            message[i] = chr(message[i])
    message = "".join(message)
    ## the ord-chr transformation of spaces leads to a strange ' " ' appearing
    return message

def execute():
    message = getMessage()
    key = getKey()
    encrypted = encrypt(message, key)
    print(encrypted)
    decrypted = decrypt(encrypted, key)
    print(decrypted)
