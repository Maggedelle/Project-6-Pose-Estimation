class Network:

    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    # Tilføj et layer til vores netværk
    def add(self, layer):
        self.layers.append(layer)

    # Sæt hvilken loss funktion der skal bruges til at udregne prediction i sidste output layer
    def use(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    # Lav predictions over noget input data
    def predict(self, input_data):
        # hvor mange samples er der
        samples = len(input_data)
        result = []

        # loopet der kører vores netværk over alle vores samples
        for i in range(samples):
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # Træn vores netværk
    def fit(self, x_train, y_train, epochs, learning_rate, save_weights):
        samples = len(x_train)
        saved_layers = list()
        # trænings loop
        err = 1
        i = 0
        while err > 0.0025 and i < epochs:

            for j in range(samples):
                output = x_train[j]

                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # Bruges kun til at vise i print
                err += self.loss(y_train[j], output)

                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            err /= samples
            i = i + 1
            print('epoch %d/%d  error = %f' % (i, epochs, err))
        save_weights(self.layers[0].weights, self.layers[0].bias, 0)
        save_weights(self.layers[2].weights, self.layers[2].bias, 1)
        save_weights(self.layers[4].weights, self.layers[4].bias, 2)
        print(self.layers[0].weights, self.layers[0].bias)
