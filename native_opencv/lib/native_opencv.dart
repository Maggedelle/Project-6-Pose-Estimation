import 'dart:async';
import 'dart:ffi';
import 'dart:io';
import 'dart:typed_data';

import 'package:ffi/ffi.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

//load our C lib
final DynamicLibrary nativeLib = Platform.isAndroid
    ? DynamicLibrary.open('libnative_opencv.so')
    : DynamicLibrary.process();

typedef c_version = Pointer<Utf8> Function();
typedef c_rect = Pointer<Float> Function(Int32 width, Int32 height,
    Int32 rotation, Pointer<Uint8> bytes, Bool isYUV, Pointer<Int32> outCount);

typedef dart_version = Pointer<Utf8> Function();
typedef dart_rect = Pointer<Float> Function(int width, int height, int rotation,
    Pointer<Uint8> bytes, bool isYUV, Pointer<Int32> outCount);

final version = nativeLib.lookupFunction<c_version, dart_version>('version');
final rect = nativeLib.lookupFunction<c_rect, dart_rect>('rect');

class NativeOpenCv {
  static const MethodChannel channel = MethodChannel('native_opencv');
  Pointer<Uint8>? _imageBuffer;

  static Future<String?> get platformVersion async {
    final String? version = await channel.invokeMethod('getPlatformVersion');
    return version;
  }

  Float32List cvRect(int width, int height, int rotation, Uint8List yBuffer,
      Uint8List? uBuffer, Uint8List vBuffer) {
    var ySize = yBuffer.lengthInBytes;
    var uSize = uBuffer?.lengthInBytes ?? 0;
    var vSize = vBuffer?.lengthInBytes ?? 0;
    var totalSize = ySize + uSize + vSize;

    _imageBuffer ??= malloc.allocate<Uint8>(totalSize);

    // We always have at least 1 plane, on Android it si the yPlane on iOS its the rgba plane
    Uint8List _bytes = _imageBuffer!.asTypedList(totalSize);
    _bytes.setAll(0, yBuffer);

    if (Platform.isAndroid) {
      // Swap u&v buffer for opencv
      _bytes.setAll(ySize, vBuffer!);
      _bytes.setAll(ySize + vSize, uBuffer!);
    }

    Pointer<Int32> outCount = malloc.allocate<Int32>(1);
    var res = rect(width, height, rotation, _imageBuffer!,
        Platform.isAndroid ? true : false, outCount);
    final count = outCount.value;

    malloc.free(outCount);
    return res.asTypedList(count);
  }

  String cvVersion() {
    return version().toDartString();
  }
}
