from typing import List, Type

from .router import Router


class Server:
    routers: List[Type[Router]]

    def __init__(self, *router: Type[Router]):
        self.routers = list(router)

    def add_router(self, router: Type[Router]):
        self.routers.append(router)

    def query(self):
        pass

    def mutate(self):
        pass