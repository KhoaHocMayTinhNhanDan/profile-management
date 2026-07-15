class MobileFlutterFactory:
    """
    Concrete Factory tạo các UI templates cho Mobile Flutter (Dart).
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str:
        return f"""
import 'package:flutter/material.dart';
import '../hooks/use_{snake_name}.dart';

class {pascal_name}Page extends StatefulWidget {{
  final dynamic context;
  const {pascal_name}Page({{Key? key, this.context}}) : super(key: key);

  @override
  State<{pascal_name}Page> createState() => _{pascal_name}PageState();
}}

class _{pascal_name}PageState extends State<{pascal_name}Page> {{
  late final Use{pascal_name} _hook;

  @override
  void initState() {{
    super.initState();
    _hook = Use{pascal_name}(widget.context);
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('{pascal_name} Feature'),
        backgroundColor: Color({{ DARK_BG_ARGB }}), // Theme Background
      ),
      body: Container(
        color: Color({{ DARK_BG_ARGB }}),
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome to {pascal_name}',
              style: TextStyle(color: Color({{ TEXT_COLOR_ARGB }}), fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Text(
              'This is a Clean Architecture feature scaffolded dynamically for Flutter.',
              style: TextStyle(color: Color({{ SUBTEXT_COLOR_ARGB }}), fontSize: 16),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {{
                // Trigger logic
              }},
              style: ElevatedButton.styleFrom(backgroundColor: Color({{ ACCENT_COLOR_ARGB }})),
              child: Text('Execute Feature Action', style: TextStyle(color: Color({{ DARK_BG_ARGB }}))),
            )
          ],
        ),
      ),
    );
  }}
}}
"""

    def create_buttons(self) -> str:
        return """
import 'package:flutter/material.dart';

class AtomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Color color;

  const AtomButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.color = const Color({{ ACCENT_COLOR_ARGB }}), // Theme Accent
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular({{ RADIUS_NUM }})),
      ),
      child: Text(text, style: const TextStyle(color: Color({{ DARK_BG_ARGB }}), fontWeight: FontWeight.bold)),
    );
  }
}
"""

    def create_inputs(self) -> str:
        return """
import 'package:flutter/material.dart';

class AtomInput extends StatelessWidget {
  final String hintText;
  final TextEditingController controller;
  final bool obscureText;

  const AtomInput({
    Key? key,
    required this.hintText,
    required this.controller,
    this.obscureText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      obscureText: obscureText,
      style: const TextStyle(color: Color({{ TEXT_COLOR_ARGB }})),
      decoration: InputDecoration(
        hintText: hintText,
        hintStyle: const TextStyle(color: Color({{ SUBTEXT_COLOR_ARGB }})),
        filled: true,
        fillColor: const Color({{ CARD_BG_ARGB }}),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular({{ RADIUS_NUM }}),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }
}
"""

    def create_labels(self) -> str:
        return """
import 'package:flutter/material.dart';

class AtomLabel extends StatelessWidget {
  final String text;
  final double fontSize;
  final bool bold;
  final Color color;

  const AtomLabel({
    Key? key,
    required this.text,
    this.fontSize = 16,
    this.bold = false,
    this.color = const Color({{ TEXT_COLOR_ARGB }}),
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: TextStyle(
        fontSize: fontSize,
        fontWeight: bold ? FontWeight.bold : FontWeight.normal,
        color: color,
      ),
    );
  }
}
"""

    def create_async_hook(self) -> str:
        return """
import 'dart:async';

class UseAsync {
  bool loading = false;
  
  Future<T?> execute<T>(Future<T> Function() asyncFn, {void Function(String)? onError}) async {
    if (loading) return null;
    loading = true;
    try {
      return await asyncFn();
    } catch (e) {
      if (onError != null) onError(e.toString());
      return null;
    } finally {
      loading = false;
    }
  }
}
"""

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return f"""
class Use{pascal_name} {{
  final dynamic context;
  bool loading = false;
  String errorMsg = "";

  Use{pascal_name}(this.context);
}}
"""

    def create_ui_inspector(self) -> str:
        return """
import 'package:flutter/material.dart';

class UIInspector extends StatelessWidget {
  const UIInspector({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      color: Colors.black.withOpacity(0.8),
      child: const Text(
        'UI Inspector (F11 to Capture)',
        style: TextStyle(color: Colors.white, fontSize: 10),
      ),
    );
  }
}
"""

    def create_main_window(self, project_name: str) -> str:
        return f"""
import 'package:flutter/material.dart';
import 'level_05_pages/welcome_page.dart';

void main() {{
  runApp(const MyApp());
}}

class MyApp extends StatelessWidget {{
  const MyApp({{Key? key}}) : super(key: key);

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{project_name}',
      theme: ThemeData(
        scaffoldBackgroundColor: const Color({{ DARK_BG_ARGB }}),
      ),
      home: const WelcomePage(),
    );
  }}
}}
"""
