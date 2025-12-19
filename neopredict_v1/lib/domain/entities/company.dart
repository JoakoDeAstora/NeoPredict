class Company {
  final String ticker;
  final String name;
  final String sector;

  const Company({
    required this.ticker,
    required this.name,
    required this.sector,
  });
}

// Mock Data List
const List<Company> ipsaCompanies = [
  Company(
    ticker: 'SQM-B',
    name: 'Sociedad Química y Minera',
    sector: 'Minería',
  ),
  Company(ticker: 'CHILE', name: 'Banco de Chile', sector: 'Financiero'),
  Company(ticker: 'CENCOSUD', name: 'Cencosud S.A.', sector: 'Retail'),
  Company(ticker: 'COPEC', name: 'Empresas Copec', sector: 'Energía'),
  Company(ticker: 'ENELAM', name: 'Enel Américas', sector: 'Utilities'),
  Company(ticker: 'LTM', name: 'Latam Airlines', sector: 'Transporte'),
];
