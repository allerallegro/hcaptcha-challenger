class ImageValidationException(Exception):
    def __init__(self, message, img):
        super().__init__(message)
        self.img = img
