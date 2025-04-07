import logging
import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

logger = logging.getLogger(__name__)


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)

    if response is None:
        if isinstance(exception, DjangoValidationError):
            response = Response({'detail': exception.messages},
                                status=status.HTTP_400_BAD_REQUEST)

    if response and response.status_code == status.HTTP_400_BAD_REQUEST:
        request_data = {"request_data": context["request"].data}

        # Get more detailed error info
        error_detail = {
            'error': str(exception),
            'error_type': exception.__class__.__name__,
            'view': context['view'].__class__.__name__,
            'request_method': context['request'].method,
            'request_path': context['request'].path,
            'request_data': context['request'].data,
        }

        # Add validation errors if present
        if hasattr(exception, 'detail'):
            if isinstance(exception.detail, dict):
                error_detail['validation_errors'] = exception.detail
            else:
                error_detail['validation_errors'] = {
                    'detail': exception.detail}

        # Log the error with full context
        logger.warning(
            "Bad Request: %(path)s: [%(data)s]\nDetails: %(details)s",
            {
                'path': context['request'].path,
                'data': context['request'].data,
                'details': error_detail
            },
            extra={
                'status_code': response.status_code,
                'http_request': context['request'],
                'json_fields': error_detail,
            },
        )

        # Update response data with more details
        if isinstance(response.data, dict):
            response.data.update(error_detail)
        else:
            response.data = error_detail

        # prevent response from being logged again by "django.request" logger
        setattr(response, "_has_been_logged", True)

    return response
