from typing import override
import orjson
from ninja import NinjaAPI
from ninja.parser import Parser
from django.http import HttpRequest

from myauth.api import router as router_auth
from myboard.api import router as router_board


class ORJSONParser(Parser):
    @override
    def parse_body(self, request: HttpRequest):
        return orjson.loads(request.body)


api = NinjaAPI(parser=ORJSONParser())
api.add_router("/auth/", router_auth)
api.add_router("/board/", router_board)
