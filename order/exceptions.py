import logging

from rest_framework import status
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exception, context: dict):
    response = exception_handler(exception, context)

    if response and response.status_code == status.HTTP_400_BAD_REQUEST:
        request_data = {"request_data": context["request"].data}
        logger.warning(
            "Bad Request: %s: [%s]",
            context["request"].path, context["request"].data,
            extra={
                "status_code": response.status_code,
                "http_request": context["request"],
                "json_fields": request_data,
            },
        )
        # prevent repsonse from being logged again by "django.request" logger
        setattr(response, "_has_been_logged", True)

    return response
