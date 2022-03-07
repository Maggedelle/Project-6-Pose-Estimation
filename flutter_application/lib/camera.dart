import 'dart:async';
import 'dart:developer';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:native_opencv/native_opencv.dart';
import 'dart:typed_data';

bool debug = false;

// A screen that allows users to take a picture using a given camera.
class CameraScreen extends StatefulWidget {
  const CameraScreen({
    Key? key,
    required this.camera,
  }) : super(key: key);

  final CameraDescription camera;

  @override
  CameraScreenState createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  int _camFrameRotation = 0;
  double _camFrameToScreenScale = 0;
  int _lastRun = 0;
  bool _detectionInProgress = false;
  List<double> _arucos = List.empty();
  final nativeOpencv = NativeOpenCv();

  Float32List? getRect(CameraImage image, int rotation) {
    if (nativeOpencv == null) {
      return null;
    }

    // On Android the image format is YUV and we get a buffer per channel,
    // in iOS the format is BGRA and we get a single buffer for all channels.
    // So the yBuffer variable on Android will be just the Y channel but on iOS it will be
    // the entire image
    var planes = image.planes;
    var yBuffer = planes[0].bytes;

    Uint8List? uBuffer;
    Uint8List? vBuffer;

    uBuffer = planes[1].bytes;
    vBuffer = planes[2].bytes;

    var res = nativeOpencv!
        .cvRect(image.width, image.height, rotation, yBuffer, uBuffer, vBuffer);
    return res;
  }

  @override
  void initState() {
    super.initState();
    // To display the current output from the Camera,
    // create a CameraController.

    initCamera();

    // Next, initialize the controller. This returns a Future.
  }

  Future<void> initCamera() async {
    print("i am called :D");
    _controller = CameraController(
      // Get a specific camera from the list of available cameras.
      widget.camera,
      // Define the resolution to use.
      ResolutionPreset.medium,
    );
    _initializeControllerFuture = _controller.initialize();
    try {
      await _controller!.initialize();
      await _controller!
          .startImageStream((image) => _processCameraImage(image));
    } catch (e) {
      log("Error initializing camera, error: ${e.toString()}");
    }

    if (mounted) {
      setState(() {});
    }
  }

  void _processCameraImage(CameraImage image) async {
    if (DateTime.now().millisecondsSinceEpoch - _lastRun < 30) {
      return;
    }

    // calc the scale factor to convert from camera frame coords to screen coords.
    // NOTE!!!! We assume camera frame takes the entire screen width, if that's not the case
    // (like if camera is landscape or the camera frame is limited to some area) then you will
    // have to find the correct scale factor somehow else
    if (_camFrameToScreenScale == 0) {
      var w = (_camFrameRotation == 0 || _camFrameRotation == 180)
          ? image.width
          : image.height;
      _camFrameToScreenScale = MediaQuery.of(context).size.width / w;
    }

    // Call the detector
    _detectionInProgress = true;
    var res = await getRect(image, _camFrameRotation);
    _detectionInProgress = false;
    _lastRun = DateTime.now().millisecondsSinceEpoch;

    // Make sure we are still mounted, the background thread can return a response after we navigate away from this
    // screen but before bg thread is killed
    if (!mounted || res == null || res.isEmpty) {
      return;
    }

    // convert arucos from camera frame coords to screen coords
    print("hello my name is magnus axelsen");
    print(res);
  }

  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    super.dispose();
  }

  void cameraBytesToDetector({required CameraController camera}) {
    camera.startImageStream((image) {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Fitness App'),
        foregroundColor: Colors.red,
      ),
      // You must wait until the controller is initialized before displaying the
      // camera preview. Use a FutureBuilder to display a loading spinner until the
      // controller has finished initializing.
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // If the Future is complete, display the preview.
            return debug
                ? AspectRatio(
                    aspectRatio: _controller.value.aspectRatio,
                    child: CameraPreview(_controller))
                : CameraPreview(_controller);
          } else {
            // Otherwise, display a loading indicator.
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Color.fromARGB(255, 1, 148, 247),
        splashColor: Colors.yellow,
        // Provide an onPressed callback.
        onPressed: () async {
          setState(() {
            debug ? debug = false : debug = true;
          });
          print(debug);
          // Take the Picture in a try / catch block. If anything goes wrong,
          // catch the error.
          try {} catch (e) {
            // If an error occurs, log the error to the console.
            print(e);
          }
        },
        child: const Icon(
          Icons.display_settings,
          color: Colors.black54,
        ),
      ),
    );
  }
}
