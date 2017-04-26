# MUD

This is a MUD built in Python that gives a web API

## Client

The URL is optional, it will default to localhost:5000
```Shell
python main.py "http://localhost:5000"
```

## Server
You must setup the mysql info in config.py. See below for schema required.
```Shell
python main.py "localhost"
```

## API

| URL  | Usage  | Data  | Returns  | Notes  |
|:-:|:-:|:-:|:-:|:-:|
| /api/user/register/  | Used to register new users.  | 'username', 'password' and 'salt'  | Either an 'error' field or 'result' field.  | 'password' should contain the user's plaintext password and a 'uuid.uuid4.hex()' as the 'salt' appended and then be hashed using SHA256 |
| /api/user/login/  | Used to get a token from an existing user. | 'username' and 'password'  | Either an 'error' field or 'result'. If 'result' is true a 'token' will be present  | 'password' should contain the user's plaintext password with the 'salt' retrieved appended and then be hashed with SHA256  |
| /api/user/salt/  |   |   |   |   |
| /api/user/location/  |   |   |   |   |