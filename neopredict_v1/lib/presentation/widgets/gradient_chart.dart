import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:neopredict_v1/core/theme/app_theme.dart';
import 'package:neopredict_v1/domain/entities/stock_data.dart';

class GradientChart extends StatelessWidget {
  final List<StockData> data;
  final bool isPrediction;

  const GradientChart({
    super.key,
    required this.data,
    this.isPrediction = false,
  });

  @override
  Widget build(BuildContext context) {
    return AspectRatio(aspectRatio: 1.70, child: LineChart(mainData()));
  }

  LineChartData mainData() {
    return LineChartData(
      gridData: FlGridData(
        show: true,
        drawVerticalLine: true,
        getDrawingHorizontalLine: (value) {
          return const FlLine(color: Color(0xff37434d), strokeWidth: 1);
        },
        getDrawingVerticalLine: (value) {
          return const FlLine(color: Color(0xff37434d), strokeWidth: 1);
        },
      ),
      titlesData: FlTitlesData(
        show: true,
        rightTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 30,
            interval: 1,
            getTitlesWidget: bottomTitleWidgets,
          ),
        ),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            interval: 10, // Adjust based on data scale
            getTitlesWidget: leftTitleWidgets,
            reservedSize: 42,
          ),
        ),
      ),
      borderData: FlBorderData(
        show: true,
        border: Border.all(color: const Color(0xff37434d)),
      ),
      minX: data.first.year.toDouble(),
      maxX: data.last.year.toDouble(),
      minY: 0, // Should be dynamic based on min value
      maxY: 120, // Should be dynamic based on max value
      lineBarsData: [
        LineChartBarData(
          spots: data.map((e) => FlSpot(e.year.toDouble(), e.value)).toList(),
          isCurved: true,
          gradient: LinearGradient(
            colors: isPrediction
                ? [AppTheme.neonCyan, Colors.white]
                : [AppTheme.primaryBlue, AppTheme.neonCyan],
          ),
          barWidth: 4,
          isStrokeCapRound: true,
          dotData: FlDotData(
            show: true,
            getDotPainter: (spot, percent, barData, index) {
              // Show sentiment color on dots
              final sentiment = data[index].sentimentScore;
              Color dotColor = sentiment > 0
                  ? AppTheme.neonCyan
                  : AppTheme.neonMagenta;
              return FlDotCirclePainter(
                radius: 6,
                color: dotColor,
                strokeWidth: 2,
                strokeColor: Colors.white,
              );
            },
          ),
          belowBarData: BarAreaData(
            show: true,
            gradient: LinearGradient(
              colors: [
                (isPrediction ? AppTheme.neonCyan : AppTheme.primaryBlue)
                    .withValues(alpha: 0.3),
                (isPrediction ? AppTheme.neonCyan : AppTheme.primaryBlue)
                    .withValues(alpha: 0.0),
              ],

              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
        ),
      ],
    );
  }

  Widget bottomTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      fontWeight: FontWeight.bold,
      fontSize: 12,
      color: Colors.white54,
    );
    return SideTitleWidget(
      axisSide: meta.axisSide,
      child: Text(value.toInt().toString(), style: style),
    );
  }

  Widget leftTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      fontWeight: FontWeight.bold,
      fontSize: 12,
      color: Colors.white54,
    );
    return Text(
      value.toInt().toString(),
      style: style,
      textAlign: TextAlign.left,
    );
  }
}
