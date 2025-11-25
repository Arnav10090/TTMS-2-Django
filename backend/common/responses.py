"""
Standard API response formatting for TTMS and PTMS.
"""

from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data=None, message=None, status=http_status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        data: Response data/payload
        message: Success message
        status: HTTP status code
    
    Returns:
        DRF Response object
    
    Example:
        return success_response(data={'user_id': 123}, message='User created')
    """
    response_data = {
        'success': True,
        'status_code': status,
    }
    
    if message:
        response_data['message'] = message
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status)


def error_response(message, error_code=None, details=None, status=http_status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        error_code: Error code for client handling
        details: Additional error details
        status: HTTP status code
    
    Returns:
        DRF Response object
    
    Example:
        return error_response('Invalid user', error_code='INVALID_USER', status=400)
    """
    response_data = {
        'success': False,
        'status_code': status,
        'message': message,
    }
    
    if error_code:
        response_data['error_code'] = error_code
    
    if details:
        response_data['details'] = details
    
    return Response(response_data, status=status)


def list_response(items, count=None, page=None, message=None, status=http_status.HTTP_200_OK):
    """
    Create a standardized list response.
    
    Args:
        items: List of items
        count: Total count of items
        page: Current page info
        message: Optional message
        status: HTTP status code
    
    Returns:
        DRF Response object
    
    Example:
        return list_response(items=vehicles, count=100, page=1)
    """
    response_data = {
        'success': True,
        'status_code': status,
        'data': items,
    }
    
    if count is not None:
        response_data['count'] = count
    
    if page is not None:
        response_data['page'] = page
    
    if message:
        response_data['message'] = message
    
    return Response(response_data, status=status)


def paginated_response(paginator, queryset, serializer_class, request):
    """
    Create a paginated response.
    
    Args:
        paginator: Pagination instance
        queryset: QuerySet to paginate
        serializer_class: Serializer class for items
        request: Django request object
    
    Returns:
        DRF Response object
    
    Example:
        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        return paginated_response(paginator, page, VehicleSerializer, request)
    """
    serializer = serializer_class(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


def created_response(data, message='Resource created successfully', status=http_status.HTTP_201_CREATED):
    """
    Create a standardized created response.
    
    Args:
        data: Created resource data
        message: Success message
        status: HTTP status code (defaults to 201)
    
    Returns:
        DRF Response object
    """
    return success_response(data=data, message=message, status=status)


def updated_response(data, message='Resource updated successfully', status=http_status.HTTP_200_OK):
    """
    Create a standardized updated response.
    
    Args:
        data: Updated resource data
        message: Success message
        status: HTTP status code (defaults to 200)
    
    Returns:
        DRF Response object
    """
    return success_response(data=data, message=message, status=status)


def deleted_response(message='Resource deleted successfully', status=http_status.HTTP_204_NO_CONTENT):
    """
    Create a standardized deleted response.
    
    Args:
        message: Success message
        status: HTTP status code (defaults to 204)
    
    Returns:
        DRF Response object
    """
    return success_response(data=None, message=message, status=status)
