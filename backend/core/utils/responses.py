from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data=None, message=None, status=http_status.HTTP_200_OK):
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        status: HTTP status code
    
    Returns:
        Response: DRF Response object
    """
    response_data = {
        'success': True,
        'status': status,
    }
    
    if message:
        response_data['message'] = message
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status)


def error_response(message, error_code=None, details=None, status=http_status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        error_code: Error code for client handling
        details: Additional error details
        status: HTTP status code
    
    Returns:
        Response: DRF Response object
    """
    response_data = {
        'success': False,
        'status': status,
        'message': message,
    }
    
    if error_code:
        response_data['error_code'] = error_code
    
    if details:
        response_data['details'] = details
    
    return Response(response_data, status=status)
