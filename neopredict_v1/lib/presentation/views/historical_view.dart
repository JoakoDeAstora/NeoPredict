import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:neopredict_v1/presentation/widgets/neon_container.dart';
import 'package:neopredict_v1/presentation/widgets/gradient_chart.dart';

import 'package:neopredict_v1/presentation/providers/data_provider.dart';

class HistoricalView extends ConsumerWidget {
  const HistoricalView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dataAsync = ref.watch(companyDataProvider);

    return dataAsync.when(
      loading: () =>
          const Center(child: CircularProgressIndicator(color: Colors.cyan)),
      error: (err, stack) => Center(
        child: Text("Error: $err", style: const TextStyle(color: Colors.red)),
      ),
      data: (marketData) {
        if (marketData.history.isEmpty) {
          return const Center(
            child: Text(
              "No hay datos disponibles",
              style: TextStyle(color: Colors.white54),
            ),
          );
        }
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              NeonContainer(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "EVOLUCIÓN DE PRECIO",
                      style: TextStyle(color: Colors.white54),
                    ),
                    const SizedBox(height: 16),
                    GradientChart(data: marketData.history),
                    const SizedBox(height: 16),
                    _buildSentimentLegend(),
                  ],
                ),
              ),
              const SizedBox(height: 20),
              // Dynamic metrics based on last year data
              _buildDetailRow(
                "Cierre Año Anterior",
                "\$${marketData.history.last.value.toInt()}",
              ),
              _buildDetailRow(
                "Sentimiento Reciente",
                _getSentimentLabel(marketData.history.last.sentimentScore),
              ),
            ],
          ),
        );
      },
    );
  }

  String _getSentimentLabel(double score) {
    if (score > 0.3) return "Positivo (+${(score * 100).toInt()}%)";
    if (score < -0.3) return "Negativo (${(score * 100).toInt()}%)";
    return "Neutral";
  }

  Widget _buildSentimentLegend() {
    return const Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(Icons.circle, size: 8, color: Colors.cyanAccent),
        SizedBox(width: 4),
        Text(
          "Sentimiento Positivo",
          style: TextStyle(fontSize: 10, color: Colors.white70),
        ),
        SizedBox(width: 16),
        Icon(Icons.circle, size: 8, color: Colors.purpleAccent),
        SizedBox(width: 4),
        Text(
          "Sentimiento Negativo",
          style: TextStyle(fontSize: 10, color: Colors.white70),
        ),
      ],
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.white70)),
          Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          ),
        ],
      ),
    );
  }
}
