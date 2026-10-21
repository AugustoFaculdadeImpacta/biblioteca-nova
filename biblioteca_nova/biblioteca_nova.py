"""Authenticated library management application."""

from typing import Any

import reflex as rx

from biblioteca_nova.api import (
    APIError,
    create_book,
    create_category,
    current_user,
    delete_book,
    delete_category,
    list_books,
    list_categories,
    login,
    signup,
    update_book,
    update_category,
)


class AuthState(rx.State):
    auth_token: str = rx.Cookie(name="auth_token", max_age=60 * 60 * 24 * 7)
    user: dict[str, Any] = {}
    session_checked: bool = False
    auth_loading: bool = False
    auth_message: str = ""
    auth_error: str = ""
    login_email: str = ""
    login_password: str = ""
    signup_name: str = ""
    signup_email: str = ""
    signup_phone: str = ""
    signup_password: str = ""

    @rx.event
    def set_login_email(self, value: str) -> None:
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str) -> None:
        self.login_password = value

    @rx.event
    def set_signup_name(self, value: str) -> None:
        self.signup_name = value

    @rx.event
    def set_signup_email(self, value: str) -> None:
        self.signup_email = value

    @rx.event
    def set_signup_phone(self, value: str) -> None:
        self.signup_phone = value

    @rx.event
    def set_signup_password(self, value: str) -> None:
        self.signup_password = value

    def _clear_auth_feedback(self) -> None:
        self.auth_message = ""
        self.auth_error = ""

    def _validate_credentials(self, email: str, password: str) -> bool:
        if not email.strip() or not password:
            self.auth_error = "Informe e-mail e senha."
            return False
        return True

    def _set_authenticated(self, token: str) -> Any:
        self.auth_token = token
        try:
            self.user = current_user(token)
        except APIError as exc:
            self.auth_token = ""
            self.user = {}
            self.auth_error = str(exc)
            return None
        self.session_checked = True
        return rx.redirect("/", replace=True)

    @rx.event
    def submit_login(self) -> Any:
        if self.auth_loading:
            return None
        self._clear_auth_feedback()
        if not self._validate_credentials(self.login_email, self.login_password):
            return None
        self.auth_loading = True
        try:
            token = login(self.login_email.strip(), self.login_password)
            return self._set_authenticated(token)
        except APIError as exc:
            self.auth_error = str(exc)
            return None
        finally:
            self.auth_loading = False

    @rx.event
    def submit_signup(self) -> Any:
        if self.auth_loading:
            return None
        self._clear_auth_feedback()
        if not self.signup_name.strip() or not self.signup_email.strip() or not self.signup_password:
            self.auth_error = "Preencha nome, e-mail e senha."
            return None
        self.auth_loading = True
        try:
            token = signup(
                self.signup_name.strip(),
                self.signup_email.strip(),
                self.signup_phone.strip(),
                self.signup_password,
            )
            return self._set_authenticated(token)
        except APIError as exc:
            self.auth_error = str(exc)
            return None
        finally:
            self.auth_loading = False

    @rx.event
    def restore_session(self) -> Any:
        if self.session_checked:
            return None
        if not self.auth_token:
            self.session_checked = True
            return rx.redirect("/login", replace=True)
        try:
            self.user = current_user(str(self.auth_token))
            self.session_checked = True
            return None
        except APIError:
            self.logout_state()
            return rx.redirect("/login", replace=True)

    @rx.event
    def logout_state(self) -> None:
        self.auth_token = ""
        self.user = {}
        self.session_checked = True
        self.auth_message = ""
        self.auth_error = ""

    @rx.event
    def logout(self) -> Any:
        self.logout_state()
        return rx.redirect("/login", replace=True)


class State(AuthState):
    categories: list[dict[str, str]] = []
    books: list[dict[str, str]] = []
    form_name: str = ""
    form_description: str = ""
    editing_id: str = ""
    is_loading: bool = False
    message: str = ""
    error_message: str = ""
    confirm_delete_open: bool = False
    pending_delete_id: str = ""
    book_form_title: str = ""
    book_form_author: str = ""
    book_form_publication_year: str = ""
    book_form_available_quantity: str = ""
    book_form_category_id: str = ""
    editing_book_id: str = ""
    book_is_loading: bool = False
    book_categories_loaded: bool = False
    book_message: str = ""
    book_error_message: str = ""
    book_confirm_delete_open: bool = False
    book_pending_delete_id: str = ""

    @rx.event
    def initialize_private_page(self) -> Any:
        redirect = self.restore_session()
        if redirect or not self.session_checked or not self.auth_token:
            return redirect
        self.load_categories()
        return None

    @rx.event
    def set_form_name(self, value: str) -> None:
        self.form_name = value

    @rx.event
    def set_form_description(self, value: str) -> None:
        self.form_description = value

    @rx.event
    def set_confirm_delete_open(self, value: bool) -> None:
        self.confirm_delete_open = value

    @rx.event
    def load_categories(self) -> None:
        if self.is_loading or not self.auth_token:
            return
        self.is_loading = True
        self.error_message = ""
        try:
            self.categories = list_categories(str(self.auth_token))
        except APIError as exc:
            self.error_message = str(exc)
        finally:
            self.is_loading = False

    @rx.event
    def initialize_books_page(self) -> Any:
        redirect = self.restore_session()
        if redirect or not self.session_checked or not self.auth_token:
            return redirect
        self.load_books()
        return None

    @rx.event
    def set_book_form_title(self, value: str) -> None:
        self.book_form_title = value

    @rx.event
    def set_book_form_author(self, value: str) -> None:
        self.book_form_author = value

    @rx.event
    def set_book_form_publication_year(self, value: str) -> None:
        self.book_form_publication_year = value

    @rx.event
    def set_book_form_available_quantity(self, value: str) -> None:
        self.book_form_available_quantity = value

    @rx.event
    def set_book_form_category_id(self, value: str) -> None:
        self.book_form_category_id = value

    @rx.event
    def set_book_confirm_delete_open(self, value: bool) -> None:
        self.book_confirm_delete_open = value
        if not value:
            self.book_pending_delete_id = ""

    def _book_rows_with_category_names(
        self,
        books: list[dict[str, str]],
        categories: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        category_names = {
            category["id"]: category["nome"] for category in categories
        }
        return [
            {
                **book,
                "categoria_nome": category_names.get(
                    book["categoria_id"], "Sem categoria"
                ),
            }
            for book in books
        ]

    @rx.event
    def load_books(self) -> None:
        if self.book_is_loading or not self.auth_token:
            return
        self.book_is_loading = True
        self.book_error_message = ""
        try:
            categories = list_categories(str(self.auth_token))
            self.categories = categories
            self.book_categories_loaded = True
            books = list_books(str(self.auth_token))
            self.books = self._book_rows_with_category_names(books, categories)
        except APIError as exc:
            self.book_error_message = str(exc)
        finally:
            self.book_is_loading = False

    def _book_form_values(
        self,
    ) -> tuple[str, str, int | None, int | None, int] | None:
        title = self.book_form_title.strip()
        author = self.book_form_author.strip()
        if not title:
            self.book_error_message = "Informe o título do livro."
            return None
        if not author:
            self.book_error_message = "Informe o autor do livro."
            return None
        if not self.book_form_category_id:
            self.book_error_message = "Selecione uma categoria para o livro."
            return None
        if not any(
            category["id"] == self.book_form_category_id
            for category in self.categories
        ):
            self.book_error_message = "Selecione uma categoria válida."
            return None

        try:
            category_id = int(self.book_form_category_id)
            publication_year = (
                int(self.book_form_publication_year.strip())
                if self.book_form_publication_year.strip()
                else None
            )
            available_quantity = (
                int(self.book_form_available_quantity.strip())
                if self.book_form_available_quantity.strip()
                else None
            )
        except ValueError:
            self.book_error_message = "Ano e quantidade devem ser números inteiros."
            return None
        if available_quantity is not None and available_quantity < 0:
            self.book_error_message = "A quantidade disponível não pode ser negativa."
            return None
        return title, author, publication_year, available_quantity, category_id

    def _reset_book_form(self) -> None:
        self.book_form_title = ""
        self.book_form_author = ""
        self.book_form_publication_year = ""
        self.book_form_available_quantity = ""
        self.book_form_category_id = ""
        self.editing_book_id = ""

    @rx.event
    def start_book_edit(self, book_id: str) -> None:
        for book in self.books:
            if book["id"] == book_id:
                self.editing_book_id = book_id
                self.book_form_title = book["titulo"]
                self.book_form_author = book["autor"]
                self.book_form_publication_year = book["ano_publicacao"]
                self.book_form_available_quantity = book["quantidade_disponivel"]
                self.book_form_category_id = book["categoria_id"]
                self.book_message = ""
                self.book_error_message = ""
                return

    @rx.event
    def cancel_book_edit(self) -> None:
        self._reset_book_form()
        self.book_error_message = ""
        self.book_message = ""

    @rx.event
    def save_book(self) -> None:
        if self.book_is_loading or not self.auth_token:
            return
        self.book_error_message = ""
        values = self._book_form_values()
        if values is None:
            return

        self.book_is_loading = True
        self.book_message = ""
        title, author, publication_year, available_quantity, category_id = values
        try:
            if self.editing_book_id:
                book = update_book(
                    self.editing_book_id,
                    title,
                    author,
                    publication_year,
                    available_quantity,
                    category_id,
                    str(self.auth_token),
                )
                self.books = self._book_rows_with_category_names(
                    [
                        book if item["id"] == self.editing_book_id else item
                        for item in self.books
                    ],
                    self.categories,
                )
                self.book_message = "Livro atualizado com sucesso."
            else:
                book = create_book(
                    title,
                    author,
                    publication_year,
                    available_quantity,
                    category_id,
                    str(self.auth_token),
                )
                self.books = self._book_rows_with_category_names(
                    [book, *self.books],
                    self.categories,
                )
                self.book_message = "Livro cadastrado com sucesso."
            self._reset_book_form()
        except APIError as exc:
            self.book_error_message = str(exc)
        finally:
            self.book_is_loading = False

    @rx.event
    def ask_delete_book(self, book_id: str) -> None:
        if self.book_is_loading:
            return
        self.book_pending_delete_id = book_id
        self.book_confirm_delete_open = True

    @rx.event
    def close_book_delete_dialog(self) -> None:
        self.book_pending_delete_id = ""
        self.book_confirm_delete_open = False

    @rx.event
    def confirm_delete_book(self) -> None:
        if (
            self.book_is_loading
            or not self.book_pending_delete_id
            or not self.auth_token
        ):
            return
        self.book_is_loading = True
        self.book_error_message = ""
        self.book_message = ""
        try:
            delete_book(self.book_pending_delete_id, str(self.auth_token))
            self.books = [
                book
                for book in self.books
                if book["id"] != self.book_pending_delete_id
            ]
            self.book_message = "Livro excluído com sucesso."
            self.close_book_delete_dialog()
        except APIError as exc:
            self.book_error_message = str(exc)
        finally:
            self.book_is_loading = False

    def _validate_form(self) -> bool:
        if not self.form_name.strip():
            self.error_message = "Informe o nome da categoria."
            return False
        self.error_message = ""
        return True

    def _reset_form(self) -> None:
        self.form_name = ""
        self.form_description = ""
        self.editing_id = ""

    @rx.event
    def save_category(self) -> None:
        if self.is_loading or not self.auth_token or not self._validate_form():
            return
        self.is_loading = True
        self.message = ""
        try:
            if self.editing_id:
                update_category(
                    self.editing_id,
                    self.form_name.strip(),
                    self.form_description.strip(),
                    str(self.auth_token),
                )
                self.message = "Categoria atualizada com sucesso."
            else:
                create_category(
                    self.form_name.strip(),
                    self.form_description.strip(),
                    str(self.auth_token),
                )
                self.message = "Categoria cadastrada com sucesso."
            self._reset_form()
            self.categories = list_categories(str(self.auth_token))
        except APIError as exc:
            self.error_message = str(exc)
        finally:
            self.is_loading = False

    @rx.event
    def start_edit(self, category_id: str) -> None:
        for category in self.categories:
            if category["id"] == category_id:
                self.editing_id = category_id
                self.form_name = category["nome"]
                self.form_description = category["descricao"]
                self.message = ""
                self.error_message = ""
                return

    @rx.event
    def cancel_edit(self) -> None:
        self._reset_form()
        self.error_message = ""
        self.message = ""

    @rx.event
    def ask_delete(self, category_id: str) -> None:
        if self.is_loading:
            return
        self.pending_delete_id = category_id
        self.confirm_delete_open = True

    @rx.event
    def close_delete_dialog(self) -> None:
        self.pending_delete_id = ""
        self.confirm_delete_open = False

    @rx.event
    def confirm_delete(self) -> None:
        if self.is_loading or not self.pending_delete_id or not self.auth_token:
            return
        self.is_loading = True
        self.message = ""
        try:
            delete_category(self.pending_delete_id, str(self.auth_token))
            self.message = "Categoria excluída com sucesso."
            self.categories = list_categories(str(self.auth_token))
        except APIError as exc:
            self.error_message = str(exc)
        finally:
            self.is_loading = False
            self.close_delete_dialog()


def auth_feedback() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AuthState.auth_message != "",
            rx.callout(AuthState.auth_message, icon="check", color_scheme="green"),
            rx.fragment(),
        ),
        rx.cond(
            AuthState.auth_error != "",
            rx.callout(AuthState.auth_error, icon="triangle_alert", color_scheme="red"),
            rx.fragment(),
        ),
        width="100%",
    )


def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Entrar", size="7"),
                rx.text("Acesse o gerenciamento da biblioteca."),
                auth_feedback(),
                rx.input(placeholder="E-mail", type="email", value=AuthState.login_email, on_change=AuthState.set_login_email, width="100%"),
                rx.input(placeholder="Senha", type="password", value=AuthState.login_password, on_change=AuthState.set_login_password, width="100%"),
                rx.button("Entrar", on_click=AuthState.submit_login, loading=AuthState.auth_loading, width="100%"),
                rx.link("Criar uma conta", href="/cadastro"),
                spacing="4",
                width="100%",
            ),
            width="min(100%, 420px)",
        ),
        min_height="100vh",
        padding="6",
    )


def signup_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Criar conta", size="7"),
                rx.text("Cadastre-se para acessar a biblioteca."),
                auth_feedback(),
                rx.input(placeholder="Nome", value=AuthState.signup_name, on_change=AuthState.set_signup_name, width="100%"),
                rx.input(placeholder="E-mail", type="email", value=AuthState.signup_email, on_change=AuthState.set_signup_email, width="100%"),
                rx.input(placeholder="Telefone (opcional)", value=AuthState.signup_phone, on_change=AuthState.set_signup_phone, width="100%"),
                rx.input(placeholder="Senha", type="password", value=AuthState.signup_password, on_change=AuthState.set_signup_password, width="100%"),
                rx.button("Cadastrar", on_click=AuthState.submit_signup, loading=AuthState.auth_loading, width="100%"),
                rx.link("Já tenho uma conta", href="/login"),
                spacing="4",
                width="100%",
            ),
            width="min(100%, 420px)",
        ),
        min_height="100vh",
        padding="6",
    )


def category_row(category: dict[str, str]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(category["nome"]),
        rx.table.cell(category["descricao"]),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", on_click=State.start_edit(category["id"]), variant="soft"),
                rx.button("Excluir", on_click=State.ask_delete(category["id"]), color_scheme="red", variant="soft"),
                spacing="2",
            )
        ),
    )


def category_form() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(rx.cond(State.editing_id, "Editar categoria", "Nova categoria"), size="5"),
            rx.input(placeholder="Nome da categoria", value=State.form_name, on_change=State.set_form_name, width="100%"),
            rx.text_area(placeholder="Descrição (opcional)", value=State.form_description, on_change=State.set_form_description, width="100%"),
            rx.hstack(
                rx.button(rx.cond(State.editing_id, "Salvar alterações", "Cadastrar"), on_click=State.save_category, loading=State.is_loading),
                rx.cond(State.editing_id, rx.button("Cancelar", on_click=State.cancel_edit, variant="soft"), rx.fragment()),
                spacing="3",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        width="100%",
    )


def category_list() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Categorias cadastradas", size="5"),
                rx.spacer(),
                rx.button("Atualizar", on_click=State.load_categories, loading=State.is_loading, variant="soft"),
                width="100%",
            ),
            rx.cond(
                State.is_loading,
                rx.center(rx.spinner(), padding="6"),
                rx.cond(
                    State.categories.length() > 0,
                    rx.table.root(
                        rx.table.header(rx.table.row(rx.table.column_header_cell("Nome"), rx.table.column_header_cell("Descrição"), rx.table.column_header_cell("Ações"))),
                        rx.table.body(rx.foreach(State.categories, category_row)),
                        width="100%",
                    ),
                    rx.center(rx.text("Nenhuma categoria cadastrada. Cadastre a primeira acima."), padding="6"),
                ),
            ),
            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
    )


def delete_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Excluir categoria?"),
            rx.alert_dialog.description("Essa ação não pode ser desfeita."),
            rx.hstack(
                rx.alert_dialog.cancel(rx.button("Cancelar", on_click=State.close_delete_dialog, variant="soft")),
                rx.alert_dialog.action(rx.button("Excluir", on_click=State.confirm_delete, color_scheme="red")),
                justify="end",
                spacing="3",
            ),
        ),
        open=State.confirm_delete_open,
        on_open_change=State.set_confirm_delete_open,
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.vstack(rx.heading("Gerenciamento de categorias", size="8"), rx.text("Organize as categorias do acervo."), align="start"),
                rx.spacer(),
                rx.link(rx.button("Livros", variant="soft"), href="/livros"),
                rx.button("Sair", on_click=AuthState.logout, color_scheme="red", variant="soft"),
                width="100%",
                align="start",
            ),
            rx.cond(State.message != "", rx.callout(State.message, icon="check", color_scheme="green"), rx.fragment()),
            rx.cond(State.error_message != "", rx.callout(State.error_message, icon="triangle_alert", color_scheme="red"), rx.fragment()),
            rx.cond(
                State.session_checked & (State.auth_token != ""),
                rx.vstack(category_form(), category_list(), delete_dialog(), spacing="6", align="stretch"),
                rx.center(rx.spinner(), min_height="50vh"),
            ),
            on_mount=State.initialize_private_page,
            spacing="6",
            align="stretch",
            max_width="960px",
            width="100%",
        ),
        padding_y="8",
    )


def book_category_option(category: dict[str, str]) -> rx.Component:
    return rx.select.item(category["nome"], value=category["id"])


def book_row(book: dict[str, str]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(book["titulo"]),
        rx.table.cell(book["autor"]),
        rx.table.cell(
            rx.cond(book["ano_publicacao"] != "", book["ano_publicacao"], "-")
        ),
        rx.table.cell(
            rx.cond(
                book["quantidade_disponivel"] != "",
                book["quantidade_disponivel"],
                "-",
            )
        ),
        rx.table.cell(book["categoria_nome"]),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Editar",
                    on_click=State.start_book_edit(book["id"]),
                    variant="soft",
                ),
                rx.button(
                    "Excluir",
                    on_click=State.ask_delete_book(book["id"]),
                    color_scheme="red",
                    variant="soft",
                ),
                spacing="2",
            )
        ),
    )


def book_form() -> rx.Component:
    return rx.cond(
        State.book_categories_loaded,
        rx.cond(
            State.categories.length() > 0,
            rx.card(
                rx.vstack(
                    rx.heading(
                        rx.cond(
                            State.editing_book_id,
                            "Editar livro",
                            "Cadastrar livro",
                        ),
                        size="5",
                    ),
                    rx.input(
                        placeholder="Título (obrigatório)",
                        value=State.book_form_title,
                        on_change=State.set_book_form_title,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Autor (obrigatório)",
                        value=State.book_form_author,
                        on_change=State.set_book_form_author,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Ano de publicação (opcional)",
                        type="number",
                        step="1",
                        value=State.book_form_publication_year,
                        on_change=State.set_book_form_publication_year,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Quantidade disponível (opcional)",
                        type="number",
                        min="0",
                        step="1",
                        value=State.book_form_available_quantity,
                        on_change=State.set_book_form_available_quantity,
                        width="100%",
                    ),
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Selecione uma categoria",
                            width="100%",
                        ),
                        rx.select.content(
                            rx.foreach(State.categories, book_category_option)
                        ),
                        value=State.book_form_category_id,
                        on_change=State.set_book_form_category_id,
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.cond(
                                State.editing_book_id,
                                "Salvar alterações",
                                "Cadastrar",
                            ),
                            on_click=State.save_book,
                            loading=State.book_is_loading,
                        ),
                        rx.cond(
                            State.editing_book_id,
                            rx.button(
                                "Cancelar edição",
                                on_click=State.cancel_book_edit,
                                variant="soft",
                            ),
                            rx.fragment(),
                        ),
                        spacing="3",
                    ),
                    spacing="3",
                    align="stretch",
                    width="100%",
                ),
                width="100%",
            ),
            rx.callout(
                rx.vstack(
                    rx.text("Cadastre uma categoria antes de adicionar um livro."),
                    rx.link("Ir para categorias", href="/"),
                    align="start",
                ),
                icon="info",
            ),
        ),
        rx.cond(
            State.book_is_loading,
            rx.center(rx.spinner(), padding="6"),
            rx.fragment(),
        ),
    )


def book_list() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Livros cadastrados", size="5"),
                rx.spacer(),
                rx.button(
                    "Atualizar",
                    on_click=State.load_books,
                    loading=State.book_is_loading,
                    variant="soft",
                ),
                width="100%",
            ),
            rx.cond(
                State.book_is_loading,
                rx.center(rx.spinner(), padding="6"),
                rx.cond(
                    State.books.length() > 0,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Título"),
                                rx.table.column_header_cell("Autor"),
                                rx.table.column_header_cell("Ano"),
                                rx.table.column_header_cell("Disponível"),
                                rx.table.column_header_cell("Categoria"),
                                rx.table.column_header_cell("Ações"),
                            )
                        ),
                        rx.table.body(rx.foreach(State.books, book_row)),
                        width="100%",
                    ),
                    rx.cond(
                        State.book_error_message == "",
                        rx.center(
                            rx.text("Nenhum livro cadastrado."),
                            padding="6",
                        ),
                        rx.fragment(),
                    ),
                ),
            ),
            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
    )


def book_delete_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Excluir livro?"),
            rx.alert_dialog.description("Essa ação não pode ser desfeita."),
            rx.hstack(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancelar",
                        on_click=State.close_book_delete_dialog,
                        variant="soft",
                    )
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Excluir",
                        on_click=State.confirm_delete_book,
                        color_scheme="red",
                        loading=State.book_is_loading,
                    )
                ),
                justify="end",
                spacing="3",
            ),
        ),
        open=State.book_confirm_delete_open,
        on_open_change=State.set_book_confirm_delete_open,
    )


def books_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Livros", size="8"),
                rx.spacer(),
                rx.link("Gerenciar categorias", href="/"),
                rx.button("Sair", on_click=AuthState.logout, color_scheme="red", variant="soft"),
                width="100%",
            ),
            rx.cond(
                State.book_message != "",
                rx.callout(State.book_message, icon="check", color_scheme="green"),
                rx.fragment(),
            ),
            rx.cond(
                State.book_error_message != "",
                rx.callout(
                    State.book_error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                ),
                rx.fragment(),
            ),
            rx.cond(
                State.session_checked & (State.auth_token != ""),
                rx.vstack(
                    book_form(),
                    book_list(),
                    book_delete_dialog(),
                    spacing="6",
                    align="stretch",
                ),
                rx.center(rx.spinner(), min_height="50vh"),
            ),
            on_mount=State.initialize_books_page,
            spacing="6",
            align="stretch",
            max_width="960px",
            width="100%",
        ),
        padding_y="8",
    )


app = rx.App()
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/cadastro")
app.add_page(index, route="/")
app.add_page(books_page, route="/livros")