from ninja import NinjaAPI
from myauth.api import router as router_auth
from myboard.api import router as router_board

api = NinjaAPI()
api.add_router("/auth/", router_auth)
api.add_router("/board/", router_board)
