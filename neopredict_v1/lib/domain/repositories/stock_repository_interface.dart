import 'package:neopredict_v1/domain/entities/stock_data.dart';

abstract class StockRepositoryInterface {
  Future<List<StockData>> getHistoricalData(String ticker);
  Future<List<StockData>> getPredictionData(String ticker);
}
