class PredictionHistoryItem {
  final int id;
  final String createdAt;
  final double limitBal;
  final int age;
  final double defaultProbability;
  final String predictionLabel;
  final String riskLevel;
  final String modelVersion;

  PredictionHistoryItem({
    required this.id,
    required this.createdAt,
    required this.limitBal,
    required this.age,
    required this.defaultProbability,
    required this.predictionLabel,
    required this.riskLevel,
    required this.modelVersion,
  });

  factory PredictionHistoryItem.fromJson(Map<String, dynamic> json) {
    return PredictionHistoryItem(
      id: json['id'] ?? 0,
      createdAt: json['created_at'] ?? '',
      limitBal: (json['limit_bal'] ?? 0.0).toDouble(),
      age: json['age'] ?? 0,
      defaultProbability: (json['default_probability'] ?? 0.0).toDouble(),
      predictionLabel: json['prediction_label'] ?? '',
      riskLevel: json['risk_level'] ?? '',
      modelVersion: json['model_version'] ?? '',
    );
  }
}

class PredictionHistoryResponse {
  final List<PredictionHistoryItem> items;
  final int total;
  final int page;
  final int pageSize;

  PredictionHistoryResponse({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
  });

  factory PredictionHistoryResponse.fromJson(Map<String, dynamic> json) {
    var rawList = json['items'] as List<dynamic>? ?? [];
    List<PredictionHistoryItem> parsedItems =
        rawList.map((e) => PredictionHistoryItem.fromJson(e)).toList();

    return PredictionHistoryResponse(
      items: parsedItems,
      total: json['total'] ?? 0,
      page: json['page'] ?? 1,
      pageSize: json['page_size'] ?? 10,
    );
  }
}
