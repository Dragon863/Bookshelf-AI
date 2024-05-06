import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:flutter_svg_provider/flutter_svg_provider.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatefulWidget {
  const MainApp({super.key});

  @override
  _MainAppState createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  Timer? _timer;
  Map<String, dynamic>? _data;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 5), (timer) {
      setState(() {
        _fetchData();
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _fetchData() async {
    final response =
        await http.get(Uri.parse('http://192.168.1.67:5000/books'));
    if (response.statusCode == 200) {
      Map<String, dynamic>? newData = jsonDecode(response.body);
      print(mapEquals(_data, newData));

      if (newData != null && newData['title'] != _data?['title']) {
        FlutterTts flutterTts = FlutterTts();
        //await flutterTts.setLanguage("en-US");
        await flutterTts.setSpeechRate(0.5);
        await flutterTts
            .speak("Your recommended book is " + newData['recommendation']);

        setState(() {
          _data = newData;
        });
      }
    } else {
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Center(
            child: Text(
              'Book Recommender',
              style:
                  TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
            ),
          ),
          backgroundColor: Colors.redAccent,
        ),
        body: _data == null
            ? const Center(
                child: CircularProgressIndicator(
                color: Colors.redAccent,
              ))
            : Container(
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: Svg("assets/bg.svg"),
                    fit: BoxFit.cover,
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(28.0),
                      child: SizedBox(
                        width: MediaQuery.of(context).size.width * 0.7,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text('${_data!['recommendation']}',
                                style: const TextStyle(
                                    fontWeight: FontWeight.bold, fontSize: 25)),
                            Text(
                                'by ${_data!['recommendation_object']['authors'][0]}',
                                style: const TextStyle(
                                    fontStyle: FontStyle.italic, fontSize: 13)),
                            const SizedBox(height: 17),
                            Text(
                                '${_data!['recommendation_object']['description']}'),
                          ],
                        ),
                      ),
                    ),
                    const Spacer(),
                    Padding(
                      padding: const EdgeInsets.only(right: 28.0, top: 28.0),
                      child: Container(
                        width: 160,
                        child: CachedNetworkImage(
                          imageUrl: _data!['recommendation_object']
                              ['large_thumbnail'],
                          fit: BoxFit.fitHeight,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
      ),
    );
  }
}
