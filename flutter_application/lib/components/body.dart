import 'package:flutter/material.dart';
import 'package:flutter_application/constants.dart';
import 'package:flutter_application/model/exercises.dart';
import 'package:flutter_svg/flutter_svg.dart';

class Body extends StatefulWidget {
  @override
  State<Body> createState() => _BodyState();
}

class _BodyState extends State<Body> {

  List<Exercise> showingExercises = Exercises;
  String selectedCategory = "All";
  String searchQuery = "";
  void updateShowingExercise() {
    List<Exercise> exercises = Exercises;
    
    if(selectedCategory != "All") {
      exercises = exercises.where((element) => element.category == selectedCategory).toList();
    }

    if(searchQuery != "") {
      exercises = exercises.where((element) => element.title.toLowerCase().contains(searchQuery)).toList();
    }

  setState(() {
    showingExercises = exercises;
  });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        SearchBox(
          onChanged: (value) {
            searchQuery = value.toString().toLowerCase();
            updateShowingExercise();
          },
        ),
        CategoryList(onChanged: (value) { 
          selectedCategory = value;
          updateShowingExercise();
        },),
        SizedBox(height: kDefaultPadding / 2),
        Expanded(
          child: Stack(
            children: <Widget>[
              Container(
                margin: EdgeInsets.only(top: 70),
                decoration: BoxDecoration(
                    color: Color.fromRGBO(181,230,29, 1),
                    borderRadius: BorderRadius.only(
                        topLeft: Radius.circular(40),
                        topRight: Radius.circular(40))),
              ),
              ListView.builder(
                itemCount:  showingExercises.length,
                itemBuilder: (context,index) => ExerciseCard(exercise:showingExercises[index], exerciseIndex: index,),
              ),
            ],
          ),
        )
      ],
    );
  }
}

class ExerciseCard extends StatelessWidget {
  const ExerciseCard({
    Key? key,
    required this.exerciseIndex,
    required this.exercise
  }) : super(key: key);

  final int exerciseIndex;
  final Exercise exercise;
  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return ElevatedButton(
      onPressed: () {
        Navigator.pushNamed(context, "/cameraScreen/armcurl");
      },
      style: ButtonStyle(
            shadowColor: MaterialStateProperty.all(Colors.white.withOpacity(0)),
           backgroundColor: MaterialStateProperty.all(Colors.white.withOpacity(0)),
      ),
      child: Container(

      margin: EdgeInsets.symmetric(
        horizontal: kDefaultPadding,
        vertical: kDefaultPadding / 2,
      ),
      height: 160,
      child: Stack(
        alignment: Alignment.bottomCenter,
        children: <Widget>[

          Container(
            height: 136,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(22),
              color: kBlueColor,
            ),
            child: Container(
              decoration: BoxDecoration(
                  color: Colors.white, borderRadius: BorderRadius.circular(22)),
            ),
          ),
          Positioned(
              top: 0,
              right: 0,
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: kDefaultPadding),
                height: 160,
                width: 200,
                child:
                    Image.asset(exercise.image, fit: BoxFit.cover),
              )),
          Positioned(
            bottom: 0,
            left:0,
              child: SizedBox(
            height: 90,
            width: size.width - 250,
            child: Column(
              children: <Widget>[Text(exercise.title, style: Theme.of(context).textTheme.headline5)],
            ),
          ))
        ],
      ),
      )
    );
  }
}

class CategoryList extends StatefulWidget {
  const CategoryList({Key? key, required this.onChanged}) : super(key: key);
  final ValueChanged onChanged;
  @override
  State<CategoryList> createState() => _CategoryListState();
}

class _CategoryListState extends State<CategoryList> {
  int selectedIndex = 0;
  List categories = ['All', 'Arm', 'Shoulder', 'Core', 'Leg'];

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: kDefaultPadding / 2),
      height: 30,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: categories.length,
        itemBuilder: (context, index) => GestureDetector(
          onTap: () {
            setState(() {
              selectedIndex = index;
            });
            widget.onChanged(categories[selectedIndex]);
          },
          child: Container(
            alignment: Alignment.center,
            margin: EdgeInsets.symmetric(horizontal: kDefaultPadding / 2),
            padding: EdgeInsets.symmetric(horizontal: kDefaultPadding),
            decoration: BoxDecoration(
                color: index == selectedIndex
                    ? Colors.white.withOpacity(0.4)
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(12)),
            child: Text(
              categories[index],
              style: TextStyle(color: Colors.white),
            ),
          ),
        ),
      ),
    );
  }
}

class SearchBox extends StatelessWidget {
  const SearchBox({
    Key? key,
    required this.onChanged,
  }) : super(key: key);
  final ValueChanged onChanged;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(kDefaultPadding),
      padding: EdgeInsets.symmetric(
          horizontal: kDefaultPadding, vertical: kDefaultPadding / 4),
      decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.4),
          borderRadius: BorderRadius.circular(20)),
      child: TextField(
        onChanged: onChanged,
        decoration: InputDecoration(
            icon: SvgPicture.asset("assets/images/search.svg"),
            enabledBorder: InputBorder.none,
            focusedBorder: InputBorder.none,
            hintText: 'Search for an exercise..',
            hintStyle: TextStyle(color: Colors.white)),
      ),
    );
  }
}
