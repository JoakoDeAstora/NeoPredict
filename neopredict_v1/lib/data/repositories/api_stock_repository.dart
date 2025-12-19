import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:neopredict_v1/domain/entities/stock_data.dart';
import 'package:neopredict_v1/domain/repositories/stock_repository_interface.dart';

class ApiStockRepository implements StockRepositoryInterface {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'http://127.0.0.1:8000', // Localhost for Windows
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 5),
    ),
  );

  @override
  Future<List<StockData>> getHistoricalData(String ticker) async {
    try {
      final response = await _dio.get('/market/$ticker/history');
      final List<dynamic> data = response.data;

      return data
          .map(
            (json) => StockData(
              year: (json['year'] as num).toDouble(),
              value: (json['value'] as num).toDouble(),
              sentimentScore: (json['sentimentScore'] as num).toDouble(),
            ),
          )
          .toList();
    } catch (e) {
      debugPrint("Error fetching history: $e");
      return []; // Return empty on error to avoid crash
    }
  }

  @override
  Future<List<StockData>> getPredictionData(String ticker) async {
    try {
      final response = await _dio.get('/market/$ticker/prediction');
      final List<dynamic> data = response.data;

      return data
          .map(
            (json) => StockData(
              year: (json['year'] as num).toDouble(),
              value: (json['value'] as num).toDouble(),
              sentimentScore: (json['sentimentScore'] as num).toDouble(),
            ),
          )
          .toList();
    } catch (e) {
      debugPrint("Error fetching prediction: $e");
      return [];
    }
  }
}
