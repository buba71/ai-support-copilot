import time

class RetryService:
    """
    A service that provides retry logic for operations that might temporarily fail.
    
    It allows executing a function and automatically retrying it if specific 
    retryable exceptions (like timeouts or server errors) occur.
    """

    def __init__(self, max_retries: int = 3, delay: float = 1.0):

        self.max_retries = max_retries
        self.delay = delay

    def _should_retry(self, exception: Exception) -> bool:
        """
        Determine if a given exception is retryable based on its error message.

        Args:
            exception (Exception): The exception caught during execution.

        Returns:
            bool: True if the exception matches known retryable errors, False otherwise.
        """
        error_message = str(exception).lower()

        # List of string patterns that indicate a temporary, retryable error
        retryable_errors = [
            "timeout",
            "rate limit",
            "429",
            "500",
            "502",
            "503",
        ]

        # Check if any of the retryable error patterns exist in the error message
        return any(err in error_message for err in retryable_errors)

    def execute(self, func, *args, **kwargs):
        """
        Execute a function with retry logic.

        Args:
            func: The callable function to execute.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            The return value of the executed function.

        Raises:
            Exception: Re-raises the exception if it's not retryable, or if 
                       the maximum number of retries has been reached.
        """
        for attempt in range(self.max_retries):
            try:
                # Attempt to execute the provided function with its arguments
                return func(*args, **kwargs)

            except Exception as e: 
                # If the error is not in our retryable list, stop and raise immediately
                if not self._should_retry(e):
                    raise

                # If we have exhausted all attempts, raise the last caught exception
                if attempt == self.max_retries - 1:
                    raise

                # Wait for the specified delay before the next attempt
                time.sleep(self.delay)