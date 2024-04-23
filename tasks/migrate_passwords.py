
import bcrypt
if len(pwd) == 0:
    return false
bytes(pwd, "UTF-8")
bcrypt.checkpwd(b"password", b"salt")
