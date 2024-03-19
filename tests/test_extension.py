from __future__ import annotations

import asyncio

import pytest
from email_simplified import Message
from email_simplified import SMTPEmailHandler
from email_simplified import TestEmailHandler
from flask import Flask

from flask_email_simplified import EmailExtension


@pytest.mark.usefixtures("app_ctx")
def test_init_test(app: Flask) -> None:
    email = EmailExtension()
    email.init_app(app)
    assert isinstance(email.handler, TestEmailHandler)
    assert app.extensions["email"] is email


@pytest.mark.usefixtures("app_ctx")
def test_init_smtp(app: Flask) -> None:
    app.testing = False
    email = EmailExtension(app)
    assert isinstance(email.handler, SMTPEmailHandler)


@pytest.mark.usefixtures("app_ctx")
def test_send(email: EmailExtension, handler: TestEmailHandler) -> None:
    email.send(Message(subject="a"))
    email.send([Message(subject="b"), Message(subject="c")])
    assert len(handler.outbox) == 3


@pytest.mark.usefixtures("app_ctx")
def test_send_async(email: EmailExtension, handler: TestEmailHandler) -> None:
    async def send() -> None:
        await email.send_async(Message(subject="a"))
        await email.send_async([Message(subject="b"), Message(subject="c")])

    asyncio.run(send())
    assert len(handler.outbox) == 3
