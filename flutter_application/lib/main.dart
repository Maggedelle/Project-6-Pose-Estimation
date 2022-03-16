import 'dart:developer';
import 'dart:async';
import 'dart:io';
import 'dart:ui';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:native_opencv/native_opencv.dart';
import 'package:flutter_application/camera.dart';
import 'package:flutter_application/cameraPage/cameraPage.dart';
import 'package:flutter_application/homeScreen/homeScreen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);
  NativeOpenCv nativeOpenCv = NativeOpenCv();
  
  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();

  // Get a specific camera from the list of available cameras.
  final firstCamera = cameras.first;
 runApp(MaterialApp(
    title: "Exercise Correction - Pose Estimateion",
    initialRoute: '/',
    routes: {
      '/': (context) => const HomeScreen(),
      '/cameraScreen': (context) =>  CameraScreen(camera:firstCamera)
    },
  ));
}