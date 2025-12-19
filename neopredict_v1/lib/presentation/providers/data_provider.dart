import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:neopredict_v1/data/repositories/mock_stock_repository.dart';
import 'package:neopredict_v1/domain/entities/stock_data.dart';
import 'package:neopredict_v1/presentation/providers/company_provider.dart';

// Repository Provider (Switched to Mock for Demo/Stability)
final stockRepositoryProvider = Provider((ref) => MockStockRepository());

// Data State Class
class CompanyMarketData {
  final List<StockData> history;
  final List<StockData> prediction;

  CompanyMarketData({required this.history, required this.prediction});
}

// Main Data Provider
final companyDataProvider = FutureProvider<CompanyMarketData>((ref) async {
  final company = ref.watch(selectedCompanyProvider);
  final repo = ref.watch(stockRepositoryProvider);

  final history = await repo.getHistoricalData(company.ticker);
  final prediction = await repo.getPredictionData(company.ticker);

  return CompanyMarketData(history: history, prediction: prediction);
});
