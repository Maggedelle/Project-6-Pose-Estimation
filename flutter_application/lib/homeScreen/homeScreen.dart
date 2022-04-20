import 'package:flutter/material.dart';
import 'package:flutter_application/components/exercisePage.dart';
import 'package:flutter_application/constants.dart';
import 'package:flutter_application/model/exercises.dart';

import '../components/body.dart';

class HomeScreen extends StatefulWidget {
  HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Exercise? showingExercise = null;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kPrimaryColor,
      appBar: buildAppBar(),
      body: showingExercise == null
          ? Body(
              onChanged: (value) {
                setState(() {
                  showingExercise = value;
                });
              },
            )
          : ExercisePage(
              exercise: showingExercise!,
              onChanged: (value) {
                setState(() {
                  showingExercise = null;
                });
              }),
    );
  }

  AppBar buildAppBar() {
    return AppBar(
      elevation: 0,
      backgroundColor: kPrimaryColor,
      title: const Text("Your Online Fitness Coach"),
    );
  }
}
