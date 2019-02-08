import pymysql

# I'm totally aware this is hardcoded
# I found out at 1am (while drunk) that I needed to code thiss
# And I legit couldn't be bothered to read this shit from environ variables
# Treat this python as basically a config file huehuehue
_HOST = "127.0.0.1"
_USER = "xsspay"
_PASS = "password"
_DB = "xsspay"

# Also I wouldn't use pymysql; i'd use an ORM lik sqlalchemy..
# but it's also 3am rn and I don't care
def connect():
    return pymysql.connect(
        host=_HOST,
        user=_USER,
        password=_PASS,
        db=_DB,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
