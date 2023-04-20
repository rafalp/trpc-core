from typing import Dict, Optional, Type, Union

from .procedure import Procedure, WrappedProcedure
from .router import Router


class Server:
    procedures: Dict[str, Union[Procedure, WrappedProcedure]]

    def __init__(self, *routers: Type[Router]):
        self.procedures = {}

        for router in routers:
            self.add_router(router)

    def add_router(self, router: Type[Router]):
        for attr_name in dir(router):
            attr = getattr(router, attr_name)
            if isinstance(attr, (Procedure, WrappedProcedure)):
                self.procedures[attr.name] = attr

    def query(self, name: str, params: Optional[dict] = None):
        if name in self.procedures:
            kwargs = params or {}
            return self.procedures[name].query(None, **kwargs)

        raise ValueError(f"query {name} is not defined")

    def mutation(self, name: str, params: Optional[dict] = None):
        if name in self.procedures:
            kwargs = params or {}
            return self.procedures[name].mutation(None, **kwargs)

        raise ValueError(f"mutation {name} is not defined")
