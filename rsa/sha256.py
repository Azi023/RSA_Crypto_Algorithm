import hashlib

def hash_message(message):
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()
    
    # Update the hash object with the bytes of the message
    sha256.update(message.encode())
    
    # Return the hex digest of the hash
    return sha256.hexdigest()

# Example usage
message = "Hello, SHA-256!"
hash_value = hash_message(message)
print(f"SHA-256 hash: {hash_value}")
