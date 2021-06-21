class RunningError(Exception):
    
    def __init__(self, ex, message='An error occured on running phase: '):
        self.message = message
        self.ex = ex
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message} {self.ex}'