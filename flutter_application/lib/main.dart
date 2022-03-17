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
import 'package:flutter_application/homeScreen/homeScreen.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:math';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations(
      [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);

  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();

  final channel = WebSocketChannel.connect(
    Uri.parse('ws://172.25.20.235:5000/ws'),
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
  runApp(MaterialApp(
    title: "Exercise Correction - Pose Estimateion",
    initialRoute: '/',
    routes: {
      '/': (context) => const HomeScreen(),
      '/cameraScreen': (context) =>
          CameraScreen(camera: firstCamera, channel: channel, id: id)
    },
  ));
}
