import hashlib

_hexhash = hashlib.sha512("password").hexdigest()

print _hexhash