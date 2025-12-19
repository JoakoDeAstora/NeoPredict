import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:neopredict_v1/core/theme/app_theme.dart';
import 'package:neopredict_v1/domain/entities/company.dart';
import 'package:neopredict_v1/presentation/providers/company_provider.dart';
import 'package:neopredict_v1/presentation/views/historical_view.dart';
import 'package:neopredict_v1/presentation/views/prediction_view.dart';

class HomeLayout extends ConsumerStatefulWidget {
  const HomeLayout({super.key});

  @override
  ConsumerState<HomeLayout> createState() => _HomeLayoutState();
}

class _HomeLayoutState extends ConsumerState<HomeLayout> {
  int _currentIndex = 0;

  final List<Widget> _views = const [HistoricalView(), PredictionView()];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // App Name on the left
        title: const Text(
          "NeoPredict",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            letterSpacing: 2.0,
            fontSize: 22,
            color: AppTheme.neonCyan,
            shadows: [
              Shadow(
                blurRadius: 10.0,
                color: AppTheme.neonCyan,
                offset: Offset(0, 0),
              ),
            ],
          ),
        ),
        centerTitle: false,
        // Filter on the right as an action/widget
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: _buildCompanySelector(ref),
          ),
        ],
      ),
      body: _views[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        backgroundColor: AppTheme.background,
        selectedItemColor: AppTheme.neonCyan,
        unselectedItemColor: Colors.white24,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.history),
            label: 'Histórico',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.auto_graph),
            label: 'Predicciones',
          ),
        ],
      ),
    );
  }

  Widget _buildCompanySelector(WidgetRef ref) {
    final selectedCompany = ref.watch(selectedCompanyProvider);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: AppTheme.surface.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.primaryBlue.withValues(alpha: 0.3)),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<Company>(
          value: selectedCompany,
          dropdownColor: AppTheme.surface,
          icon: const Icon(Icons.arrow_drop_down, color: AppTheme.neonCyan),
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
          onChanged: (Company? newValue) {
            if (newValue != null) {
              ref.read(selectedCompanyProvider.notifier).state = newValue;
            }
          },
          items: ipsaCompanies.map<DropdownMenuItem<Company>>((
            Company company,
          ) {
            return DropdownMenuItem<Company>(
              value: company,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(company.ticker),
                  const SizedBox(width: 8),
                  Text(
                    "| ${company.sector}",
                    style: const TextStyle(color: Colors.white38, fontSize: 12),
                  ),
                ],
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}
