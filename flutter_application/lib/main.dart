import 'dart:developer';
import 'dart:async';
import 'dart:io';
import 'dart:ui';
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

 runApp(MaterialApp(
    title: "Exercise Correction - Pose Estimateion",
    initialRoute: '/',
    routes: {
      '/': (context) => const HomeScreen(),
      '/cameraScreen': (context) => const DetectionPage()
    },
  ));
}