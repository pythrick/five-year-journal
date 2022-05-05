import 'package:five_year_journal/services/api_service.dart';
import 'package:flutter/material.dart';

import 'models.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(const MyApp());
}

final List<JournalLog> journalLogs = [
  const JournalLog(content: "xxx"),
];

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: "Five-Year Journal",
        home: Scaffold(
            appBar: AppBar(
              title: const Text("Welcome to Five-Year Journal"),
            ),
            body: ListView(children: <Widget>[
              titleSection,
              formSection,
              journalLogsSection,
            ])));
  }
}

Widget titleSection = Container(
  padding: const EdgeInsets.all(32),
  child: Row(
    children: const [
      Icon(
        Icons.arrow_back,
      ),
      Expanded(child: Center(child: Text("May 5th"))),
      Icon(
        Icons.arrow_forward,
      ),
    ],
  ),
);

class FormPost extends StatefulWidget {
  const FormPost({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _FormPostState();
}

class _FormPostState extends State<FormPost> {
  final _formKey = GlobalKey<FormState>();
  final Map<String, dynamic> formData = {"content": ""};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _buildForm(),
    );
  }

  Widget _buildForm() {
    return Form(
        key: _formKey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _buildPostField(),
            _buildSubmitButton(),
          ],
        ));
  }

  Widget _buildPostField() {
    return TextFormField(
      decoration: const InputDecoration(labelText: 'Post'),
      validator: (String? value) {
        if (value == null || value.isEmpty) {
          return 'Please enter some text';
        }
        return null;
      },
      onSaved: (String? value) {
        formData["content"] = value;
      },
      onFieldSubmitted: (v) {
        _submitForm();
      },
    );
  }

  Widget _buildSubmitButton() {
    return ElevatedButton(
      onPressed: () {
        _submitForm();
      },
      child: const Text('Post'),
    );
  }

  void _submitForm() {
    print('Submitting form');
    if (_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Processing Data')),
      );
      _formKey.currentState!.save();
      print(formData);
    }
  }
}

Widget formSection = Container(padding: const EdgeInsets.all(30), height: 200, child: const FormPost()) ;

Widget journalLogsSection = Container(
      color: Colors.red,
      padding: EdgeInsets.all(20.0),
      child: Column(
        children: <Widget>[
          Text('Red container should be scrollable'),
          Container(
            width: double.infinity,
            height: 700.0,
            padding: EdgeInsets.all(10.0),
            color: Colors.white.withOpacity(0.7),
            child: Text('I will have a column here'),
          )
        ],
      ),
);

class JournalLogTile extends StatelessWidget {
  final JournalLog? journalLog;

  const JournalLogTile({this.journalLog, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(journalLog?.createdAt?.year.toString() ?? "2099"),
    );
  }
}
