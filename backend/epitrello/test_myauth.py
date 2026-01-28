from base64 import b64encode
from typing import override
from django.test import TestCase, Client
import sys


class MyBoardTest(TestCase):
    def test_user_login(self):
        c1: Client
        c1_email = "u1@ggl.com"
        c2: Client
        c2_email = "u2@ggl.com"
        #
        auth1 = b64encode(f"{c1_email}:u1".encode()).decode()
        c1 = Client(headers={"Authorization": f"Test {auth1}"})
        response = c1.get("/v2/auth/user/login/", follow=True)
        self.assertEqual(
            200,
            response.status_code,
            f"Get user failed | {response.text} | {response.status_code} | {response.headers}",
        )
        res = response.json()
        self.assertEqual(c1_email, res["email"], f"{res}")
        #
        auth2 = b64encode(f"{c2_email}:u2".encode()).decode()
        c2 = Client(headers={"Authorization": f"Test {auth2}"})
        response2 = c2.get("/v2/auth/user/login/", follow=True)
        self.assertEqual(
            200,
            response2.status_code,
            f"Get user failed | {response2.text} | {response2.status_code} | {response2.headers}",
        )
        res2 = response2.json()
        self.assertEqual(c2_email, res2["email"], f"{res2}")
