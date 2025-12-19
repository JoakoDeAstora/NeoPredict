class StockData {
  final double year; // Supports decimal years like 2020.5 (June)
  final double value;
  final double sentimentScore; // -1.0 to 1.0

  StockData({
    required this.year,
    required this.value,
    required this.sentimentScore,
  });
}

class PredictionData {
  final double targetYear;
  final String trend; // Bullish, Bearish, Neutral
  final double confidence;
  final double projectedValue; // Optional, illustrative

  PredictionData({
    required this.targetYear,
    required this.trend,
    required this.confidence,
    this.projectedValue = 0.0,
  });
}
