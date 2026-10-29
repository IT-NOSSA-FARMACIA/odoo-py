from __future__ import annotations
from typing import Any
from environs import Env
import xmlrpc.client

from ._transport import DEFAULT_TIMEOUT, server_proxy

env = Env()
env.read_env()


class OdooGenericIntegration:
    def __init__(
        self,
        odoo_url: str | None = None,
        odoo_db: str | None = None,
        odoo_username: str | None = None,
        odoo_password: str | None = None,
        odoo_language: str | None = None,
        odoo_timeout: float | None = None,
    ) -> None:
        self._url = odoo_url or env.str("ODOO_URL")
        self._db = odoo_db or env.str("ODOO_DB")
        self._username = odoo_username or env.str("ODOO_USERNAME")
        self._password = odoo_password or env.str("ODOO_PASSWORD")
        self._language = odoo_language or env.str("ODOO_LANGUAGE", default="es_ES")
        self._timeout = odoo_timeout or env.float("ODOO_TIMEOUT", default=DEFAULT_TIMEOUT)
        self._common = server_proxy("{}/xmlrpc/2/common".format(self._url), self._timeout)
        self._uid = self._common.authenticate(
            self._db, self._username, self._password, {}
        )
        self._models = server_proxy("{}/xmlrpc/2/object".format(self._url), self._timeout)

    def execute_kw(
        self,
        model: str,
        method: str,
        args: list[Any],
        kwargs: dict[str, Any] | None = None,
    ) -> list[int]:
        default_kwargs = {"context": {"lang": self._language}}
        if kwargs:
            default_kwargs.update(kwargs)
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            method,
            args,
            default_kwargs,
        )
        return response

    def search(
        self,
        model: str,
        search_params: list[Any],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[int]:
        response = self.execute_kw(
            model=model,
            method="search",
            args=[search_params],
            kwargs=kwargs_data,
        )
        return response

    def search_read(
        self,
        model: str,
        search_params: list[Any],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[int]:
        response = self.execute_kw(
            model=model,
            method="search_read",
            args=[search_params],
            kwargs=kwargs_data,
        )
        return response

    def search_count(
        self,
        model: str,
        search_params: list[Any],
        kwargs_data: dict[str, Any] | None = None,
    ) -> int:
        response = self.execute_kw(
            model=model,
            method="search_count",
            args=[search_params],
            kwargs=kwargs_data,
        )
        return response

    def read(
        self,
        model: str,
        ids: list[int | str],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        response = self.execute_kw(
            model=model,
            method="read",
            args=[ids],
            kwargs=kwargs_data,
        )
        return response

    def create(
        self,
        model: str,
        data: dict[str, Any],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        response = self.execute_kw(
            model=model,
            method="create",
            args=[data],
            kwargs=kwargs_data,
        )
        return response

    def bulk_create(
        self,
        model: str,
        data: list[dict[str, Any]],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        response = self.execute_kw(
            model=model,
            method="create",
            args=data,
            kwargs=kwargs_data,
        )
        return response

    def update(
        self,
        model: str,
        object_id: int | str,
        data: list[dict[str, Any]],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        response = self.execute_kw(
            model=model,
            method="write",
            args=[[object_id], data],
            kwargs=kwargs_data,
        )
        return response

    def bulk_update(
        self,
        model: str,
        records: list[dict[str, Any]],
        kwargs_data: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        response = self.execute_kw(
            model=model,
            method="write",
            args=records,
            kwargs=kwargs_data,
        )
        return response

    def call_method(
        self,
        model: str,
        call_method: str,
        args: list[any],
        kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = self.execute_kw(
            model=model,
            method=call_method,
            args=args,
            kwargs=kwargs,
        )
        return response
