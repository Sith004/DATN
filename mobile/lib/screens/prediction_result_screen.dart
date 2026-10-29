import 'package:flutter/material.dart';
import '../models/customer_input.dart';
import '../models/prediction_result.dart';
import '../theme/app_theme.dart';
import 'prediction_history_screen.dart';

class PredictionResultScreen extends StatelessWidget {
  final PredictionResult result;
  final CustomerInput input;

  const PredictionResultScreen({
    super.key,
    required this.result,
    required this.input,
  });

  @override
  Widget build(BuildContext context) {
    final double probPercent = result.predictionProbability * 100;
    final bool isDefault = result.isDefault;

    Color riskColor;
    Color riskBgColor;
    IconData riskIcon;

    if (result.riskLevel == 'High Risk') {
      riskColor = AppTheme.riskHigh;
      riskBgColor = AppTheme.riskHighBg;
      riskIcon = Icons.warning_amber_rounded;
    } else if (result.riskLevel == 'Medium Risk') {
      riskColor = AppTheme.riskMedium;
      riskBgColor = AppTheme.riskMediumBg;
      riskIcon = Icons.info_outline;
    } else {
      riskColor = AppTheme.riskLow;
      riskBgColor = AppTheme.riskLowBg;
      riskIcon = Icons.verified_user_outlined;
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('KẾT QUẢ DỰ BÁO RỦI RO'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. Persistence Notification Banner
            _buildPersistenceBanner(context),

            const SizedBox(height: 14),

            // 2. Main Risk Classification Card
            Card(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: riskBgColor,
                        shape: BoxShape.circle,
                      ),
                      child: Icon(riskIcon, color: riskColor, size: 48),
                    ),
                    const SizedBox(height: 14),
                    Text(
                      isDefault ? '⚠️ CẢNH BÁO: DEFAULT' : '✅ AN TOÀN: NON-DEFAULT',
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: isDefault ? AppTheme.riskHigh : AppTheme.riskLow,
                        letterSpacing: 0.5,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 6),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                      decoration: BoxDecoration(
                        color: riskBgColor,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: riskColor, width: 1.5),
                      ),
                      child: Text(
                        'Mức rủi ro: ${result.riskLevel}',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: riskColor,
                        ),
                      ),
                    ),
                    const SizedBox(height: 18),
                    const Divider(),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildMetricColumn(
                          'Xác suất Vỡ nợ (Default)',
                          '${probPercent.toStringAsFixed(2)}%',
                          riskColor,
                        ),
                        Container(width: 1, height: 40, color: Colors.grey.shade300),
                        _buildMetricColumn(
                          'Ngưỡng quyết định',
                          '${(result.threshold * 100).toInt()}%',
                          AppTheme.primaryNavy,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 14),

            // 3. Business Interpretation Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.lightbulb_outline, color: AppTheme.accentCyan, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Ý nghĩa kết quả kinh doanh',
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      isDefault
                          ? 'Mô hình XGBoost đánh giá khách hàng này có xác suất vỡ nợ (${probPercent.toStringAsFixed(1)}%) vượt qua ngưỡng rủi ro 60%. '
                            'Khuyến nghị thẩm định chuyên sâu trước khi phê duyệt hạn mức.'
                          : (result.riskLevel == 'Medium Risk'
                              ? 'Khách hàng có mức độ rủi ro trung bình (30% - 59%). Cần xem xét thêm lịch sử thanh toán các kỳ gần nhất.'
                              : 'Khách hàng có độ tin cậy tín dụng cao (< 30% rủi ro). Hồ sơ đủ điều kiện phê duyệt hạn mức bình thường.'),
                      style: const TextStyle(fontSize: 13, height: 1.4, color: Color(0xFF334155)),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 14),

            // 4. Explainable AI (Top SHAP Contributors)
            if (result.topRiskFactors.isNotEmpty) ...[
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.psychology, color: AppTheme.primaryNavy, size: 20),
                          SizedBox(width: 8),
                          Text(
                            'Giải thích SHAP (Top yếu tố ảnh hưởng)',
                            style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      for (var factor in result.topRiskFactors) ...[
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Row(
                            children: [
                              Expanded(
                                flex: 4,
                                child: Text(
                                  factor.feature,
                                  style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                                ),
                              ),
                              Expanded(
                                flex: 3,
                                child: Text(
                                  'Giá trị: ${factor.rawValue.toStringAsFixed(1)}',
                                  style: const TextStyle(fontSize: 12, color: Color(0xFF64748B)),
                                ),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                decoration: BoxDecoration(
                                  color: factor.shapValue > 0 ? AppTheme.riskHighBg : AppTheme.riskLowBg,
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(
                                  factor.direction,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: factor.shapValue > 0 ? AppTheme.riskHigh : AppTheme.riskLow,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        if (factor != result.topRiskFactors.last) const Divider(height: 8),
                      ],
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 14),
            ],

            // 5. Educational Disclaimer
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFFF1F5F9),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: const Color(0xFFE2E8F0)),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.info_outline, size: 18, color: Color(0xFF64748B)),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Tuyên bố học thuật: Kết quả dự báo là ước tính từ mô hình Machine Learning phục vụ nghiên cứu khóa luận tốt nghiệp, không thay thế cho quyết định phê duyệt tín dụng của ngân hàng hoặc tổ chức tài chính.',
                      style: TextStyle(fontSize: 11, color: Colors.grey.shade700, height: 1.3),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // 6. Navigation Buttons
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Nhập lại'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    onPressed: () => Navigator.pop(context),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.history),
                    label: const Text('Xem Lịch sử'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryNavy,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const PredictionHistoryScreen()),
                      );
                    },
                  ),
                ),
              ],
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildPersistenceBanner(BuildContext context) {
    if (result.persisted) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: AppTheme.riskLowBg,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: AppTheme.riskLow),
        ),
        child: Row(
          children: [
            const Icon(Icons.check_circle, color: AppTheme.riskLow, size: 20),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'PostgreSQL: Đã lưu bản ghi #${result.recordId ?? 'N/A'} an toàn.',
                style: const TextStyle(color: AppTheme.riskLow, fontSize: 13, fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      );
    } else {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: AppTheme.riskMediumBg,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: AppTheme.riskMedium),
        ),
        child: Row(
          children: [
            const Icon(Icons.cloud_off, color: AppTheme.riskMedium, size: 20),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'Cơ sở dữ liệu: ${result.persistenceMessage}',
                style: const TextStyle(color: AppTheme.riskMedium, fontSize: 13),
              ),
            ),
          ],
        ),
      );
    }
  }

  Widget _buildMetricColumn(String label, String value, Color color) {
    return Column(
      children: [
        Text(label, style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
        const SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }
}
