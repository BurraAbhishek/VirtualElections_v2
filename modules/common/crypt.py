import base64


def str_encrypt(message: str) -> str:
    messagebytes = message.encode("ascii")
    b64bytes = base64.b64encode(messagebytes)
    b64str = b64bytes.decode("ascii")
    return b64str


def str_decrypt(encrypted: str) -> str:
    encryptedbytes = encrypted.encode("ascii")
    messagebytes = base64.b64decode(encryptedbytes)
    message = messagebytes.decode("ascii")
    return message
