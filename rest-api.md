# Sahara REST API Documentation

Sahara is a simple web store that ships with a standard REST API.

## Response format

All responses are in JSON. If the process is successful, the response will have a 'status' property set to 'good'. If the process is unsuccessful, the response will have a 'status' property set to 'bad' and a 'message' property with an explanation for the error. If the response contains a data payload, there will be a 'data' property with the corresponding data.

## Authentication

### Log in

Logs the user into Sahara

#### Request

    POST to /api/auth/login/
    email: your email
    password: your password

#### Response

    name: your name
    staff: true if user has staff permissions, otherwise false

### Register

Creates a Sahara account for the user. Does not sign the user in.

#### Request

    POST /api/auth/login/
    email (unique): your email
    password: your password
    address (optional): your address
    name: your name

#### Response

    name: your name
    staff: true if user has staff permissions, otherwise false

### Logout

Ends the active user's session.

#### Request

    GET to /api/auth/logout/

## Products
