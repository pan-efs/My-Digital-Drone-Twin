class RunningError(Exception):
    def __init__(self, ex, message = 'An error occured on running phase: '):
        self.message = message
        self.ex = ex
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.ex}'

class BuildError(Exception):
    pass

class ReadingConfigurationError(Exception):
    def __init__(self, ex, message = 'An error occured during reading file: '):
        self.message = message
        self.ex = ex
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.ex}'

class IndexConfigurationError(Exception):
    def __init__(self, ex, message = 'An error occured related to index. Fill all text inputs.'):
        self.message = message
        self.ex = ex
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.ex}'