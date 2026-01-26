# Epitrello http backend api

A swagger is now available for the new api version. `/v2/docs`

# Epitrello websocket backend api

The websocket is used to implement real-time update from multiple user connected at the same time on a board.

Every time a user has done an action, an event is sent through the websocket.

Every board has its own route to connect to.

`/ws/board/<board_id>/`

In this documentation, when the `# const` is put at the end of the line, it means that this data will allways be that value.

## Login to the websocket

The first message that needs to be sent is the login event.

```json
{
    "type": "login", # const
    "Authorization": "Bearer dwakjbfkjerqbfhqjewfbqewhjf" # the google bearer (it is like setting the Authorization header)
}
```

## Events received

After the login event sent, events will be sent.

### `f_invit_board`

```json
{
    "type": "f_invit_board", # const
    "admin": True,
    "user": {
        "id": "",
        username: "",
        email: "",
        profile_picture: ""
    }
}
```

### `f_delete_member`

```json
{
    "type": "f_delete_member", # const
    "id": ""
}
```

### `f_update_board`

```json
{
    "type": "f_update_board", # const
    "board_title": "",
    "board_owner": {
        "id": "",
        username: "",
        email: "",
        profile_picture: ""
    },
    "board_color": ""
}
```

### `f_update_categories`

```json
{
    "type": "f_update_categories", # const
    "categories": ["", ""]
}
```

### `f_create_task`

```json
{
    "type": "f_create_task", # const
    "task": {
        "id": "",
        "title": "",
        "description": "",
        "color": "",
        "category": "",
        "date_start": "",
        "date_end": "",
        "date_creation": "",
        "owner": "",
        "assigned": "",
        "completed": ""
    },
    "board_categories": ["", ""]
}
```

### `f_delete_task`

```json
{
    "type": "f_delete_task", # const
    "id": ""
}
```

### `f_deleteforce_task`

```json
{
    "type": "f_deleteforce_task", # const
    "id": ""
}
```

### `f_update_task`

```json
{
    "type": "f_update_task", # const
    "task": {
        "id": "",
        "title": "",
        "description": "",
        "color": "",
        "category": "",
        "date_start": "",
        "date_end": "",
        "date_creation": "",
        "owner": "",
        "assigned": "",
        "completed": ""
    },
    "board_categories": ["", ""]
}
```

### `f_restore_task`

```json
{
    "type": "", # const
    "task": {
        "id": "",
        "title": "",
        "description": "",
        "color": "",
        "category": "",
        "date_start": "",
        "date_end": "",
        "date_creation": "",
        "owner": "",
        "assigned": "",
        "completed": ""
    },
    "board_categories": ["", ""]
}
```

### `f_update_role`

```json
{
    "type": "f_update_role", # const
    "user": {
        "id": "",
        username: "",
        email: "",
        profile_picture: ""
    },
    "admin": True
}
```
