# Epitrello backend api

## Get Board details

METHOD: `GET`
PATH: `/get/board/<uuid>`

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
            "owner": false
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

#### 404

Board `uuid` does not exists

## Invit email to Board

METHOD: `POST`
PATH: `invit/<uuid>`
HEADERS:
```
{
    "email": "a@a.com",
    "admin": false
}
```
RETURN

#### 200

#### 400

- Missing `email` in post body
- or, Missing `admin` in post body

#### 404

- Board `uuid` does not exists
- or, User `email` does not exists

#### 403

User is not the owner of the board

## Create Board

METHOD: `POST`
PATH: `create/board/<uuid>`
HEADERS:
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

- Missing `title` in post body,
- or, Too many characters for the `title` value.

### Delete Board

METHOD: `GET`
PATH: `delete/board/<uuid>`

#### 200

#### 404

Board with uuid does not exists

#### 403

User is not the owner of the board
