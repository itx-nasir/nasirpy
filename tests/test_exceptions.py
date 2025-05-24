import pytest
from nasirpy.exceptions import HTTPException, NotFoundError, BadRequestError


class TestHTTPException:
    """Test cases for HTTPException base class."""
    
    def test_http_exception_with_custom_detail(self):
        """Test HTTPException with custom detail message."""
        exc = HTTPException(status_code=400, detail="Custom error message")
        
        assert exc.status_code == 400
        assert exc.detail == "Custom error message"
    
    def test_http_exception_with_default_detail(self):
        """Test HTTPException with default detail messages."""
        test_cases = [
            (404, "Not Found"),
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (500, "Internal Server Error")
        ]
        
        for status_code, expected_detail in test_cases:
            exc = HTTPException(status_code=status_code)
            assert exc.status_code == status_code
            assert exc.detail == expected_detail
    
    def test_http_exception_unknown_status_code(self):
        """Test HTTPException with unknown status code."""
        exc = HTTPException(status_code=418)  # I'm a teapot
        
        assert exc.status_code == 418
        assert exc.detail == "Unknown Error"
    
    def test_http_exception_none_detail(self):
        """Test HTTPException when detail is explicitly None."""
        exc = HTTPException(status_code=404, detail=None)
        
        assert exc.status_code == 404
        assert exc.detail == "Not Found"  # Should use default
    
    def test_http_exception_empty_string_detail(self):
        """Test HTTPException with empty string detail."""
        exc = HTTPException(status_code=400, detail="")
        
        assert exc.status_code == 400
        assert exc.detail == ""  # Should use the empty string, not default
    
    def test_http_exception_inheritance(self):
        """Test that HTTPException inherits from Exception."""
        exc = HTTPException(status_code=500, detail="Server error")
        
        assert isinstance(exc, Exception)
        assert isinstance(exc, HTTPException)
    
    def test_http_exception_str_representation(self):
        """Test string representation of HTTPException."""
        exc = HTTPException(status_code=404, detail="Not Found")
        
        # Should be able to convert to string without error
        str_repr = str(exc)
        assert isinstance(str_repr, str)
    
    def test_http_exception_raise(self):
        """Test that HTTPException can be raised and caught."""
        with pytest.raises(HTTPException) as exc_info:
            raise HTTPException(status_code=400, detail="Test error")
        
        exception = exc_info.value
        assert exception.status_code == 400
        assert exception.detail == "Test error"


class TestNotFoundError:
    """Test cases for NotFoundError exception."""
    
    def test_not_found_error_with_custom_detail(self):
        """Test NotFoundError with custom detail message."""
        exc = NotFoundError(detail="Custom not found message")
        
        assert exc.status_code == 404
        assert exc.detail == "Custom not found message"
    
    def test_not_found_error_with_default_detail(self):
        """Test NotFoundError with default detail message."""
        exc = NotFoundError()
        
        assert exc.status_code == 404
        assert exc.detail == "Not Found"
    
    def test_not_found_error_with_none_detail(self):
        """Test NotFoundError when detail is explicitly None."""
        exc = NotFoundError(detail=None)
        
        assert exc.status_code == 404
        assert exc.detail == "Not Found"  # Should use default
    
    def test_not_found_error_inheritance(self):
        """Test that NotFoundError inherits from HTTPException."""
        exc = NotFoundError(detail="Resource not found")
        
        assert isinstance(exc, Exception)
        assert isinstance(exc, HTTPException)
        assert isinstance(exc, NotFoundError)
    
    def test_not_found_error_raise(self):
        """Test that NotFoundError can be raised and caught."""
        with pytest.raises(NotFoundError) as exc_info:
            raise NotFoundError(detail="Page not found")
        
        exception = exc_info.value
        assert exception.status_code == 404
        assert exception.detail == "Page not found"
    
    def test_not_found_error_catch_as_http_exception(self):
        """Test that NotFoundError can be caught as HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            raise NotFoundError(detail="Resource missing")
        
        exception = exc_info.value
        assert isinstance(exception, NotFoundError)
        assert exception.status_code == 404
        assert exception.detail == "Resource missing"


class TestBadRequestError:
    """Test cases for BadRequestError exception."""
    
    def test_bad_request_error_with_custom_detail(self):
        """Test BadRequestError with custom detail message."""
        exc = BadRequestError(detail="Invalid input data")
        
        assert exc.status_code == 400
        assert exc.detail == "Invalid input data"
    
    def test_bad_request_error_with_default_detail(self):
        """Test BadRequestError with default detail message."""
        exc = BadRequestError()
        
        assert exc.status_code == 400
        assert exc.detail == "Bad Request"
    
    def test_bad_request_error_with_none_detail(self):
        """Test BadRequestError when detail is explicitly None."""
        exc = BadRequestError(detail=None)
        
        assert exc.status_code == 400
        assert exc.detail == "Bad Request"  # Should use default
    
    def test_bad_request_error_inheritance(self):
        """Test that BadRequestError inherits from HTTPException."""
        exc = BadRequestError(detail="Validation failed")
        
        assert isinstance(exc, Exception)
        assert isinstance(exc, HTTPException)
        assert isinstance(exc, BadRequestError)
    
    def test_bad_request_error_raise(self):
        """Test that BadRequestError can be raised and caught."""
        with pytest.raises(BadRequestError) as exc_info:
            raise BadRequestError(detail="Invalid JSON")
        
        exception = exc_info.value
        assert exception.status_code == 400
        assert exception.detail == "Invalid JSON"
    
    def test_bad_request_error_catch_as_http_exception(self):
        """Test that BadRequestError can be caught as HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            raise BadRequestError(detail="Malformed request")
        
        exception = exc_info.value
        assert isinstance(exception, BadRequestError)
        assert exception.status_code == 400
        assert exception.detail == "Malformed request"


class TestExceptionIntegration:
    """Integration tests for exception handling."""
    
    def test_multiple_exception_types(self):
        """Test handling multiple exception types."""
        exceptions = [
            HTTPException(status_code=500, detail="Server error"),
            NotFoundError(detail="Page not found"),
            BadRequestError(detail="Invalid data")
        ]
        
        for exc in exceptions:
            assert hasattr(exc, 'status_code')
            assert hasattr(exc, 'detail')
            assert isinstance(exc, HTTPException)
    
    def test_exception_hierarchy(self):
        """Test the exception inheritance hierarchy."""
        # All should inherit from HTTPException
        assert issubclass(NotFoundError, HTTPException)
        assert issubclass(BadRequestError, HTTPException)
        
        # All should inherit from Exception
        assert issubclass(HTTPException, Exception)
        assert issubclass(NotFoundError, Exception)
        assert issubclass(BadRequestError, Exception)
    
    def test_exception_equality(self):
        """Test exception equality based on status code and detail."""
        exc1 = HTTPException(status_code=404, detail="Not Found")
        exc2 = HTTPException(status_code=404, detail="Not Found")
        exc3 = HTTPException(status_code=404, detail="Different message")
        exc4 = HTTPException(status_code=500, detail="Not Found")
        
        # Note: Python exceptions don't have built-in equality,
        # but we can test their attributes
        assert exc1.status_code == exc2.status_code
        assert exc1.detail == exc2.detail
        assert exc1.detail != exc3.detail
        assert exc1.status_code != exc4.status_code
    
    def test_exception_with_various_status_codes(self):
        """Test HTTPException with various HTTP status codes."""
        status_codes = [200, 201, 301, 302, 400, 401, 403, 404, 405, 500, 502, 503]
        
        for status_code in status_codes:
            exc = HTTPException(status_code=status_code)
            assert exc.status_code == status_code
            assert isinstance(exc.detail, str)
            assert len(exc.detail) > 0  # Should have some detail
    
    def test_custom_exception_subclassing(self):
        """Test creating custom exception subclasses."""
        class UnauthorizedError(HTTPException):
            def __init__(self, detail: str = None):
                super().__init__(401, detail)
        
        class ForbiddenError(HTTPException):
            def __init__(self, detail: str = None):
                super().__init__(403, detail)
        
        # Test custom exceptions
        unauthorized = UnauthorizedError("Login required")
        forbidden = ForbiddenError("Access denied")
        
        assert unauthorized.status_code == 401
        assert unauthorized.detail == "Login required"
        assert isinstance(unauthorized, HTTPException)
        
        assert forbidden.status_code == 403
        assert forbidden.detail == "Access denied"
        assert isinstance(forbidden, HTTPException) 