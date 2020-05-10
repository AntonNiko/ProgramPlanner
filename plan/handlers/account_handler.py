from django.contrib.auth import authenticate, login, logout


class AccountHandler:
    """
    Handles requests relating to user accounts, and performs actions to fulfill
    the specified requests.
    """

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
        password = request.POST('password', None)

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
