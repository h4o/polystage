from python.excel.Widgets import LineChart


class BSLine(LineChart):
    def __init__(self):
        super().__init__('Tasks execution times')
        self.header = ['Task name', 'Worst Execution time (ms)', 'Best Execution Time (ms)']

    def update(self):
        self.append('Mission Task', 0.089, 0.011)
        self.append('Navigate Task', 0.917, 0.162)
        self.append('Refine Task', 29.020, 8.718)
        self.append('Report Task', 53.487, 0.496)
        self.append('Control Task', 0.017, 0.001)
        self.append('Avoid Task', 14.081, 1.165)
        self.append('Communicate Task', 27.049, 11.913)
