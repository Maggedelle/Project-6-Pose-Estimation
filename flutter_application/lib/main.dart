import 'dart:convert';
import 'dart:developer';
import 'dart:async';
import 'dart:io';
import 'dart:ui';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_application/camera.dart';
import 'package:flutter_application/cameraPage/cameraPage.dart';
import 'package:flutter_application/constants.dart';
import 'package:flutter_application/homeScreen/homeScreen.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:math';
import 'package:google_fonts/google_fonts.dart';
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations(
      [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);

  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();

  final channel = WebSocketChannel.connect(
    Uri.parse('ws://192.168.87.181:5000/ws'),
  );

  channel.stream.listen(
    (data) {
      print(data);
    },
    onError: (error) => print(error),
  );

  var rng = Random();
  String id = "id:" +
      rng.nextInt(100000).toString() +
      rng.nextInt(100000).toString() +
      rng.nextInt(10).toString();

  var data = {'type': 'init', 'id': id};
  channel.sink.add(json.encode(data));


  // Get a specific camera from the list of available cameras.
  final firstCamera = cameras.first;
  
  final ThemeData theme = ThemeData();
  runApp(MaterialApp(
    title: "Exercise Correction - Pose Estimateion",
    theme: theme.copyWith(
      primaryColor: kPrimaryColor,
      colorScheme: theme.colorScheme.copyWith(secondary: kPrimaryColor, primary: kPrimaryColor),
      visualDensity: VisualDensity.adaptivePlatformDensity
    ),
    initialRoute: '/',
    routes: {
      '/': (context) =>  HomeScreen(),
      '/cameraScreen/armcurl': (context) =>
          CameraScreen(camera: firstCamera, channel: channel, id: id, exerciseType:"armcurl"),
      '/cameraScreen/armraise': (context) =>
          CameraScreen(camera: firstCamera, channel: channel, id: id, exerciseType: "armraise"),
      '/cameraScreen/pushup': (context) =>
          CameraScreen(camera: firstCamera, channel: channel, id: id, exerciseType: "pushup")
    },
  ));
}
