import hashlib
from app.models import User


def validate_user(username, password):
    hashpass = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User.query.filter(User.userName == username.strip(),
                             User.passWord == hashpass).first()
    if user:
        return user
    return None


if __name__ == "__main__":
    print()
