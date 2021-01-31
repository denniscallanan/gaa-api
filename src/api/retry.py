import time


def retry(maxAttempts=3, exceptions=(Exception,), initial_wait_seconds=3):
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < maxAttempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, maxAttempts)
                    )
                    attempt += 1
                    time.sleep(initial_wait_seconds*(2**attempt))
            return func(*args, **kwargs)
        return newfn
    return decorator
