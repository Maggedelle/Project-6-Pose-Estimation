import 'package:flutter/material.dart';
import 'package:flutter_application/constants.dart';
import 'package:flutter_application/model/exercises.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:video_player/video_player.dart';

class ExercisePage extends StatefulWidget {
  const ExercisePage(
      {Key? key, required this.onChanged, required this.exercise})
      : super(key: key);
  final ValueChanged onChanged;
  final Exercise exercise;
  @override
  State<ExercisePage> createState() => _ExercisePageState();
}

class _ExercisePageState extends State<ExercisePage> {
  late VideoPlayerController controller;

  String getEquipmentString() {
    String equiptment = "";
    if (widget.exercise.equipment != null) {
      for (var string in widget.exercise.equipment!) {
        equiptment += string + " ";
      }
    }

    return equiptment;
  }

  @override
  void initState() {
    super.initState();
    controller = VideoPlayerController.asset(widget.exercise.video)
      ..addListener(() => setState(() {}))
      ..setLooping(true)
      ..initialize().then((_) => controller.play());
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;

    return Column(children: <Widget>[
      Container(child: VideoPlayerWidget(controller: controller)),
      Text(
        widget.exercise.title,
        style: TextStyle(
          color: Colors.white,
          fontSize: 44,
        ),
      ),
      Container(
        margin: EdgeInsets.all(15),
        child: Text(
          widget.exercise.description,
          style: TextStyle(
            color: Colors.white,
            fontSize: 18,
          ),
        ),
      ),
      Container(
        margin: EdgeInsets.all(15),
        child: Text(
          widget.exercise.equipment == null
              ? "This exercise does not require any equiptment!"
              : "This exercise requires the following equipment: " +
                  getEquipmentString(),
          style: TextStyle(fontSize: 20, color: Colors.white),
        ),
      ),
      Container(
        margin: EdgeInsets.only(left: 20, top: 100),
        child: Row(
          children: [
            ElevatedButton(
                onPressed: (() => widget.onChanged("back")),
                style: ButtonStyle(
                    backgroundColor: MaterialStateProperty.all(
                        Color.fromRGBO(181, 230, 29, 1)),
                    minimumSize: MaterialStateProperty.all(Size(125, 50))),
                child: Text("Back")),
            SizedBox(width: 100),
            ElevatedButton(
              onPressed: (() =>
                  Navigator.pushNamed(context, "/cameraScreen/armcurl")),
              child: Text("Begin"),
              style: ButtonStyle(
                  backgroundColor: MaterialStateProperty.all(
                      Color.fromRGBO(181, 230, 29, 1)),
                  minimumSize: MaterialStateProperty.all(Size(125, 50))),
            )
          ],
        ),
      )
    ]);
  }
}

class VideoPlayerWidget extends StatelessWidget {
  final VideoPlayerController controller;

  const VideoPlayerWidget({
    required this.controller,
  });

  @override
  Widget build(BuildContext context) =>
      controller != null && controller.value.isInitialized
          ? Container(alignment: Alignment.topCenter, child: buildVideo())
          : Container(
              height: 200,
              child: Center(child: CircularProgressIndicator()),
            );

  Widget buildVideo() => buildVideoPlayer();

  Widget buildVideoPlayer() => AspectRatio(
      aspectRatio: controller.value.aspectRatio,
      child: VideoPlayer(controller));
}
