import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:image/image.dart' as imglib;
import 'package:http/http.dart' as http;

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

bool debug = false;
bool sentImage = false;
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
    try{
      await _initializeControllerFuture;

      cameraBytesToDetector(camera: _controller);
    }catch(e) {
      print(e);
    }
  }



  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    super.dispose();
  }

  void cameraBytesToDetector({required CameraController camera}) {
    camera.startImageStream((image) => _processCameraImage(image));
  }

  void _processCameraImage(CameraImage image) async {
    
    print("haha");
    if(!sentImage){
      final imageBytes = await convertImagetoPng(image);

      //Uint8List bytes = image.planes[1].bytes;
      
      sendBytes(base64.encode(imageBytes!));
       //sendBytes(bytes);
       sentImage = true;
       sleep1();
    }
    
  }
  Future sleep1() {
    return new Future.delayed(const Duration(milliseconds: 100), () => sentImage=false);
  }
  
Future<List<int>?> convertImagetoPng(CameraImage image) async {
  try {
    imglib.Image img;
    if (image.format.group == ImageFormatGroup.yuv420) {
      img = _convertYUV420(image);
    } else  {
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
      var newVal = shift | (pixelColor << 16) | (pixelColor << 8) | pixelColor;

      img.data[planeOffset + x] = newVal;
    }
  }

  return img;
}
  Future<http.Response> sendBytes(String bytes) {
  return http.post(
    Uri.parse('http://192.168.33.1:5000/'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'byteData': bytes,
    }),
  );
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