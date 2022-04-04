class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # Den her bruger vi til at udregne output for et layer, givet det input den modtager
    def forward_propagation(self, input):
        raise NotImplementedError

    # Bruges til at opdater weights mellem layers
    def backward_propagation(self, output_error, learning_rate):
        raise NotImplementedError