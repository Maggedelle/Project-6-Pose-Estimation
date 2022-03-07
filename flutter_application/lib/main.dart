import 'dart:async';
import 'dart:io';
import 'dart:ui';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_application/camera.dart';

Future<void> main() async {
  // Ensure that plugin services are initialized so that `availableCameras()`
  // can be called before `runApp()`
  WidgetsFlutterBinding.ensureInitialized();

  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();

  // Get a specific camera from the list of available cameras.
  final firstCamera = cameras.first;

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
      appBar: AppBar(
        title: Text("Exercises"),
        backgroundColor: const Color.fromARGB(255, 65, 75, 80),
      ),
      body: Center(
        child: Column(children: [
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {},
            child: const Text("Bicep Curls"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: const Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {},
            child: const Text("Arm Raises"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {},
            child: const Text("Push Ups"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
        ]),
      ),
    ));
  }
}
