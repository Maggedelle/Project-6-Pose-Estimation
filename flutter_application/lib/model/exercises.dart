class Exercise {
  final int id;
  final String title, description, image, category;

  Exercise({required this.id, required this.title, required this.description, required this.image, required this.category});
}

// list of Exercises
// for our demo
List<Exercise> Exercises = [
  Exercise(
    id: 1,
    title: "Arm Curl",
    image: "assets/images/armcurl.png",
    category:"Arm",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
  ),
  Exercise(
    id: 2,
    title: "Arm Raise",
    image: "assets/images/armcurl.png",
    category: "Arm",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
  ),
  Exercise(
    id: 3,
    title: "Push-up",
    image: "assets/images/pushup.png",
    category: "Core",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
  ),
   Exercise(
    id: 4,
    title: "Sit-up",
    category: "Core",
    image: "assets/images/situp.png",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
  ),
];

List<Exercise> Exercisesa = [
  Exercise(
    id: 1,
    title: "Arm Curl",
    image: "assets/images/armcurl.png",
    category:"Arm",
    description:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
  )
];