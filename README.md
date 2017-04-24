## MUD

This is a MUD built in Python that gives a web API

### API

| URL  | Usage  | Data  | Returns  | Notes  |
|:-:|:-:|:-:|:-:|:-:|
| /api/user/register/  | Used to register new users.  | 'username', 'password' and 'salt'  | Either an 'error' field or 'result' field.  | 'password' should have a 'uuid.uuid4.hex()' as the 'salt' appended and be hashed using SHA256 |
| /api/user/login/  | Used to get a token  |   |   |   |
| /api/user/salt/  |   |   |   |   |
| /api/user/location/  |   |   |   |   |