import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Home Screen"),
      ),
      body: Center(
        child: Column(children: [
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {
              Navigator.pushNamed(context, '/cameraScreen');
            },
            child: const Text("Bicep Curls"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: const Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {
              Navigator.pushNamed(context, '/cameraScreen');
            },
            child: const Text("Arm Raises"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: const Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {
              Navigator.pushNamed(context, '/cameraScreen');
            },
            child: const Text("Push Ups"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: const Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
        ]),
      ),
    );
  }
}
