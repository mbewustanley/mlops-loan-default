# creating custom exceptions because production pipelines never raise raw exceptions

class PipelineException(Exception):
    def __init__(self, message):
        super().__init__(message)