import argon2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from app.logger import logger

# Complete hashing function with parameters
def hash_password(password):
	# Configure the algorithm
	time_cost = 2          # Number of iterations
	memory_cost = 102400   # 100 MB in KiB
	parallelism = 8        # Number of parallel threads
	hash_len = 32          # Length of the hash in bytes
	salt_len = 16          # Length of the salt in bytes

	# Create the hasher
	ph = argon2.PasswordHasher(
		time_cost=time_cost,
		memory_cost=memory_cost,
		parallelism=parallelism,
		hash_len=hash_len,
		salt_len=salt_len,
		type=argon2.Type.ID  # Using Argon2id variant
	)

	# Hash the password (salt is generated automatically)
	hash = ph.hash(password)

	return hash

# # Example usage
# password = "super_secret_password"
# hash_result = hash_password(password)
# print(f"Hashed password: {hash_result}")

# # This will produce something like:
# # $argon2id$v=19$m=102400,t=2,p=8$RTRrSEl2MTNpSnZ3ZmFpNg$wxJjHFEQpJXsLFO+T5xzHJGkUqJkL7SYgvUB4GQqKyQ
# # Which includes the algorithm, version, parameters, salt, and hash

def verify_password(stored_hash, provided_password):
	ph = PasswordHasher()

	try:
		# The verify method returns True if the password matches
		# It raises an exception if the password doesn't match
		ph.verify(stored_hash, provided_password)
		return True
	except VerifyMismatchError:
		# Password doesn't match
		return False
	except InvalidHash:
		# The stored hash has an invalid format
		logger.error("Invalid hash format. The hash may be corrupted.")
		# print("Invalid hash format. The hash may be corrupted.")
		return False

# # Example usage
# stored_hash = "$argon2id$v=19$m=102400,t=2,p=8$RTRrSEl2MTNpSnZ3ZmFpNg$wxJjHFEQpJXsLFO+T5xzHJGkUqJkL7SYgvUB4GQqKyQ"
# is_valid = verify_password(stored_hash, "super_secret_password")
# if is_valid:
#     print("Password is correct!")
# else:
#     print("Password is incorrect!")