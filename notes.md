# Useful Notes <!-- omit in toc -->
## Contents <!-- omit in toc -->
- [Early Stages](#early-stages)
- [Authentication](#authentication)
- [Set up Home Page](#set-up-home-page)
## Early Stages
1. Create workspace using CI template
2. Install Django:
   ```shell
   pip3 install django
   ```
3. Create the project:
   ```shell
   django-admin startproject <projectname> .
   ```
   (The dot instructs tot create the project in the current directory)
4. Create a .gitignore file and include *.sqlite3, *.pyc and pycache
5. Perform initial migrations:
   ```shell
   python3 manage.py migrate
   ```
6. Create a superuser to use django admin:
   ```
   python3 manage.py createsuperuser
   ```
7. Commit to github   

## Authentication
1. Install allauth:
   ```shell
   pip3 install django-allauth==0.41.0
   ```
2. Update allauth settings in settings.py
3. Update urls.py to:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
   ]
   ```

4. Log in to the django admin dashboard and update the domain name and display name. (Reason for this not clear in video)
5. Update EMAIL_BACKEND settings in settings.py:
   ```py
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```
   This prevents the default sending of emails to verify new accounts and instead sendsthem to console (this is for dev phase only).
6. Add to settings.py:
   ```py
   ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
   ACCOUNT_EMAIL_REQUIRED = True
   ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
   ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
   ACCOUNT_USERNAME_MIN_LENGTH = 4
   LOGIN_URL = '/accounts/login'
   LOGIN_REDIRECT_URL = '/'
   ```

## Set up Home Page

**Note**: Anything installed with pip goes to sitepackages directory.

1. Copy all the allauth templates from where they are in the site packages directory to the templates/allauth folder. There, we can customize them as required and not start from scratch.
   ```shell
   cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth/
   ```
