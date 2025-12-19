import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:neopredict_v1/core/theme/app_theme.dart';
import 'package:neopredict_v1/presentation/pages/home_layout.dart';

void main() {
  runApp(const ProviderScope(child: NeoPredictApp()));
}

class NeoPredictApp extends StatelessWidget {
  const NeoPredictApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NeoPredict',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.theme,
      home: const HomeLayout(),
    );
  }
}
