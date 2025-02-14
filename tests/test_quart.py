import asyncio

import pytest
from email_simplified import Message
from email_simplified import SMTPEmailHandler
from flask import Flask
from quart import Quart

from flask_email_simplified import EmailExtension


def test_init() -> None:
    app = Quart(__name__)
    app.testing = True
    app.config["EMAIL_USERNAME"] = "test"
    app.config["EMAIL_TESTING_KEEP_HANDLER"] = True
    email = EmailExtension(app)

    async def inner() -> None:
        with pytest.raises(RuntimeError):
            assert email.handler

        async with app.app_context():
            handler = email.handler

        assert isinstance(handler, SMTPEmailHandler)
        assert handler.username == "test"

    asyncio.run(inner())


def test_send() -> None:
    app = Quart(__name__)
    app.testing = True
    email = EmailExtension(app)

    async def inner() -> None:
        async with app.app_context():
            await email.send_async(Message(subject="a"))
            assert email.handler.outbox  # type: ignore[attr-defined]

    asyncio.run(inner())


def test_no_init() -> None:
    email = EmailExtension()

    with pytest.raises(RuntimeError):
        assert email.handler


def test_both_init() -> None:
    email = EmailExtension()
    flask_app = Flask(__name__)
    quart_app = Quart(__name__)
    email.init_app(flask_app)
    email.init_app(quart_app)

    with pytest.raises(RuntimeError):
        assert email.handler

    with flask_app.app_context():
        flask_handler: object = email.handler

    quart_handler: object = None

    async def inner() -> None:
        nonlocal quart_handler

        async with quart_app.app_context():
            quart_handler = email.handler

    asyncio.run(inner())
    assert quart_handler is not None
    assert flask_handler is not quart_handler
