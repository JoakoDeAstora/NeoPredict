import 'package:neopredict_v1/domain/entities/stock_data.dart';
import 'package:neopredict_v1/domain/repositories/stock_repository_interface.dart';

class MockStockRepository implements StockRepositoryInterface {
  // Database "State" - Easy to update
  final Map<String, List<StockData>> _historyDB = {
    'SQM-B': [
      StockData(year: 2019, value: 25, sentimentScore: 0.1),
      StockData(year: 2020, value: 35, sentimentScore: 0.4),
      StockData(year: 2021, value: 55, sentimentScore: 0.8), // Boom
      StockData(year: 2022, value: 85, sentimentScore: 0.9),
      StockData(year: 2023, value: 60, sentimentScore: -0.2), // Correction
    ],
    'CHILE': [
      StockData(year: 2019, value: 80, sentimentScore: 0.3),
      StockData(
        year: 2020,
        value: 75,
        sentimentScore: -0.4,
      ), // Social unrest/Pandemic
      StockData(year: 2021, value: 82, sentimentScore: 0.2),
      StockData(year: 2022, value: 90, sentimentScore: 0.5),
      StockData(year: 2023, value: 95, sentimentScore: 0.6), // Stability
    ],
    'CENCOSUD': [
      StockData(year: 2019, value: 1200, sentimentScore: 0.0),
      StockData(year: 2020, value: 900, sentimentScore: -0.6),
      StockData(year: 2021, value: 1400, sentimentScore: 0.5),
      StockData(year: 2022, value: 1350, sentimentScore: 0.2),
      StockData(year: 2023, value: 1500, sentimentScore: 0.7),
    ],
  };

  final Map<String, List<StockData>> _predictionDB = {
    'SQM-B': [
      StockData(year: 2023, value: 60, sentimentScore: -0.2),
      StockData(
        year: 2024,
        value: 75,
        sentimentScore: 0.4,
      ), // Rebound predicted
    ],
    'CHILE': [
      StockData(year: 2023, value: 95, sentimentScore: 0.6),
      StockData(year: 2024, value: 98, sentimentScore: 0.5), // Slow growth
    ],
    'CENCOSUD': [
      StockData(year: 2023, value: 1500, sentimentScore: 0.7),
      StockData(year: 2024, value: 1650, sentimentScore: 0.8), // Expansion
    ],
  };

  @override
  Future<List<StockData>> getHistoricalData(String ticker) async {
    await Future.delayed(const Duration(milliseconds: 300)); // Simulate latency
    return _historyDB[ticker] ?? _historyDB['SQM-B']!; // Fallback
  }

  @override
  Future<List<StockData>> getPredictionData(String ticker) async {
    await Future.delayed(const Duration(milliseconds: 300));
    return _predictionDB[ticker] ?? _predictionDB['SQM-B']!;
  }
}
