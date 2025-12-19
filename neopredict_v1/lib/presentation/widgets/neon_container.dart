import 'package:flutter/material.dart';
import 'package:neopredict_v1/core/theme/app_theme.dart';

class NeonContainer extends StatelessWidget {
  final Widget child;
  final Color neonColor;
  final double padding;
  final double radius;
  final bool intense;

  const NeonContainer({
    super.key,
    required this.child,
    this.neonColor = AppTheme.neonCyan,
    this.padding = 16.0,
    this.radius = 16.0,
    this.intense = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(padding),
      decoration: AppTheme.neonDecoration(
        color: neonColor,
        radius: radius,
        intense: intense,
      ),
      child: child,
    );
  }
}
