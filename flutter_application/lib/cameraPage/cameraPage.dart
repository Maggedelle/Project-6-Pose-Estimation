import 'package:flutter/material.dart';

class CameraPage extends StatelessWidget {
  const CameraPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Ny screen")),
      body: Center(
          child: Column(
        children: [
          const Padding(padding: EdgeInsets.all(10.0)),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
            },
            child: const Text("Åh nej, lad mig komme tilbage"),
            style: ElevatedButton.styleFrom(
                fixedSize: const Size(400, 200),
                primary: const Color.fromARGB(181, 53, 240, 6),
                onPrimary: const Color.fromARGB(235, 231, 17, 17),
                textStyle: const TextStyle(fontSize: 60)),
          ),
        ],
      )),
    );
  }
}
