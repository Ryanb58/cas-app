Auth-service
============

A Django application capable of authenticating users, issuing tokens and
serving user profile information. This service provides an internal user
datastore and also has the capability to use external user datastores.

This application uses the concept of an authentication realm to separate users
into specific pools. Each realm can be configured to use internal or external
authentication.

When a user authenticates, they are issued a JWT token which can be used to
access other services (protected is an example of such a service). This token
can be validated by other services without involving auth-service. Also, the
tokens can be refreshed without user interaction.

Services can pass tokens to downstream services (composite services). Tokens
can be invalidated (logout). This service can also validate a token via an API
call (in case the client is unable to). This service can also provide user
profile information for arbitrary users (provided the caller has sufficient
permission and provides a valid JWT token).

The concept of "service accounts" is addressed using the Django superuser
capability. An internal user can be created with superuser permissions. This
user can create realms and users. Such an account might be useful for
provisioning services (such as a signup page) to create new accounts.
