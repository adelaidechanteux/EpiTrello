# Epitrello backend api

---

## Login

METHOD: `POST`
PATH: `user/login/`
HEADERS:
```
Authorization: Bearer jwt
```

#### 200

```
{
    "id": "user uuid",
    "username": "user username",
    "email": "a@a.com",
    "profile_picture": "profile picture uri"
}
```

#### 400

Missing `Authorization` header

#### 403

Google did not validate the authorization jwt

---

## Get Board details

METHOD: `GET`
PATH: `/get/board/<uuid>`
HEADERS:
```
Authorization: Bearer jwt
```

#### 200

```
{
    "title": "some board title",
    "id": "board uuid",
    "favorite": false,
    "members": {
        "member uuid": {
            "profile_picture": "profile picture uri",
            "username": "member username",
            "email": "a@a.com",
            "owner": false,
            "id": "member id"
        }
    },
    "tasks": [
        {
            "title": "some task title",
            "description": "doing some more title description",
            "color": "#00FFAA",
            "class": "ToDo",
            "date_start": "",
            "date_end": "",
            "date_creation": "",
            "owner": "owner uuid",
            "assigned": "member uuid",
            "completed": false,
            "id": "task uuid",
        }
    ],
    "archived": [
        {
            "title": "some task title",
            "description": "doing some more title description",
            "color": "#00FFAA",
            "class": "ToDo",
            "date_start": "",
            "date_end": "",
            "date_creation": "",
            "owner": "owner uuid",
            "assigned": "member uuid",
            "completed": false,
            "id": "task uuid",
        }
    ]
}
```

#### 400

Missing `Authorization` header

#### 403

Google did not validate the authorization jwt

#### 404

Board `uuid` does not exists

---

## Invit email to Board

METHOD: `POST`
PATH: `invit/<uuid>`
HEADERS:
```
Authorization: Bearer jwt
```
BODY:
```
{
    "email": "a@a.com",
    "admin": false
}
```

#### 200

```
{}
```

#### 400

- Missing `Authorization` header
- or, Missing `email` in post body
- or, Missing `admin` in post body

#### 403

- Google did not validate the authorization jwt
- or, User is not the owner of the board

#### 404

- Board `uuid` does not exists
- or, User `email` does not exists

## Create Board

METHOD: `POST`
PATH: `create/board/`
HEADERS:
```
Authorization: Bearer jwt
```
BODY:
```
{
    "title": "some board title" # max 49 characters
}
```

#### 200

```
{
    "id": "board uuid"
}
```

#### 400

- Missing `Authorization` header
- or, Missing `title` in post body,
- or, Too many characters for the `title` value.

#### 403

Google did not validate the authorization jwt

### Delete Board

METHOD: `GET`
PATH: `delete/board/<uuid>`
HEADERS:
```
Authorization: Bearer jwt
```

#### 200

```
{}
```

#### 400

Missing `Authorization` header

#### 403

- Google did not validate the authorization jwt
- or, User is not the owner of the board

#### 404

Board with uuid does not exists
