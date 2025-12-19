import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:neopredict_v1/domain/entities/company.dart';

// Defaults to SQM-B
final selectedCompanyProvider = StateProvider<Company>((ref) {
  return ipsaCompanies[0];
});
