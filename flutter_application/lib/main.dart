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
        backgroundColor: Color.fromARGB(255, 65, 75, 80),
      ),
      body: Center(
        child: Column(children: [
          Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {},
            child: Text("hej ebbi"),
            style: ElevatedButton.styleFrom(fixedSize: Size(200, 100)),
          ),
          Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {},
            child: Text("hej Mulle"),
            style: ElevatedButton.styleFrom(fixedSize: Size(200, 100)),
          ),
        ]),
      ),
    ));
  }
}
