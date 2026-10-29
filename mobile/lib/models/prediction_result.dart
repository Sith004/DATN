class RiskFactor {
  final String feature;
  final double shapValue;
  final double rawValue;
  final String direction;

  RiskFactor({
    required this.feature,
    required this.shapValue,
    required this.rawValue,
    required this.direction,
  });

  factory RiskFactor.fromJson(Map<String, dynamic> json) {
    return RiskFactor(
      feature: json['feature'] ?? '',
      shapValue: (json['shap_value'] ?? 0.0).toDouble(),
      rawValue: (json['raw_value'] ?? 0.0).toDouble(),
      direction: json['direction'] ?? '',
    );
  }
}

class PredictionResult {
  final double predictionProbability;
  final String predictionLabel;
  final String riskLevel;
  final double threshold;
  final String modelVersion;
  final int? recordId;
  final bool persisted;
  final String persistenceMessage;
  final List<RiskFactor> topRiskFactors;

  PredictionResult({
    required this.predictionProbability,
    required this.predictionLabel,
    required this.riskLevel,
    required this.threshold,
    required this.modelVersion,
    this.recordId,
    required this.persisted,
    required this.persistenceMessage,
    required this.topRiskFactors,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    var rawFactors = json['top_risk_factors'] as List<dynamic>? ?? [];
    List<RiskFactor> factors =
        rawFactors.map((e) => RiskFactor.fromJson(e)).toList();

    return PredictionResult(
      predictionProbability: (json['prediction_probability'] ?? 0.0).toDouble(),
      predictionLabel: json['prediction_label'] ?? 'Unknown',
      riskLevel: json['risk_level'] ?? 'Unknown',
      threshold: (json['threshold'] ?? 0.60).toDouble(),
      modelVersion: json['model_version'] ?? 'xgboost_tuned_v1',
      recordId: json['record_id'],
      persisted: json['persisted'] ?? false,
      persistenceMessage: json['persistence_message'] ?? '',
      topRiskFactors: factors,
    );
  }

  bool get isDefault => predictionProbability >= threshold;
}
