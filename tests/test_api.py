import unittest
from unittest.mock import patch

import httpx

from biblioteca_nova import api


class BookAPITests(unittest.TestCase):
    def test_list_books_normalizes_contract_fields(self) -> None:
        response = httpx.Response(
            200,
            json=[
                {
                    "id": 7,
                    "titulo": "O livro",
                    "autor": "A autora",
                    "ano_publicacao": 2020,
                    "quantidade_disponivel": 3,
                    "categoria_id": 2,
                }
            ],
        )
        with patch(
            "biblioteca_nova.api.httpx.request", return_value=response
        ) as request:
            books = api.list_books()

        self.assertEqual(
            books,
            [
                {
                    "id": "7",
                    "titulo": "O livro",
                    "autor": "A autora",
                    "ano_publicacao": "2020",
                    "quantidade_disponivel": "3",
                    "categoria_id": "2",
                }
            ],
        )
        self.assertEqual(
            request.call_args.args[:2],
            ("GET", f"{api.XANO_BASE_URL}/livro"),
        )

    def test_list_books_accepts_nullable_contract_fields(self) -> None:
        response = httpx.Response(
            200,
            json=[
                {
                    "id": 7,
                    "titulo": None,
                    "autor": None,
                    "ano_publicacao": None,
                    "quantidade_disponivel": None,
                    "categoria_id": None,
                }
            ],
        )
        with patch("biblioteca_nova.api.httpx.request", return_value=response):
            books = api.list_books()

        self.assertEqual(books[0]["titulo"], "")
        self.assertEqual(books[0]["autor"], "")
        self.assertEqual(books[0]["categoria_id"], "")
        self.assertEqual(books[0]["ano_publicacao"], "")
        self.assertEqual(books[0]["quantidade_disponivel"], "")

    def test_create_book_sends_contract_payload(self) -> None:
        response = httpx.Response(
            200,
            json={
                "id": 8,
                "titulo": "O livro",
                "autor": "A autora",
                "ano_publicacao": 2020,
                "quantidade_disponivel": 3,
                "categoria_id": 2,
            },
        )
        with patch(
            "biblioteca_nova.api.httpx.request", return_value=response
        ) as request:
            book = api.create_book("O livro", "A autora", 2020, 3, 2)

        self.assertEqual(book["id"], "8")
        self.assertEqual(
            request.call_args.args[:2],
            ("POST", f"{api.XANO_BASE_URL}/livro"),
        )
        self.assertEqual(
            request.call_args.kwargs["json"],
            {
                "titulo": "O livro",
                "autor": "A autora",
                "ano_publicacao": 2020,
                "quantidade_disponivel": 3,
                "categoria_id": 2,
            },
        )

    def test_update_book_uses_put_endpoint(self) -> None:
        response = httpx.Response(
            200,
            json={
                "id": 8,
                "titulo": "Atualizado",
                "autor": "A autora",
                "ano_publicacao": None,
                "quantidade_disponivel": 0,
                "categoria_id": 2,
            },
        )
        with patch(
            "biblioteca_nova.api.httpx.request", return_value=response
        ) as request:
            book = api.update_book("8", "Atualizado", "A autora", None, 0, 2)

        self.assertEqual(book["titulo"], "Atualizado")
        self.assertEqual(
            request.call_args.args[:2],
            ("PUT", f"{api.XANO_BASE_URL}/livro/8"),
        )

    def test_delete_book_uses_delete_endpoint(self) -> None:
        response = httpx.Response(204)
        with patch(
            "biblioteca_nova.api.httpx.request", return_value=response
        ) as request:
            api.delete_book("8")

        self.assertEqual(
            request.call_args.args[:2],
            ("DELETE", f"{api.XANO_BASE_URL}/livro/8"),
        )

    def test_rejects_invalid_book_response(self) -> None:
        response = httpx.Response(200, json=[{"titulo": "Sem identificador"}])
        with patch("biblioteca_nova.api.httpx.request", return_value=response):
            with self.assertRaises(api.APIError):
                api.list_books()

    def test_rejects_incomplete_book_response(self) -> None:
        response = httpx.Response(200, json=[{"id": 7, "titulo": "O livro"}])
        with patch("biblioteca_nova.api.httpx.request", return_value=response):
            with self.assertRaises(api.APIError):
                api.list_books()

    def test_rejects_non_list_response(self) -> None:
        response = httpx.Response(200, json={"livros": []})
        with patch("biblioteca_nova.api.httpx.request", return_value=response):
            with self.assertRaises(api.APIError):
                api.list_books()

    def test_reports_http_errors(self) -> None:
        response = httpx.Response(403, json={"message": "Acesso negado"})
        with patch("biblioteca_nova.api.httpx.request", return_value=response):
            with self.assertRaisesRegex(api.APIError, "Acesso negado"):
                api.list_books()

    def test_rejects_invalid_book_id_before_request(self) -> None:
        with patch("biblioteca_nova.api.httpx.request") as request:
            with self.assertRaises(api.APIError):
                api.delete_book("invalid")

        request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
