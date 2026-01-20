from base64 import b64encode
from typing import override
from django.test import TestCase, Client
from myboard.models import Board, Task
import sys

class MyBoardTest(TestCase):
    c1: Client
    c1_email = "u1@ggl.com"
    c2: Client
    c2_email = "u2@ggl.com"

    @override
    def setUp(self) -> None:
        auth1 = b64encode(f"{self.c1_email}:u1".encode()).decode()
        self.c1 = Client(headers={"Authorization": f"Test {auth1}"})
        auth2 = b64encode(f"{self.c2_email}:u2".encode()).decode()
        self.c2 = Client(headers={"Authorization": f"Test {auth2}"})

    @override
    def tearDown(self) -> None:
        _ = Board.objects.all().delete()
        _ = Task.objects.all().delete()

    # BOARD

    def test_create_board(self):
        title = "Test Board 1"
        color = "#800081"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"{response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        self.assertEqual(title, res.get("title"), f"Bad board title | {res}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(res["owner"]["id"], f"{board.owner.id}", f"Bad board owner id |{res}")
        self.assertEqual(res["color"], color, f"{res}")

    def test_board_members(self):
        title = "Test Board b1"
        title2 = "Test Board b2"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"{response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response1 = self.c1.post("/v2/board/create/board/", data={"title": title2, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response1.status_code, f"{response1.text} | {response1.status_code} | {response1.headers}")
        res1 = response1.json()
        #
        response2 = self.c1.get("/v2/board/boards/", follow=True)
        self.assertEqual(200, response2.status_code, f"{response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        self.assertEqual(2, len(res2.get("boards")), f"{res2}")
        self.assertEqual(2, len(res2.get("owned")), f"{res2}")
        self.assertEqual(0, len(res2.get("favorite")), f"{res2}")
        self.assertEqual(2, len(res2.get("admin")), f"{res2}")


    def test_delete_board(self):
        title = "Test Board 2"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        self.assertEqual(1, Board.objects.all().distinct().count(), "Number of board is not correct")
        #
        response2 = self.c1.put(f"/v2/board/delete/board/{res['id']}/", follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Deletion of board failed | {response2.text} | {response2.status_code} | {response2.headers}")
        self.assertEqual(0, Board.objects.all().distinct().count(), "Number of board is not correct")

    def test_update_board(self):
        title = "Test Board a"
        title2 = "Test Board b"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        board = Board.objects.get(pk=res['id'])
        self.assertEqual(title, res.get("title"), f"{res}")
        self.assertEqual(title, board.title)
        #
        response2 = self.c1.put(f"/v2/board/update/board/{res['id']}/", data={"title": title2}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Update of board failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        board2 = Board.objects.get(pk=res2['id'])
        self.assertEqual(title2, res2.get("title"), f"{res2}")
        self.assertEqual(title2, board2.title)

    def test_invit(self):
        title = "Test board c"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response3 = self.c2.post(f"/v2/board/invit/board/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(403, response3.status_code, f"Invit failed | {response3.text} | {response3.status_code} | {response3.headers}")
        #
        response2 = self.c1.post(f"/v2/board/invit/board/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Invit failed | {response2.text} | {response2.status_code} | {response2.headers}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.members.filter(email=self.c2_email).distinct().count(), f"{list(board.members.all())}")


    def test_delete_member(self):
        title = "Test board c"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response3 = self.c2.post(f"/v2/board/invit/board/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(403, response3.status_code, f"Invit failed | {response3.text} | {response3.status_code} | {response3.headers}")
        #
        response2 = self.c1.post(f"/v2/board/invit/board/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Invit failed | {response2.text} | {response2.status_code} | {response2.headers}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.members.filter(email=self.c2_email).distinct().count(), f"{list(board.members.all())}")
        #
        response3 = self.c1.put(f"/v2/board/delete/member/{res['id']}/", data={"email": self.c2_email}, follow=True, content_type="application/json")
        self.assertEqual(200, response3.status_code, f"Invit failed | {response3.text} | {response3.status_code} | {response3.headers}")
        board3 = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board3.members.filter(email=self.c2_email).distinct().count(), f"{list(board3.members.all())}")


    def test_update_categories(self):
        title = "Test board c"
        t_cat = ["Backlog", "ToDo", "Done"]
        t1_cat = ["Backlog", "ToDo", "InProgress", "Done"]
        t2_cat = ["Done", "ToDo"]
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        self.assertEqual([], res["categories"], "Bad categories")
        #
        response2 = self.c1.put(f"/v2/board/update/categories/{res['id']}/", data={"categories": t_cat}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Update of categories failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        self.assertEqual(t_cat, res2["categories"], "Bad categories")
        self.assertEqual(t_cat, Board.objects.get(pk=res["id"]).categories)
        #
        response3 = self.c1.put(f"/v2/board/update/categories/{res['id']}/", data={"categories": t1_cat}, follow=True, content_type="application/json")
        self.assertEqual(200, response3.status_code, f"Update of categories failed | {response3.text} | {response3.status_code} | {response3.headers}")
        res3 = response3.json()
        self.assertEqual(t1_cat, res3["categories"], "Bad categories")
        self.assertEqual(t1_cat, Board.objects.get(pk=res["id"]).categories)
        #
        response4 = self.c1.put(f"/v2/board/update/categories/{res['id']}/", data={"categories": t2_cat}, follow=True, content_type="application/json")
        self.assertEqual(200, response4.status_code, f"Update of categories failed | {response4.text} | {response4.status_code} | {response4.headers}")
        res4 = response4.json()
        self.assertEqual(t2_cat, res4["categories"], "Bad categories")
        self.assertEqual(t2_cat, Board.objects.get(pk=res["id"]).categories)


    def test_update_favorite(self):
        title = "Test board c"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response2 = self.c1.put(f"/v2/board/update/favorite/{res['id']}/", data={"favorite": True}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Put to favorite failed | {response2.text} | {response2.status_code} | {response2.headers}")
        #
        response3 = self.c1.get("/v2/board/boards/", follow=True)
        self.assertEqual(200, response3.status_code, f"{response3.text} | {response3.status_code} | {response3.headers}")
        res3 = response3.json()
        self.assertEqual(1, len(res3.get("boards")), f"{res3}")
        self.assertEqual(1, len(res3.get("owned")), f"{res3}")
        self.assertEqual(1, len(res3.get("favorite")), f"{res3}")
        self.assertEqual(1, len(res3.get("admin")), f"{res3}")
        #
        response4 = self.c1.put(f"/v2/board/update/favorite/{res['id']}/", data={"favorite": False}, follow=True, content_type="application/json")
        self.assertEqual(200, response4.status_code, f"Put to favorite failed | {response4.text} | {response4.status_code} | {response4.headers}")
        #
        response5 = self.c1.get("/v2/board/boards/", follow=True)
        self.assertEqual(200, response5.status_code, f"{response5.text} | {response5.status_code} | {response5.headers}")
        res5 = response5.json()
        self.assertEqual(1, len(res5.get("boards")), f"{res5}")
        self.assertEqual(1, len(res5.get("owned")), f"{res5}")
        self.assertEqual(0, len(res5.get("favorite")), f"{res5}")
        self.assertEqual(1, len(res5.get("admin")), f"{res5}")


    def test_update_role(self):
        title = "Test board c"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response3 = self.c2.post(f"/v2/board/invit/board/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(403, response3.status_code, f"Invit failed | {response3.text} | {response3.status_code} | {response3.headers}")
        #
        response2 = self.c1.post(f"/v2/board/invit/board/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Invit failed | {response2.text} | {response2.status_code} | {response2.headers}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.members.filter(email=self.c2_email).distinct().count(), f"{list(board.members.all())}")
        self.assertEqual(0, board.admin.filter(email=self.c2_email).distinct().count(), f"{list(board.admin.all())}")
        #
        response4 = self.c1.put(f"/v2/board/update/role/{res['id']}/", data={"email": self.c2_email, "admin": True}, follow=True, content_type="application/json")
        self.assertEqual(200, response4.status_code, f"Update role failed | {response4.text} | {response4.status_code} | {response4.headers}")
        #
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.members.filter(email=self.c2_email).distinct().count(), f"{list(board.members.all())}")
        self.assertEqual(1, board.admin.filter(email=self.c2_email).distinct().count(), f"{list(board.admin.all())}")
        #
        response5 = self.c1.put(f"/v2/board/update/role/{res['id']}/", data={"email": self.c2_email, "admin": False}, follow=True, content_type="application/json")
        self.assertEqual(200, response5.status_code, f"Update role failed | {response5.text} | {response5.status_code} | {response5.headers}")
        #
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.members.filter(email=self.c2_email).distinct().count(), f"{list(board.members.all())}")
        self.assertEqual(0, board.admin.filter(email=self.c2_email).distinct().count(), f"{list(board.admin.all())}")


    # TASK

    def test_create_task(self):
        title = "Test Board 3"
        t_title = "fix bug 1"
        t3_title = "fix bug 2"
        t_description = ""
        t3_description = "adfsafd"
        t_category = "ToDo"
        t3_category = "Abcd"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board.tasks.all().distinct().count(), "Board tasks number does not match")
        #
        response2 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        self.assertEqual(t_title, res2.get("title"), f"Bad task title | {res2}")
        self.assertEqual(t_description, res2.get("description"), f"Bad task description | {res2}")
        self.assertEqual(t_category, res2.get("category"), f"Bad task category {res2}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.tasks.all().distinct().count(), "Board tasks number does not match")
        task2 = Task.objects.get(pk=res2["id"])
        self.assertEqual(t_title, task2.title, f"Bad task title | {res2}")
        self.assertEqual(t_description, task2.description, f"Bad task description | {res2}")
        self.assertEqual(t_category, task2.category, f"Bad task category {res2}")
        #
        response3 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t3_title, "description": t3_description, "category": t3_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of task failed | {response3.text} | {response3.status_code} | {response3.headers}")
        res3 = response3.json()
        self.assertEqual(t3_title, res3.get("title"), f"Bad task title | {res3}")
        self.assertEqual(t3_description, res3.get("description"), f"Bad task description | {res3}")
        self.assertEqual(t3_category, res3.get("category"), f"Bad task category {res3}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(2, board.tasks.all().distinct().count(), "Board tasks number does not match")
        task3 = Task.objects.get(pk=res3["id"])
        self.assertEqual(t3_title, task3.title, f"Bad task title | {res3}")
        self.assertEqual(t3_description, task3.description, f"Bad task description | {res3}")
        self.assertEqual(t3_category, task3.category, f"Bad task category {res3}")

    def test_delete_task(self):
        title = "Test board a1"
        t_title = "fix bug 1"
        t_description = "afasdfasd"
        t_category = "Done"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response2 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        board2 = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board2.tasks.all().distinct().count(), "Task number bad")
        #
        response3 = self.c1.put(f"/v2/board/delete/task/{res['id']}/{res2['id']}/", follow=True)
        self.assertEqual(200, response3.status_code, f"Delete task failed | {response3.text} | {response3.status_code} | {response3.headers}")
        board3 = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board3.tasks.all().distinct().count(), "Task number bad")
        self.assertEqual(1, board3.archived.all().distinct().count(), "Task number bad")

    def test_deleteforce_task(self):
        title = "Test board a1"
        t_title = "fix bug 1"
        t_description = "afasdfasd"
        t_category = "Done"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response2 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        board2 = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board2.tasks.all().distinct().count(), "Task number bad")
        #
        response3 = self.c1.put(f"/v2/board/delete/task/{res['id']}/{res2['id']}/", follow=True)
        self.assertEqual(200, response3.status_code, f"Delete task failed | {response3.text} | {response3.status_code} | {response3.headers}")
        board3 = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board3.tasks.all().distinct().count(), "Task number bad")
        self.assertEqual(1, board3.archived.all().distinct().count(), "Task number bad")
        #
        response4 = self.c1.put(f"/v2/board/deleteforce/task/{res['id']}/{res2['id']}/", follow=True)
        self.assertEqual(200, response4.status_code, f"Delete task failed | {response4.text} | {response4.status_code} | {response4.headers}")
        board4 = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board4.tasks.all().distinct().count(), "Task number bad")
        self.assertEqual(0, board4.archived.all().distinct().count(), "Task number bad")


    def test_restore_task(self):
        title = "Test board a1"
        t_title = "fix bug 1"
        t_description = "afasdfasd"
        t_category = "Done"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response2 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        board2 = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board2.tasks.all().distinct().count(), "Task number bad")
        #
        response3 = self.c1.put(f"/v2/board/delete/task/{res['id']}/{res2['id']}/", follow=True)
        self.assertEqual(200, response3.status_code, f"Delete task failed | {response3.text} | {response3.status_code} | {response3.headers}")
        board3 = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board3.tasks.all().distinct().count(), "Task number bad")
        self.assertEqual(1, board3.archived.all().distinct().count(), "Task number bad")
        #
        response4 = self.c1.put(f"/v2/board/restore/task/{res['id']}/{res2['id']}/", follow=True)
        self.assertEqual(200, response4.status_code, f"Restore task failed | {response4.text} | {response4.status_code} | {response4.headers}")
        board4 = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board4.tasks.all().distinct().count(), "Task number bad")
        self.assertEqual(0, board4.archived.all().distinct().count(), "Task number bad")


    def test_update_task(self):
        title = "Test Board 4"
        t_title = "fix bug 1"
        t3_title = "fix bug 2"
        t_description = ""
        t3_description = "sjgfhnqhliqw"
        t_category = "ToDo"
        t3_category = "Abcd"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board.tasks.all().distinct().count(), "Board tasks number does not match")
        #
        response2 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        self.assertEqual(t_title, res2.get("title"), f"Bad task title | {res2}")
        self.assertEqual(t_description, res2.get("description"), f"Bad task description | {res2}")
        self.assertEqual(t_category, res2.get("category"), f"Bad task category {res2}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.tasks.all().distinct().count(), "Board tasks number does not match")
        task2 = Task.objects.get(pk=res2["id"])
        self.assertEqual(t_title, task2.title, f"Bad task title | {res2}")
        self.assertEqual(t_description, task2.description, f"Bad task description | {res2}")
        self.assertEqual(t_category, task2.category, f"Bad task category {res2}")
        #
        response3 = self.c1.put(f"/v2/board/update/task/{res['id']}/{res2['id']}/", data={"title": t3_title, "description": t3_description, "category": t3_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response3.status_code, f"Update of task failed | {response3.status_code} | {response3.text} | {response3.headers}")
        res3 = response3.json()
        self.assertEqual(t3_title, res3.get("title"), f"Bad task title | {res2}")
        self.assertEqual(t3_description, res3.get("description"), f"Bad task description | {res2}")
        self.assertEqual(t3_category, res3.get("category"), f"Bad task category {res2}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.tasks.all().distinct().count(), "Board tasks number does not match")
        task3 = Task.objects.get(pk=res3["id"])
        self.assertEqual(t3_title, task3.title, f"Bad task title | {res3}")
        self.assertEqual(t3_description, task3.description, f"Bad task description | {res3}")
        self.assertEqual(t3_category, task3.category, f"Bad task category {res3}")
        #
        self.assertEqual(task2.id, task3.id, f"Bad task selected | {task2.id} | {task3.id}")

    def test_update_task_order(self):
        title = "Test Board 3"
        t_title = "fix bug 1"
        t3_title = "fix bug 2"
        t_description = ""
        t3_description = "adfsafd"
        t_category = "ToDo"
        t3_category = "Abcd"
        color = "#800080"
        #
        response = self.c1.post("/v2/board/create/board/", data={"title": title, "color": color}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        #
        response2 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        #
        response3 = self.c1.post(f"/v2/board/create/task/{res['id']}/", data={"title": t3_title, "description": t3_description, "category": t3_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response3.status_code, f"Creation of task failed | {response3.text} | {response3.status_code} | {response3.headers}")
        res3 = response3.json()
        #
        response4 = self.c1.get(f"/v2/board/get/board/{res['id']}/", follow=True)
        self.assertEqual(200, response4.status_code, f"Get board failed | {response4.text} | {response4.status_code} | {response4.headers}")
        res4 = response4.json()
        self.assertEqual(res2["id"], res4["tasks"][0]["id"], f"Order Failed | {res4}")
        self.assertEqual(res3["id"], res4["tasks"][1]["id"], f"Order Failed | {res4}")
        #
        response5 = self.c1.put(f"/v2/board/update/task/{res['id']}/{res2['id']}/", data={"order": 1}, follow=True, content_type="application/json")
        self.assertEqual(200, response5.status_code, f"Update task failed | {response5.text} | {response5.status_code} | {response5.headers}")
        #
        response6 = self.c1.get(f"/v2/board/get/board/{res['id']}/", follow=True)
        self.assertEqual(200, response6.status_code, f"Get board failed | {response6.text} | {response6.status_code} | {response6.headers}")
        res6 = response6.json()
        self.assertEqual(res3["id"], res6["tasks"][0]["id"], f"Order Failed | {res6}")
        self.assertEqual(res2["id"], res6["tasks"][1]["id"], f"Order Failed | {res6}")
