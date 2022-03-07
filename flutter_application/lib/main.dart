import 'dart:async';
import 'dart:io';
import 'dart:ui';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_application/camera.dart';
import 'package:flutter_application/cameraScreen/cameraScreen.dart';
import 'package:flutter_application/homeScreen/homeScreen.dart';

void main() async {
  // Ensure that plugin services are initialized so that `availableCameras()`
  // can be called before `runApp()`
  //WidgetsFlutterBinding.ensureInitialized();

  // Obtain a list of the available cameras on the device.
  //final cameras = await availableCameras();

  // Get a specific camera from the list of available cameras.
  //final firstCamera = cameras.first;

  runApp(MaterialApp(
    title: "Exercise Correction - Pose Estimateion",
    initialRoute: '/',
    routes: {
      '/': (context) => const HomeScreen(),
      '/cameraScreen': (context) => const CameraScreen()
    },
  ));
}


