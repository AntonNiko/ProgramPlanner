from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class AccountHandler:
    """
    Handles requests relating to user accounts, and performs actions to fulfill
    the specified requests.
    """

    @staticmethod
    def register(request):
        """

        :param request:
        :return:
        """

        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        assert username is not None
        assert email is not None
        assert password is not None

        # TODO: Determine what failure conditions to handle
        user = User.objects.create_user(username=username, email=email, password=password)

        return True

    @staticmethod
    def delete(request):
        """

        :param request:
        :return:
        """

        username = request.POST.get('username', None)

        assert username is not None

        # TODO: Validate the terms and ensure proper data returned for action
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False

        user.delete()
        return True

    @staticmethod
    def login(request):
        """
        Attempts to login the user, given the request provided.

        Args:
         - request: An `HttpRequest` object.
        Returns:
         - `True` if the user is successfully logged in, `False` otherwise.
        Raises:
         - `AssertionError`: If the username or password is not present in the request object.
        """

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

    @staticmethod
    def logout(request):
        """
        Logs the user out.
        """
        logout(request)
        return True
