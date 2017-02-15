
# encode all exceptions here

class gdcException(Exception):
    def __init__(self, msg):
        super().__init__("GDC: " + msg)

class gdcSuccess(gdcException):
    def __init__(self):
        super().__init__("Success!")

class NoCredentialsError(gdcException):
    def __init__(self):
        super().__init__("No credentials found.")

class NoRootDir(gdcException):
    def __init__(self, path):
        super().__init__("No Root directory found: (%s)" % path)

class NoDriveService(gdcException):
    def __init__(self, path):
        super().__init__("Drive service failed to initialize.")

class NotCleanSlateError(gdcException):
    def __init__(self, path):
        super().__init__("Drive folder is not empty.")
