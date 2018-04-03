Protected API
-------------

This API endpoint (Django Rest Framework) is protected by the auth
service. It expects a JWT in the HTTP Authorization header. It will
validate the signature of this token to determine if the user is
authenticated or not.

The only endpoint currently is `/api/me/` which returns the JWT payload
to the caller.

