class HealthStatus {
  final String status;
  final String apiVersion;
  final bool modelReady;
  final String modelName;
  final double threshold;
  final bool databaseConnected;
  final String databaseStatusMessage;

  HealthStatus({
    required this.status,
    required this.apiVersion,
    required this.modelReady,
    required this.modelName,
    required this.threshold,
    required this.databaseConnected,
    required this.databaseStatusMessage,
  });

  factory HealthStatus.fromJson(Map<String, dynamic> json) {
    return HealthStatus(
      status: json['status'] ?? 'unknown',
      apiVersion: json['api_version'] ?? '1.0.0',
      modelReady: json['model_ready'] ?? false,
      modelName: json['model_name'] ?? '',
      threshold: (json['threshold'] ?? 0.60).toDouble(),
      databaseConnected: json['database_connected'] ?? false,
      databaseStatusMessage: json['database_status_message'] ?? '',
    );
  }

  bool get isHealthy => status == 'healthy';
}
