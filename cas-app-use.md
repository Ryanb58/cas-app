## Start App:

```
make run
```

#### note: might have to create `db` folder under auth_service.

## FTP Auth:
Create an Realm & ExternalAuthentication object.
Realm: Default

Navigate to http://localhost:8000/api/auth/token/obtain/
Login

Username: ryanb58
Password: testing123

Response:

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTUyNDU4NDE5MiwianRpIjoiYjRkZDZlMDdiZWI2NDkwMWFjNTg2NTgyNGM0NTVmOGYiLCJ1c2VyX2lkIjoiMzNkM2U4NDctYzBiNy00MDEyLTkxMGEtNjg4MjE0MjE1YjI3IiwidXNlcm5hbWUiOiJyeWFuYjU4In0.Vbxx7w5vMZ5GxoyqyJ8zLo4v2n2O5R6SRxZHmSmLt_U",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTI0NDk4OTkyLCJqdGkiOiJlODdkZDE4MDkxZjg0N2FkYjlmMzlhMzllNjE2NmNhYiIsInVzZXJfaWQiOiIzM2QzZTg0Ny1jMGI3LTQwMTItOTEwYS02ODgyMTQyMTViMjciLCJ1c2VybmFtZSI6InJ5YW5iNTgifQ.XpKpbSmf1u6Qm2LL5MvY1jaulGTdsQ7Vu_pVU5PfBQk"
}


Decode Token:

```
import base64
base64.b64decode("eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTI0NDk4OTkyLCJqdGkiOiJlODdkZDE4MDkxZjg0N2FkYjlmMzlhMzllNjE2NmNhYiIsInVzZXJfaWQiOiIzM2QzZTg0Ny1jMGI3LTQwMTItOTEwYS02ODgyMTQyMTViMjciLCJ1c2VybmFtZSI6InJ5YW5iNTgifQ")
```

Open Postman:
GET http://localhost:8000/api/protected/me/
Authorization =  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTI0NDk4OTkyLCJqdGkiOiJlODdkZDE4MDkxZjg0N2FkYjlmMzlhMzllNjE2NmNhYiIsInVzZXJfaWQiOiIzM2QzZTg0Ny1jMGI3LTQwMTItOTEwYS02ODgyMTQyMTViMjciLCJ1c2VybmFtZSI6InJ5YW5iNTgifQ.XpKpbSmf1u6Qm2LL5MvY1jaulGTdsQ7Vu_pVU5PfBQk



## Web Auth:
