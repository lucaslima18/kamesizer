class IncorrectImageFormatError(Exception):
    """
    Incorrect image format from file
    """


class ImageMaxSizeExceededError(Exception):
    """
    Max dimensions size exceded
    """


class ImageNegativeSizeError(Exception):
    """
    Image must be a positive number
    """


class ResizeToOriginalValueError(Exception):
    """
    The image cannot be resized to the original value
    """


class ImageAlreadyOnMaxSizeError(Exception):
    """
    The image is already on max supported size
    """


class ImageAlreadyExists(Exception):
    """
    The image already exists
    """


class ImageNotFound(Exception):
    """
    The image not exists in dataabse
    """


class StillNotResized(Exception):
    """
    The image stil not resized
    """
