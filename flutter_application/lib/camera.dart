import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:image/image.dart' as imglib;
import 'package:http/http.dart' as http;
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'constants.dart';

bool debug = false;
bool sentImage = false;

// A screen that allows users to take a picture using a given camera.
class CameraScreen extends StatefulWidget {
  const CameraScreen(
      {Key? key,
      required this.camera,
      required this.channel,
      required this.id,
      required this.exerciseType})
      : super(key: key);

  final CameraDescription camera;
  final WebSocketChannel channel;
  final String id;
  final String exerciseType;
  @override
  CameraScreenState createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // To display the current output from the Camera,
    // create a CameraController.
    _controller = CameraController(
      // Get a specific camera from the list of available cameras.
      widget.camera,
      // Define the resolution to use.
      ResolutionPreset.low,
    );
    // Next, initialize the controller. This returns a Future.
    _initializeControllerFuture = _controller.initialize();
    initCamera();
  }

  Future<void> initCamera() async {
    try {
      await _initializeControllerFuture;

      cameraBytesToDetector(camera: _controller);
    } catch (e) {
      print(e);
    }
  }

  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    widget.channel.sink.close();
    super.dispose();
  }

  void cameraBytesToDetector({required CameraController camera}) {
    camera.startImageStream((image) => _processCameraImage(image));
  }

  void _processCameraImage(CameraImage image) async {
    if (!sentImage && sendImageData == true) {
      final imageBytes = await convertImagetoPng(image);

      //Uint8List bytes = image.planes[1].bytes;

      sendBytes(base64.encode(imageBytes!));
      //sendBytes(bytes);
      sentImage = true;
      sleep1();
    }
  }

  Future sleep1() {
    return new Future.delayed(
        const Duration(milliseconds: 20), () => sentImage = false);
  }

  Future<List<int>?> convertImagetoPng(CameraImage image) async {
    try {
      imglib.Image img;
      if (image.format.group == ImageFormatGroup.yuv420) {
        img = _convertYUV420(image);
      } else {
        img = _convertBGRA8888(image);
      }

      imglib.PngEncoder pngEncoder = new imglib.PngEncoder();

      // Convert to png
      List<int> png = pngEncoder.encodeImage(img);
      return png;
    } catch (e) {
      print(">>>>>>>>>>>> ERROR:" + e.toString());
    }
    return null;
  }

// CameraImage BGRA8888 -> PNG
// Color
  imglib.Image _convertBGRA8888(CameraImage image) {
    return imglib.Image.fromBytes(
      image.width,
      image.height,
      image.planes[0].bytes,
      format: imglib.Format.bgra,
    );
  }

// CameraImage YUV420_888 -> PNG -> Image (compresion:0, filter: none)
// Black
  imglib.Image _convertYUV420(CameraImage image) {
    var img = imglib.Image(image.width, image.height); // Create Image buffer

    Plane plane = image.planes[0];
    const int shift = (0xFF << 24);

    // Fill image buffer with plane[0] from YUV420_888
    for (int x = 0; x < image.width; x++) {
      for (int planeOffset = 0;
          planeOffset < image.height * image.width;
          planeOffset += image.width) {
        final pixelColor = plane.bytes[planeOffset + x];
        // color: 0x FF  FF  FF  FF
        //           A   B   G   R
        // Calculate pixel color
        var newVal =
            shift | (pixelColor << 16) | (pixelColor << 8) | pixelColor;

        img.data[planeOffset + x] = newVal;
      }
    }

    return img;
  }

  Future<void> sendBytes(String bytes) async {
    try {
      widget.channel.sink.add(json.encode({
        "frame": bytes,
        "id": widget.id,
        "type": "sendImage",
        "exerciseType": widget.exerciseType
      }));
    } catch (e) {
      print("ERROR: " + e.toString());
    }
  }

  Timer? countdownTimer;
  Duration myDuration = Duration(seconds: 3);
  void startTimer() {
    countdownTimer =
        Timer.periodic(Duration(seconds: 1), (_) => {
          setCountDown(),
          if(myDuration.inSeconds == 0) {
            sendImageData = true
          }

          });
  }

  void setCountDown() {
    final reduceSecondsBy = 1;
    setState(() {
      final seconds = myDuration.inSeconds - reduceSecondsBy;
      if (seconds < 0) {
        countdownTimer!.cancel();
      } else {
        myDuration = Duration(seconds: seconds);
      }
    });
  }

  bool showBeginButton = true;
  bool showTimerText = false;
  bool sendImageData = false;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(),
      // You must wait until the controller is initialized before displaying the
      // camera preview. Use a FutureBuilder to display a loading spinner until the
      // controller has finished initializing.
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // If the Future is complete, display the preview.
            return Container(
                child: Stack(
              children: <Widget>[
                Transform.scale(
                    scale: 1 /
                        (_controller.value.aspectRatio *
                            MediaQuery.of(context).size.aspectRatio),
                    alignment: Alignment.topCenter,
                    child: CameraPreview(_controller)),
                myDuration.inSeconds != 0 && showTimerText == true
                    ? Center(
                        child: Stack(
                        children: <Widget>[
                          // Stroked text as border.
                          Text(
                            myDuration.inSeconds.remainder(60).toString(),
                            style: TextStyle(
                              fontSize: 150,
                              foreground: Paint()
                                ..style = PaintingStyle.stroke
                                ..strokeWidth = 4
                                ..color = Colors.black,
                            ),
                          ),
                          // Solid text as fill.
                          Text(
                            myDuration.inSeconds.remainder(60).toString(),
                            style: const TextStyle(
                              fontSize: 150,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      ))
                    : Text("")
              ],
            ));
          } else {
            // Otherwise, display a loading indicator.
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      floatingActionButton: showBeginButton
          ? FloatingActionButton.extended(
              backgroundColor: const Color.fromRGBO(181, 230, 29, 1),
              splashColor: Colors.yellow,
              label: Stack(
                children: <Widget>[
                  // Stroked text as border.
                  Text(
                    'Begin!',
                    style: TextStyle(
                      fontSize: 40,
                      foreground: Paint()
                        ..style = PaintingStyle.stroke
                        ..strokeWidth = 3
                        ..color = Colors.black,
                    ),
                  ),
                  // Solid text as fill.
                  const Text(
                    'Begin!',
                    style: TextStyle(
                      fontSize: 40,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
              extendedPadding: const EdgeInsets.all(100),
              onPressed: () async {
                setState(() {
                  startTimer();
                  showBeginButton = false;
                  showTimerText = true;
                });
              },
            )
          : null,
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }

  AppBar buildAppBar() {
    return AppBar(
      elevation: 0,
      backgroundColor: kPrimaryColor,
      title: const Text("Your Online Fitness Coach"),
    );
  }
}
