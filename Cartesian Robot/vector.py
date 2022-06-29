
class vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def add(self, cords):
        self.x = self.x + cords.x
        self.y = self.y + cords.y
        return vector(self.x, self.y)
    def subtract(self, cords):
        self.x = self.x - cords.x
        self.y = self.y - cords.y
        return vector(self.x, self.y)
    def get_list(self):
        return self.x, self.y