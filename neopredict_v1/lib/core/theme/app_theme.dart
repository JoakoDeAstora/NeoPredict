import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Palette
  static const Color background = Color(0xFF050A14); // Deep Black/Blue
  static const Color primaryBlue = Color(0xFF0047FF); // Electric Blue
  static const Color neonCyan = Color(0xFF00F3FF); // Neon Cyan (Data)
  static const Color neonMagenta = Color(0xFFD500F9); // Neon Magenta (Risk)
  static const Color surface = Color(0xFF0A1020); // Slightly lighter background

  static ThemeData get theme {
    return ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: background,
      primaryColor: primaryBlue,
      colorScheme: const ColorScheme.dark(
        primary: neonCyan,
        secondary: neonMagenta,
        surface: surface, // 'background' is deprecated, 'surface' covers it now
      ),
      textTheme: GoogleFonts.outfitTextTheme(
        ThemeData.dark().textTheme,
      ).apply(bodyColor: Colors.white, displayColor: Colors.white),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
    );
  }

  // Neon Glow Decoration Helper
  static BoxDecoration neonDecoration({
    Color color = neonCyan,
    double radius = 12,
    bool intense = false,
  }) {
    return BoxDecoration(
      color: surface.withValues(alpha: 0.8),
      borderRadius: BorderRadius.circular(radius),
      border: Border.all(color: color.withValues(alpha: 0.6), width: 1.5),

      boxShadow: [
        BoxShadow(
          color: color.withValues(alpha: intense ? 0.4 : 0.2),
          blurRadius: intense ? 12 : 8,
          spreadRadius: 1,
        ),
        if (intense)
          BoxShadow(
            color: color.withValues(alpha: 0.2),
            blurRadius: 20,
            spreadRadius: 2,
          ),
      ],
    );
  }
}
