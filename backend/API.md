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
            "title": "task title",
            "description": "task description",
            "color": "task color as Hexadecimal",
            "category": "task category",
            "date_start": null, # or "2025-12-16 14:52:42.726993"
            "date_end": null, # or "2025-12-16 14:52:42.726993"
            "date_creation": "2025-12-16 14:52:42.726993",
            "owner": "task owner (user) id",
            "assigned": null, # or "task assignee (user) id"
            "completed": false,
            "id": "task id"
        }
    ],
    "archived": [
        {
            "title": "task title",
            "description": "task description",
            "color": "task color as Hexadecimal",
            "category": "task category",
            "date_start": null, # or "2025-12-16 14:52:42.726993"
            "date_end": null, # or "2025-12-16 14:52:42.726993"
            "date_creation": "2025-12-16 14:52:42.726993",
            "owner": "task owner (user) id",
            "assigned": null, # or "task assignee (user) id"
            "completed": false,
            "id": "task id"
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

---

## Create Task

METHOD: `POST`
PATH: `create/task/<uuid:board_id>`
HEADERS:
```
Authorization: Bearer jwt
```
BODY:
```
{
    "title": "task title", # max 49 characters
    "description": "task description",
    "category": "task category", # max 29 characters
    "color": "#00FF33", # as Hexadecimal # optional
    "date_start": "2025-12-16 14:52:42.726993", # optional
    "date_end": "2025-12-16 14:52:42.726993", # optional
    "assigned": "task assignee (user) id" # optional
}
```

#### 200

```
{
    "title": "task title",
    "description": "task description",
    "color": "task color as Hexadecimal",
    "category": "task category",
    "date_start": null, # or "2025-12-16 14:52:42.726993"
    "date_end": null, # or "2025-12-16 14:52:42.726993"
    "date_creation": "2025-12-16 14:52:42.726993",
    "owner": "task owner (user) id",
    "assigned": null, # or "task assignee (user) id"
    "completed": false,
    "id": "task id"
}
```

#### 400

- Missing `Authorization` header
- or, `Content-Type` header must be 'application/json'
- or, Bad json format for body
- or, Missing one of 'title', 'description', 'category' in body
- or, Bad value for 'title' or 'category'

#### 403

- Google did not validate the authorization jwt

#### 404

- Board does not exists
- or, user does not exists

---

## Delete Task (archived)

METHOD: `GET`
PATH: `delete/task/<uuid:board_id>/<uuid_task_id>/`
HEADERS:
```
Authorization: Bearer jwt
```

#### 200

```
{}
```

#### 400

- Missing `Authorization` header
- or, Task is not part of Board tasks

#### 403

- Google did not validate the authorization jwt

#### 404

- Task does not exists
- or, Board does not exists

---

## Delete (force) Task (from archived)

METHOD: `GET`
PATH: `deleteforce/task/<uuid:board_id>/<uuid:task_id>/`
HEADERS:
```
Authorization: Bearer jwt
```

#### 200

```
{}
```

#### 400

- Missing `Authorization` header
- or, Task is not part of Board archived

#### 403

- Google did not validate the authorization jwt

#### 404

- Task does not exists
- or, Board does not exists

---

## Update Task

METHOD: `PUT`
PATH: `update/task/<uuid:task_id>/`
HEADERS:
```
Authorization: Bearer jwt
```
BODY:
```
{
    "title": "task title", # max 49 characters # optional
    "description": "task description", # optional
    "color": "#00FF33", # as Hexadecimal # optional
    "category": "task category", # max 29 characters # optional
    "date_start": "2025-12-16 14:52:42.726993", # optional
    "date_end": "2025-12-16 14:52:42.726993", # optional
    "owner": "task owner (user) id", # optional
    "assigned": "task assignee (user) id", # optional
    "completed": false # optional
}
```

#### 200

```
{
    "title": "task title",
    "description": "task description",
    "color": "task color as Hexadecimal",
    "category": "task category",
    "date_start": null, # or "2025-12-16 14:52:42.726993"
    "date_end": null, # or "2025-12-16 14:52:42.726993"
    "date_creation": "2025-12-16 14:52:42.726993",
    "owner": "task owner (user) id",
    "assigned": null, # or "task assignee (user) id"
    "completed": false,
    "id": "task id"
}
```

#### 400

- Missing `Authorization` header
- or, `Content-Type` header must be 'application/json'
- or, Bad json format for body

#### 403

- Google did not validate the authorization jwt
- Attempting to change owner, but user is not the owner of the task

#### 404

Task does not exists

---

## Remove Member

METHOD: `POST`
PATH: `delete/member/<uuid:board_id>/`
HEADERS:
```
Authorization: Bearer jwt
```
BODY:
```
{
    "email": "a@a.com"
}
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
            "title": "task title",
            "description": "task description",
            "color": "task color as Hexadecimal",
            "category": "task category",
            "date_start": null, # or "2025-12-16 14:52:42.726993"
            "date_end": null, # or "2025-12-16 14:52:42.726993"
            "date_creation": "2025-12-16 14:52:42.726993",
            "owner": "task owner (user) id",
            "assigned": null, # or "task assignee (user) id"
            "completed": false,
            "id": "task id"
        }
    ],
    "archived": [
        {
            "title": "task title",
            "description": "task description",
            "color": "task color as Hexadecimal",
            "category": "task category",
            "date_start": null, # or "2025-12-16 14:52:42.726993"
            "date_end": null, # or "2025-12-16 14:52:42.726993"
            "date_creation": "2025-12-16 14:52:42.726993",
            "owner": "task owner (user) id",
            "assigned": null, # or "task assignee (user) id"
            "completed": false,
            "id": "task id"
        }
    ]
}
```

#### 400

- Missing `Authorization` header
- or, `Content-Type` header must be 'application/json'
- or, Bad json format for body
- or, Missing 'email' in body

#### 403

- Google did not validate the authorization jwt
- or, Owner is not connected user

#### 404

- Board does not exists
- User does not exists
