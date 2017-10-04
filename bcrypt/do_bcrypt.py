'''
Ultra simple example of how bcrypt and compare the generated hash with bcrypt lib
'''
import bcrypt
import base64
import hashlib

# My secret
MY_SECRET=b"e-attestations.com"

# Hashing
print 'Hashing my secret'
hashed = bcrypt.hashpw(MY_SECRET, bcrypt.gensalt())
print hashed

# Comparing
if bcrypt.hashpw(MY_SECRET, hashed) == hashed:
    print "It matches"
else:
    print "It does not match"

# One more time with more logs in the salt -> lots of CPU !
print 'Secret with more salt'
hashed = bcrypt.hashpw(MY_SECRET, bcrypt.gensalt(14))
print hashed

# Still matching !
if bcrypt.hashpw(MY_SECRET, hashed) == hashed:
    print "It matches again !"
else:
    print "It does match again !"

# For very long secrets up to 256 long password for instance
print 'Very long secret'
hashed = bcrypt.hashpw(
    base64.b64encode(hashlib.sha256(MY_SECRET).digest()),
    bcrypt.gensalt(14)
)
print hashed

# Still matching !
if bcrypt.hashpw(MY_SECRET, hashed) == hashed:
    print "It matches again !!"
else:
    print "It does match again !!"

# Generate a Key similar to SSL
print 'Generate key'
key = bcrypt.kdf(
     password=MY_SECRET,
     salt=b'mysaltysal',
     desired_key_bytes=32,
     rounds=100)
print key
