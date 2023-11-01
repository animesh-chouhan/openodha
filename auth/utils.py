import bcrypt


def bcrypt_hash_password(input_password):
    hashed_password = bcrypt.hashpw(
        input_password.encode("utf-8"), salt=bcrypt.gensalt()
    )
    return hashed_password.decode("utf-8")


def bcrypt_check_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode(), stored_password.encode())
