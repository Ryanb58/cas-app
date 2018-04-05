CAS demonstration
=================

This repository contains a demonstration of integration of SmartFile /
Veristack with a 3rd party CAS application.

CAS is one of many options for Identity Management, Federation, SSO etc.
Regardless of the implementation details the overall structure of this
integration will remain the same.

It also showcases the use of JWT for authentication with a collection of
disparate REST API services.

The idea is that SmartFile / Veristack could consist of self-contained services
focused on specific aspects of the overall application. These services could
communicate with one another using HTTP REST. The cornerstone of such an
architecture is a unified authentication service that can issue tokens granting
access to these services.

Ideally such a service would not need to be involved in each service request,
instead the tokens must be verified by the individual services.

Auth-service
------------

This service provides authentication, authorization functionality. It has the
following capabilities.

 - Integration with external CAS (authentication, SSO).
 - Multiple realms (multi-tenant). Each with external auth capability.
 - REST API and Web-based user management.
 - User profile retrieval.
 - Authentication token issuance, validation, revocation.

With this functionality, A client can authenticate the user, then make requests
to any participating service. Privileged clients (those with superuser
credentials) can create realms and users (for instance, signup page).

Protected
---------

This service is an example of a REST API which is protected by auth-service. It
is a participating service and requires a valid token in order to successfully
complete a request.


CAS
---

This is an example CAS application that provides an external user store
utilized by auth-service. This component would most likely be provided by a
customer.
