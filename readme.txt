- First you have to configure your settings.py file (For sending Email).
[
    import sys
    TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

    #after override django default user model you have to set your AUTH_USER_MODEL in your settings. 
    AUTH_USER_MODEL = 'accounts.User'

    # Email Sending Setup
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your host email'
    EMAIL_HOST_PASSWORD = 'your password'
    EMAIL_FROM_USER = 'your host email'
]

- utils.py file created for token genarator. Copy that file.
- models.py file modified, because of adding new field to User model.
- forms.py file not modified. (Remember, I've used django AuthencationForm() with crispy_form for login)
- urls.py file modified and added new url paths.
- A lot of modification in views.py file. (which function for what purpose Commented in code).
    - register function changed added some lines of code.
    - login_user function created new.
    - activate_user function created new.
    - send_activation_email fuction created new.

TEMPLATES:
- register.html file not changed
- login form changed and used crispy_form. To use crispy_form you have to install it first then have to include it on your INSTALLED_APPS in settings.py file.
[
    #also have include this line in your settings.py file.
    CRISPY_TEMPLATE_PACK = 'bootstrap4'
]
- activate.html new file created. Have to copy that file.
- activation_failed.html new file created. (Have to copy that also, if you wanted to show activation_failed) 
NOTE: Ignore base.html, index.html, navbar.html