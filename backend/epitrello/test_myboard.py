from base64 import b64encode
from typing import override
from django.test import TestCase, Client
from myboard.models import Board, Task
import sys

class MyBoardTest(TestCase):
    c1: Client

    @override
    def setUp(self) -> None:
        auth = b64encode("u1@ggl.com:u1".encode()).decode()
        self.c1 = Client(headers={"Authorization": f"Test {auth}"})

    @override
    def tearDown(self) -> None:
        _ = Board.objects.all().delete()
        _ = Task.objects.all().delete()

    def test_create_board(self):
        title = "Test Board 1"
        response = self.c1.post("/v2/create/board/", data={"title": title}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"{response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        self.assertEqual(title, res.get("title"), f"Bad board title | {res}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(res["owner"]["id"], f"{board.owner.id}", f"Bad board owner id |{res}")

    def test_delete_board(self):
        title = "Test Board 2"
        response = self.c1.post("/v2/create/board/", data={"title": title}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        self.assertEqual(1, Board.objects.all().distinct().count(), "Number of board is not correct")
        response2 = self.c1.put(f"/v2/delete/board/{res['id']}/", follow=True, content_type="application/json")
        self.assertEqual(200, response2.status_code, f"Deletion of board failed | {response2.text} | {response2.status_code} | {response2.headers}")
        self.assertEqual(0, Board.objects.all().distinct().count(), "Number of board is not correct")

    def test_create_task(self):
        title = "Test Board 3"
        t_title = "fix bug 1"
        t_description = ""
        t_category = "ToDo"
        response = self.c1.post("/v2/create/board/", data={"title": title}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of board failed | {response.text} | {response.status_code} | {response.headers}")
        res = response.json()
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(0, board.tasks.all().distinct().count(), "Board tasks number does not match")
        response2 = self.c1.post(f"/v2/create/task/{res['id']}/", data={"title": t_title, "description": t_description, "category": t_category}, follow=True, content_type="application/json")
        self.assertEqual(200, response.status_code, f"Creation of task failed | {response2.text} | {response2.status_code} | {response2.headers}")
        res2 = response2.json()
        self.assertEqual(t_title, res2.get("title"), f"Bad task title | {res2}")
        self.assertEqual(t_description, res2.get("description"), f"Bad task description | {res2}")
        self.assertEqual(t_category, res2.get("category"), f"Bad task category {res2}")
        board = Board.objects.get(pk=res["id"])
        self.assertEqual(1, board.tasks.all().distinct().count(), "Board tasks number does not match")
