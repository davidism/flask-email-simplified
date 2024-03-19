from __future__ import annotations

import typing as t

import pytest
from email_simplified.handlers import EmailHandler
from flask import Flask

from flask_email_simplified import EmailExtension


class CustomEmailHandler(EmailHandler):
    def __init__(self, **kwargs: t.Any) -> None:
        self.config = kwargs

    @classmethod
    def from_config(cls, config: dict[str, t.Any]) -> t.Self:
        return cls(**config)


@pytest.fixture
def app(app: Flask) -> Flask:
    app.testing = False
    app.config |= {
        "EMAIL_HANDLER": CustomEmailHandler,
        "EMAIL_HOST": "localhost",
        "EMAIL_PORT": 25,
    }
    return app


@pytest.mark.usefixtures("app_ctx")
def test_config(email: EmailExtension) -> None:
    handler = email.handler
    assert isinstance(handler, CustomEmailHandler)
    assert handler.config == {
        "handler": CustomEmailHandler,
        "host": "localhost",
        "port": 25,
    }
