from rest_framework.exceptions import APIException

class CantFollowYourself(APIException):
    status_code = 403
    default_detail = "You Can't Follow Yourself."
    default_code = "Forbidden"
