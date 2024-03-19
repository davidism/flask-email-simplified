# Configuration

Configuration for Flask-Email-Simplified uses the following Flask config keys.

```{module} flask_email_simplified.config
```

```{data} EMAIL_HANDLER
Selects the {class}`.EmailHandler` class to use. By default, this is ``"smtp"``
{class}`.SMTPEmailHandler`.
```

```{data} EMAIL_
Any config key with the ``EMAIL_`` prefix will be passed on to the handler's
{meth}`~.EmailHandler.from_config` method. The prefix is removed and each key is
converted to lowercase. See the specific handler's documentation for what config
keys are used.
```

```{data} EMAIL_TESTING_KEEP_HANDLER
By default, when {class}`.Flask.testing` is ``True``, the handler will be set to
{class}`.TestEmailHandler`. If this setting is ``True``, the configured handler
will be kept.
```
