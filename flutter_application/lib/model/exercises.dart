class Exercise {
  final int id;
  final String title, description, image, video, category, type;
  final List<String>? equipment;

  Exercise(
      {required this.id,
      required this.title,
      required this.description,
      required this.image,
      required this.video,
      required this.category,
      this.equipment,
      required this.type});
}

// list of Exercises
// for our demo
List<Exercise> Exercises = [
  Exercise(
      id: 1,
      title: "Arm Curl",
      image: "assets/images/armcurl.png",
      video: "assets/images/armcurl.mp4",
      category: "Arm",
      description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
      type:"armcurl",
      equipment: ["Weight"]),
  Exercise(
      id: 2,
      title: "Arm Raise",
      image: "assets/images/armcurl.png",
      video: "assets/images/armraise.mp4",
      category: "Arm",
      description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
      type:"armraise",
      equipment: ["Weight"]),
  Exercise(
    id: 3,
    title: "Push-up",
    image: "assets/images/pushup.png",
    video: "assets/images/pushup.mp4",
    category: "Core",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
    type:"pushup"
  ),
  Exercise(
    id: 4,
    title: "Sit-up",
    category: "Core",
    image: "assets/images/situp.png",
    video: "assets/images/pushup.mp4",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
    type:"situp"
  ),
];
