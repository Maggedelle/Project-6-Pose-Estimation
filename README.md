# Project-6-Pose-Estimation

# How to setup

## Python API
First install the needed libaries, by running the following commands
```
pip install fastapi
pip install "uvicorn[standard]"
pip install opencv-python
pip install mediapipe
```

Now run the sever by running this command
```
python main.py
```

## Flutter Application
Just install Flutter, and run the application, which is located in the folder called flutter_application.
Follow this guide for Windows installment: https://docs.flutter.dev/get-started/install/windows
Remember to change the websocket ip in the application, to the server API.

## Neural Network
Go to the trainer folder, and run the neural_network.py file.
This will train the neural network with the saved weights (in trainer/helper_functions/weights.json).
To only run the model, without training, comment out net.fit on line 51.