import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:neopredict_v1/core/theme/app_theme.dart';
import 'package:neopredict_v1/presentation/widgets/neon_container.dart';
import 'package:neopredict_v1/presentation/widgets/gradient_chart.dart';

import 'package:neopredict_v1/presentation/providers/data_provider.dart';

class PredictionView extends ConsumerWidget {
  const PredictionView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dataAsync = ref.watch(companyDataProvider);

    return dataAsync.when(
      loading: () => const Center(
        child: CircularProgressIndicator(color: AppTheme.neonMagenta),
      ),
      error: (err, stack) => Center(child: Text("Error: $err")),
      data: (marketData) {
        if (marketData.prediction.isEmpty) {
          return const Center(
            child: Text(
              "No hay predicciones disponibles",
              style: TextStyle(color: Colors.white54),
            ),
          );
        }
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              NeonContainer(
                neonColor: AppTheme.neonMagenta,
                intense: true,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "FUTURECAST IA",
                      style: TextStyle(
                        color: AppTheme.neonMagenta,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    GradientChart(
                      data: marketData.prediction,
                      isPrediction: true,
                    ),
                    const SizedBox(height: 24),
                    _buildPredictionInfo(),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                "ANÁLISIS DE FACTORES",
                style: TextStyle(color: Colors.white54, letterSpacing: 1.2),
              ),
              const SizedBox(height: 16),
              _buildFactorBar("Sentimiento Memorias", 0.7, AppTheme.neonCyan),
              _buildFactorBar("Volatilidad Mercado", 0.4, Colors.orange),
              _buildFactorBar("Tendencia Técnica", 0.8, AppTheme.primaryBlue),
            ],
          ),
        );
      },
    );
  }

  Widget _buildPredictionInfo() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        _buildStat("TENDENCIA 2024", "ALCISTA", AppTheme.neonCyan),
        _buildStat("CONFIANZA", "85%", Colors.white),
      ],
    );
  }

  Widget _buildStat(String label, String value, Color color) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 10, color: Colors.white54),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: color,
            shadows: [
              Shadow(blurRadius: 8.0, color: color.withValues(alpha: 0.6)),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildFactorBar(String label, double pct, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(fontSize: 12, color: Colors.white70),
          ),
          const SizedBox(height: 6),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: pct,
              backgroundColor: Colors.white10,
              color: color,
              minHeight: 6,
            ),
          ),
        ],
      ),
    );
  }
}
