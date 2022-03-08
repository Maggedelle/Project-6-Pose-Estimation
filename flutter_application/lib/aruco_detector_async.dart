import 'dart:async';
import 'dart:developer';
import 'dart:isolate';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:flutter/services.dart';
import 'package:flutter_application/aruco_detector.dart' as aruco_detector;

class ArucoDetectorAsync {
  bool arThreadReady = false;
  late Isolate _detectorThread;
  late SendPort _toDetectorThread;
  int _reqId = 0;
  final Map<int, Completer> _cbs = {};

  ArucoDetectorAsync() {
    //_initDetectionThread();
  }

  void _initDetectionThread() async { //vi bruger ikke denne funktion, men den kan blive relevant :)
    // Create the port on which the detector thread will send us messages and listen to it.
   /* ReceivePort fromDetectorThread = ReceivePort();
    fromDetectorThread.listen(_handleMessage, onDone: () {
      arThreadReady = false;
    });

    // Spawn a new Isolate using the ArucoDetector.init method as entry point and
    // the port on which it can send us messages as parameter
    final bytes = await rootBundle.load('assets/drawable/marker.png');
    final initReq = aruco_detector.InitRequest(toMainThread: fromDetectorThread.sendPort, markerPng: bytes);
    _detectorThread = await Isolate.spawn(aruco_detector.init, initReq);
    */
  }

  Future<Float32List?> detect(CameraImage image, int rotation) {
    if (!arThreadReady) {
      return Future.value(null);
    }

    var reqId = ++_reqId;
    var res = Completer<Float32List?>();
    _cbs[reqId] = res;
    var msg = aruco_detector.Request(
      reqId: reqId,
      method: 'detect',
      params: {'image': image, 'rotation': rotation},
    );

    _toDetectorThread.send(msg);
    return res.future;
  }

  void destroy() async {
    if (!arThreadReady) {
      return;
    }

    arThreadReady = false;

    // We send a Destroy request and wait for a response before killing the thread
    var reqId = ++_reqId;
    var res = Completer();
    _cbs[reqId] = res;
    var msg = aruco_detector.Request(reqId: reqId, method: 'destroy');
    _toDetectorThread.send(msg);

    // Wait for the detector to acknoledge the destory and kill the thread
    await res.future;
    _detectorThread.kill();
  }
}