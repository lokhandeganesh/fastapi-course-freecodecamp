from passlib.context import CryptContext
# from passlib.hash import pbkdf2_sha256

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password = "mysecretpassword"
# hashed_password = pbkdf2_sha256.hash(password)
# print(hashed_password)

# provided_password = "mysecretpassword"
# stored_hashed_password = "..." # Retrieve this from your database

# if pbkdf2_sha256.verify(provided_password, stored_hashed_password):
#     print("Login successful!")
# else:
#     print("Invalid credentials.")


def hash(password: str):
	return pwd_context.hash(password)


def verify(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)
