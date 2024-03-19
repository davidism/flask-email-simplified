# Getting Started

These docs cover setting up Flask-Email-Simplified. See
[Email-Simplified's docs][docs] for information on building and sending
messages, adding handlers, and more.

[docs]: https://email-simplified.readthedocs.io

## Initialize the Application

First, set up your Flask/Quart application (or application factory) and the
{class}`.EmailExtension` instance.

This extension follows the common pattern of Flask extension setup. Either
immediately pass an app to {class}`.EmailExtension`, or call
{meth}`~.EmailExtension.init_app` later.

```python
from flask_email_simplified import EmailExtension

email = EmailExtension()
email.init_app(app)  # call in the app factory if you're using that pattern
```

By default, an SMTP handler for `localhost:25` is created. This can be
configured, see {doc}`config`.

### Local Mail Server

The SMTP handler will fail to send if there's no server at the configured
location. During development, you can use a tool such as [mailcatcher], which
acts as a simple, local SMTP server as well as a UI for displaying any messages
it receives.

[mailcatcher]: https://github.com/sj26/mailcatcher

## Create a Message

Email-Simplified provides a {class}`.Message` class that can be used to define
the fields of a "standard" email MIME structure. It supports a text part, HTML
part, HTML inline attachments, and download attachments.

```python
from email_simplified import Message

message = Message(
    subject="Hello, World!",
    text="This is an example message.",
    to=["example@localhost"],
)
```

Alternatively, you may need to create a {class}`email.message.EmailMessage`
directly if you need a more complex, non-standard MIME structure.
Email-Simplified handlers can support sending both types of messages. SMTP
handlers will always convert to MIME, but other handlers for HTTP-based services
may be able to make an API call or send the MIME content directly depending on
the message structure.

## Send a Message

Call the extension's {meth}`~.EmailExtension.send` method to send the message
you created. You can pass a single message or a list of messages. Sending a list
of messages is more efficient than making multiple `send` calls, as it reuses
the same connection.

```python
email.send(message)
```

### Performance

Sending messages can be a slow operation, which will delay the view from
returning a response. It can be useful to send messages in background tasks,
using a system such as [RQ] or [Celery].

[RQ]: https://python-rq.org
[Celery]: https://docs.celeryq.dev

### Async

If you're calling this from an `async` view, you should `await`
{meth}`~.EmailExtension.send_async` instead. However, this requires the handler
to support async sending.

The default `smtp` handler does not support async, but a handler that uses
[aiosmtplib] can be written. Alternatively, use {func}`asyncio.to_thread` to run
the sync `send` function in a thread.

[aiosmtplib]: https://pypi.org/project/aiosmtplib/
