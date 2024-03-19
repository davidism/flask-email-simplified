# Flask-Email-Simplified

Flask-Email-Simplified is a [Flask]/[Quart] extension that provides email
sending capability using the [Email-Simplified] library.

Email-Simplified provides a much simpler interface for creating and sending
email messages compared to Python's `email` and `smtplib` modules. It also
defines an interface for using other email sending providers that offer an API
other than SMTP.

[Flask]: https://flask.palletsprojects.com
[Quart]: https://quart.palletsprojects.com
[Email-Simplified]: https://email-simplified.readthedocs.io

## Install

Install from [PyPI]:

```text
$ pip install flask-email-simplified
```

[PyPI]: https://pypi.org/project/flask-email-simiplified

## Example

```python
from email_simplified import Message
from flask import Flask
from flask_email_simplified import EmailExtension

app = Flask(__name__)
app.config["EMAIL_HOST"] = "localhost"
app.config["EMAIL_PORT"] = 25
email = EmailExtension(app)

@app.get("/send")
def hello():
    message = Message(
        subject="Hello",
        text="Hello, World!",
        to=["world@example.test"],
    )
    email.send(message)
    return "Hello, World!"
```
