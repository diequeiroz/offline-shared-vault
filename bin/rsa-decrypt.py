import ast, os, sys, base64

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

secret = base64.b64decode(sys.argv[1])

with open('gen/masterkey.pem') as privatefile:
	privateKey = load_pem_private_key(privatefile.read().encode(), str.encode(os.getenv("PASS")))

decMessage = privateKey.decrypt(secret, padding.PKCS1v15())

print(decMessage.decode("utf-8"))
