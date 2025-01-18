class TaskIDGenerator:
    def __init__(self):
        self._current_id = 1
    
    def generate_task_id(self):
        task_id = self._current_id
        self._current_id += 1
        return task_id

# Initialize the task ID generator
