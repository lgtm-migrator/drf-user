"""Custom Managers for drf-user"""
from typing import Optional

from django.contrib.auth.base_user import BaseUserManager

from drf_user import update_user_settings
from drf_user.models import User


class UserManager(BaseUserManager):
    """
    UserManager class for Custom User Model

    Author: Himanshu Shankar (https://himanshus.com)
    Source: Can't find link but the following solution is inspired
    from a solution provided on internet.
    """

    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        email: str,
        name: str,
        password: Optional[str] = None,
        mobile: Optional[str] = None,
        **kwargs
    ) -> User:
        """
        Creates and saves a User with given details
        """
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, name=name, mobile=mobile, **kwargs
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        email: str,
        name: str,
        password: Optional[str] = None,
        mobile: Optional[str] = None,
        **kwargs
    ) -> User:
        """
        Creates a normal user considering the specified user settings
        from Django Project's settings.py

        Parameters
        ----------
        username: str
        email: str
        password: str
        name: str
        mobile: str, optional
        kwargs

        Returns
        -------
        User Instance
        """
        vals = update_user_settings()

        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_active", vals.get("DEFAULT_ACTIVE_STATE", False))

        return self._create_user(
            username=username,
            email=email,
            name=name,
            password=password,
            mobile=mobile,
            **kwargs
        )

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str,
        name: str,
        mobile: Optional[str] = None,
        **kwargs
    ) -> User:
        """
        Creates a super user considering the specified user settings
        from Django Project's settings.py

        Parameters
        ----------
        username: str
        email: str
        password: str
        name: str
        mobile: str, optional
        kwargs

        Returns
        -------
        User Instance
        """
        vals = update_user_settings()

        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", vals.get("DEFAULT_ACTIVE_STATE", False))

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(
            username=username,
            email=email,
            name=name,
            password=password,
            mobile=mobile,
            **kwargs
        )
