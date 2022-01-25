# Doc

## About
This is a backend for a simple social media application. It is created using django as the backend framework and MongoDB as the database provider.


## End points

* **/api/create**: This endpoint creates an account using the username and password provided as its request.
### Request
```JSON
{
	"username": "GhoulRe",
	"password": "1234"
}
```
### Response
```JSON
{
    "return": "created"
}
```
or 
```JSON
{
    "return": "invalid"
}
```
or 
```JSON
{
    "return": "already exists"
}
```

* **/api/login**: This is used to handle logging in
### Request
```JSON
{
	"username": "GhoulRe",
	"password": "1234"
}
```
### Response
```JSON
{
    "return": "correct"
}
```
or
```JSON
{
    "return": "invalid"
}
```
The text for the second login return case is kept as "invalid" for consistency

* **/api/chats**: This is used to handle logging in
### Request
```JSON
{
	"users": ["GhoulRe", "GhoulKing"]
}
```
### Response
```JSON
[
    {"from": "GhoulRe", "text": "Hello"}
    {"from": "GhoulKing", "text": "Hi"}
]
```
or
```JSON
[]
```

* **/api/send**: This is used to handle logging in
### Request
```JSON
{
	"users": ["GhoulRe", "GhoulKing"],
    "message": {
        "from": "GhoulRe",
        "message": "How you doing?"
    }
}
```
### Response
```JSON
{
    "from": "GhoulRe",
    "message": "How you doing?"
}
```