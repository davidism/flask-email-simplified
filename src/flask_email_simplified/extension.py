from __future__ import annotations

from email.message import EmailMessage as _EmailMessage
from weakref import WeakKeyDictionary

from email_simplified import get_handler_class
from email_simplified import Message
from email_simplified.handlers.base import EmailHandler
from flask import current_app
from flask.sansio.app import App  # pyright: ignore


class EmailExtension:
    """Flask extension that manages sending email messages with the
    Email-Simplified library.
    """

    def __init__(self, app: App | None = None) -> None:
        self._handlers: WeakKeyDictionary[App, EmailHandler] = WeakKeyDictionary()

        if app is not None:
            self.init_app(app)

    def init_app(self, app: App) -> None:
        """Configure the extension with the given Flask application.

        Imports the handler class identified by :data:`.EMAIL_HANDLER` using
        :func:`.get_email_handler`. Calls
        :meth:`~email_simplified.handlers.base.EmailHandler.from_config`
        to create a handler instance. Config is any key prefixed with
        ``EMAIL_`` with the prefix removed and the key converted to lower case.

        This extension is added to :attr:`.Flask.extensions` with the
        ``"email"`` key.

        When :attr:`.Flask.testing` is ``True``, the handler will always be
        :class:`.TestEmailHandler` unless ``EMAIL_TESTING_KEEP_HANDLER`` is
        ``True``.
        """
        config = app.config.get_namespace("EMAIL_")

        if app.testing and not config.get("testing_keep_handler", False):
            handler_str = "test"
        else:
            handler_str = config.get("handler", "smtp")

        handler_cls = get_handler_class(handler_str)
        handler = handler_cls.from_config(config)
        self._handlers[app] = handler
        app.extensions["email"] = self

    @property
    def handler(self) -> EmailHandler:
        """The email handler associated with :data:`.current_app`.

        When not in an active request or CLI command, an app context must be
        pushed manually.
        """
        return self._handlers[current_app._get_current_object()]  # type: ignore[attr-defined]

    def send(
        self, messages: Message | _EmailMessage | list[Message | _EmailMessage]
    ) -> None:
        """Send one or more messages with the email handler associated with
        :data:`.current_app`.

        Messages should typically be :class:`.Message` instances. However, they
        may also be :class:`email.message.EmailMessage` instances for cases
        where a non-standard MIME construction is needed.
        """
        if isinstance(messages, Message | _EmailMessage):
            messages = [messages]

        self.handler.send(messages)

    async def send_async(
        self, messages: Message | _EmailMessage | list[Message | _EmailMessage]
    ) -> None:
        """Send one or more email messages, as with :meth:`send`, in an
        ``async`` context. May not be implemented by some handlers.
        """
        if isinstance(messages, Message | _EmailMessage):
            messages = [messages]

        await self.handler.send_async(messages)
