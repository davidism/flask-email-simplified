from __future__ import annotations

import os
import typing as t
from pathlib import Path

import pytest
from email_simplified import TestEmailHandler
from flask import Flask
from flask.ctx import AppContext

from flask_email_simplified import EmailExtension


@pytest.fixture
def app(request: pytest.FixtureRequest, tmp_path: Path) -> Flask:
    app = Flask(request.module.__name__, instance_path=os.fspath(tmp_path / "instance"))  # pyright: ignore
    app.testing = True
    return app


@pytest.fixture
def app_ctx(app: Flask) -> t.Iterator[AppContext]:
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def email(app: Flask) -> EmailExtension:
    return EmailExtension(app)


@pytest.fixture
def handler(app: Flask, email: EmailExtension) -> TestEmailHandler:
    with app.app_context():
        handler = email.handler

    assert isinstance(handler, TestEmailHandler)
    return handler
