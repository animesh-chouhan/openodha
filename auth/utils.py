import bcrypt


def bcrypt_hash_password(input_password):
    hashed_password = bcrypt.hashpw(input_password.encode(), salt=bcrypt.gensalt())
    return hashed_password


def bcrypt_check_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode(), stored_password)
