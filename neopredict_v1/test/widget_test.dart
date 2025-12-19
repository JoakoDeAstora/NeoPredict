// This is a basic Flutter widget test.

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:neopredict_v1/main.dart';
import 'package:neopredict_v1/presentation/pages/home_layout.dart';

void main() {
  testWidgets('App renders HomeLayout smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    // We must wrap the app in a ProviderScope for Riverpod to work.
    await tester.pumpWidget(const ProviderScope(child: NeoPredictApp()));
    await tester.pumpAndSettle(); // Wait for navigation and animations

    // Verify that HomeLayout is present.
    expect(find.byType(HomeLayout), findsOneWidget);

    // Verify that the title is present (part of the AppBar).
    expect(find.text('NeoPredict'), findsOneWidget);
  });
}
