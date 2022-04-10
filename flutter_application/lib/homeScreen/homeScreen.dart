import 'package:flutter/material.dart';
import 'package:flutter_application/constants.dart';

import '../components/body.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kPrimaryColor,
      appBar: buildAppBar(),
      body: Body(),
    );
  }
  AppBar buildAppBar (){
    return AppBar(
      elevation: 0,
        backgroundColor: kPrimaryColor,
        title: const Text("Your Online Fitness Coach"),
    );
  }
}
