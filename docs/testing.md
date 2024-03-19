# Testing

During testing, you don't want to actually send messages. By default, the
handler will be switched to {class}`.TestEmailHandler` when
{attr}`.Flask.testing` is `True`. This stores all messages in a list called
{attr}`~.TestEmailHandler.outbox`. After sending messages, you can check that
the length or content of the outbox is what you expect.

It's easiest to take advantage of this when using the app factory pattern.

```python
from email_simplified import Message
from flask import Flask
from flask_email_simplified import EmailExtension

email = EmailExtension()

def create_app(testing: bool = False):
    app = Flask(__name__)
    app.testing = testing
    email.init_app(app)
    return app

def test_send():
    app = create_app(testing=True)

    with app.app_context():
        email.send(Message(...))

    assert len(email.handler.outbox) == 1
```

## Keeping the Handler

You can set {data}`.EMAIL_TESTING_KEEP_HANDLER` to keep the existing handler
rather than replacing it with the test handler. In this case, you'll need to
set up a test server or mock internals in order to avoid sending externally.
