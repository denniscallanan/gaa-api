from fastapi import HTTPException


def generic_error_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper
