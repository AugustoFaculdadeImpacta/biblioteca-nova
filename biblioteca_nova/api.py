"""HTTP client for the library backend."""

import os
from typing import Any

import httpx


XANO_BASE_URL = os.getenv(
    "XANO_BASE_URL",
    "https://x8ki-letl-twmt.n7.xano.io/api:sNcpa9z-",
).rstrip("/")


class APIError(Exception):
    """Raised when Xano cannot provide a valid response."""


def _error_message(response: httpx.Response) -> str:
    try:
        payload = response.json()
        if isinstance(payload, dict):
            for key in ("message", "error", "detail"):
                value = payload.get(key)
                if value:
                    return str(value)
    except ValueError:
        pass
    return f"A API retornou o status {response.status_code}."


def _request(method: str, path: str, token: str = "", **kwargs: Any) -> Any:
    headers = dict(kwargs.pop("headers", {}))
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = httpx.request(
            method,
            f"{XANO_BASE_URL}{path}",
            timeout=15.0,
            headers=headers,
            **kwargs,
        )
    except httpx.RequestError as exc:
        raise APIError("Não foi possível conectar ao servidor da biblioteca.") from exc

    if response.is_error:
        raise APIError(_error_message(response))

    if response.status_code == 204:
        return None

    try:
        return response.json()
    except ValueError as exc:
        raise APIError("A API retornou uma resposta inválida.") from exc


def _auth_token(payload: Any) -> str:
    if not isinstance(payload, dict) or not isinstance(payload.get("authToken"), str):
        raise APIError("A API não retornou um token de autenticação válido.")
    return payload["authToken"]


def login(email: str, password: str) -> str:
    return _auth_token(
        _request("POST", "/auth/login", json={"email": email, "senha": password})
    )


def signup(name: str, email: str, phone: str, password: str) -> str:
    return _auth_token(
        _request(
            "POST",
            "/auth/signup",
            json={
                "nome": name,
                "email": email,
                "telefone": phone,
                "senha": password,
            },
        )
    )


def current_user(token: str) -> dict[str, Any]:
    payload = _request("GET", "/auth/me", token=token)
    if not isinstance(payload, dict) or not isinstance(payload.get("id"), int):
        raise APIError("A API retornou dados de usuário inválidos.")
    return payload


def _category_payload(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise APIError("A API retornou uma categoria inválida.")

    category_id = payload.get("id")
    name = payload.get("nome")
    description = payload.get("descricao", "")
    if category_id is None or not isinstance(name, str) or not isinstance(description, str):
        raise APIError("A API retornou uma categoria incompleta.")

    return {
        "id": str(category_id),
        "nome": name,
        "descricao": description,
    }


def list_categories(token: str = "") -> list[dict[str, str]]:
    payload = _request("GET", "/categorias", token=token)
    if not isinstance(payload, list):
        raise APIError("A API retornou uma lista de categorias inválida.")
    return [_category_payload(category) for category in payload]


def create_category(name: str, description: str, token: str = "") -> dict[str, str]:
    payload = _request(
        "POST",
        "/categorias",
        token=token,
        json={"nome": name, "descricao": description},
    )
    return _category_payload(payload)


def update_category(
    category_id: str,
    name: str,
    description: str,
    token: str = "",
) -> dict[str, str]:
    payload = _request(
        "PATCH",
        f"/categorias/{category_id}",
        token=token,
        json={"nome": name, "descricao": description},
    )
    return _category_payload(payload)


def delete_category(category_id: str, token: str = "") -> None:
    _request("DELETE", f"/categorias/{category_id}", token=token)