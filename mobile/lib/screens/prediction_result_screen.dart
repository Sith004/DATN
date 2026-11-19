import 'package:flutter/material.dart';
import '../models/customer_input.dart';
import '../models/prediction_result.dart';
import '../theme/app_theme.dart';
import '../widgets/banking_components.dart';
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

    if (result.riskLevel == 'High Risk' || isDefault) {
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
        title: const Text('KẾT QUẢ THẨM ĐỊNH TÍN DỤNG'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. Thông báo trạng thái Lưu trữ PostgreSQL
            _buildPersistenceBanner(context),

            const SizedBox(height: 14),

            // 2. Thẻ Đánh giá Rủi ro Tổng thể phong cách Báo cáo Tài chính
            Card(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 22, horizontal: 16),
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: riskBgColor,
                        shape: BoxShape.circle,
                        border: Border.all(color: riskColor.withValues(alpha: 0.3), width: 2),
                      ),
                      child: Icon(riskIcon, color: riskColor, size: 48),
                    ),
                    const SizedBox(height: 14),

                    Text(
                      isDefault ? 'CẢNH BÁO: KHÁCH HÀNG VỠ NỢ' : 'AN TOÀN: ĐỦ TIÊU CHUẨN TÍN DỤNG',
                      style: TextStyle(
                        fontSize: 18.5,
                        fontWeight: FontWeight.w800,
                        color: riskColor,
                        letterSpacing: 0.3,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),

                    RiskBadge(
                      riskLevel: result.riskLevel,
                      isDefault: isDefault,
                      probability: result.predictionProbability,
                    ),

                    const SizedBox(height: 20),
                    const Divider(height: 1),
                    const SizedBox(height: 16),

                    // Hai cột chỉ số: Xác suất vs Ngưỡng quyết định
                    Row(
                      children: [
                        Expanded(
                          child: _buildMetricColumn(
                            'Xác suất Vỡ nợ (PD)',
                            '${probPercent.toStringAsFixed(2)}%',
                            riskColor,
                            'Mô hình XGBoost',
                          ),
                        ),
                        Container(width: 1, height: 48, color: AppTheme.cardBorder),
                        Expanded(
                          child: _buildMetricColumn(
                            'Ngưỡng Quyết định',
                            '${(result.threshold * 100).toInt()}%',
                            AppTheme.headingNavy,
                            'Threshold tối ưu W8',
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 16),

                    // Thước đo xác suất trực quan (Probability Progress Bar)
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              'Thước đo Rủi ro (0% - 100%)',
                              style: TextStyle(fontSize: 11.5, color: AppTheme.bodyText, fontWeight: FontWeight.w500),
                            ),
                            Text(
                              isDefault ? 'Vượt ngưỡng +${(probPercent - 60).toStringAsFixed(1)}%' : 'Dưới ngưỡng rủi ro',
                              style: TextStyle(
                                fontSize: 11.5,
                                color: riskColor,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(6),
                          child: LinearProgressIndicator(
                            value: result.predictionProbability.clamp(0.0, 1.0),
                            minHeight: 10,
                            backgroundColor: AppTheme.backgroundLight,
                            valueColor: AlwaysStoppedAnimation<Color>(riskColor),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 14),

            // 3. Ý nghĩa Nghiệp vụ & Khuyến nghị Thẩm định
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.lightbulb_outline, color: AppTheme.primaryGreen, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Khuyến nghị Thẩm định Nghiệp vụ',
                          style: TextStyle(fontSize: 14.5, fontWeight: FontWeight.w700, color: AppTheme.headingNavy),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      isDefault
                          ? 'Mô hình XGBoost Tuned ước tính xác suất vỡ nợ của hồ sơ đạt ${probPercent.toStringAsFixed(1)}%, vượt ngưỡng rủi ro cho phép (60.0%). '
                            'Khuyến nghị phòng Thẩm định từ chối cấp hạn mức tín dụng mới hoặc yêu cầu bổ sung tài sản bảo đảm.'
                          : (result.riskLevel == 'Medium Risk'
                              ? 'Hồ sơ có mức độ rủi ro trung bình (${probPercent.toStringAsFixed(1)}%). Khuyến nghị xem xét lại lịch sử thanh toán 3 tháng gần nhất trước khi phê duyệt.'
                              : 'Khách hàng có lịch sử tín dụng chuẩn mực, xác suất rủi ro thấp (${probPercent.toStringAsFixed(1)}% < 30%). Hồ sơ đáp ứng tiêu chuẩn phê duyệt hạn mức thẻ tín dụng theo quy chuẩn.'),
                      style: const TextStyle(fontSize: 12.8, height: 1.45, color: AppTheme.bodyText),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 14),

            // 4. Giải thích Minh bạch với SHAP (Explainable AI)
            if (result.topRiskFactors.isNotEmpty) ...[
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.psychology_outlined, color: AppTheme.primaryGreen, size: 20),
                          SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              'Giải thích SHAP (Top Yếu tố Ảnh hưởng)',
                              style: TextStyle(fontSize: 14.5, fontWeight: FontWeight.w700, color: AppTheme.headingNavy),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Phân tích đóng góp cục bộ (Local Explanation) qua TreeExplainer',
                        style: TextStyle(fontSize: 11.5, color: AppTheme.bodyText),
                      ),
                      const SizedBox(height: 12),
                      for (var factor in result.topRiskFactors) ...[
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Row(
                            children: [
                              Expanded(
                                flex: 4,
                                child: Text(
                                  factor.feature,
                                  style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: AppTheme.headingNavy),
                                ),
                              ),
                              Expanded(
                                flex: 3,
                                child: Text(
                                  'Giá trị: ${factor.rawValue.toStringAsFixed(1)}',
                                  style: const TextStyle(fontSize: 11.5, color: AppTheme.bodyText),
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
                                    fontWeight: FontWeight.w700,
                                    color: factor.shapValue > 0 ? AppTheme.riskHigh : AppTheme.riskLow,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        if (factor != result.topRiskFactors.last) const Divider(height: 8, color: AppTheme.dividerColor),
                      ],
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 14),
            ],

            // 5. Nút điều hướng Hành động
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    icon: const Icon(Icons.history_edu, size: 18),
                    label: const Text('Xem Sổ phụ'),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const PredictionHistoryScreen(),
                        ),
                      );
                    },
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.replay, size: 18),
                    label: const Text('Hồ sơ Mới'),
                    onPressed: () => Navigator.pop(context),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 18),

            // 6. Educational Disclaimer
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppTheme.backgroundLight,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppTheme.cardBorder),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.info_outline, size: 16, color: AppTheme.bodyText),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: Text(
                      'Tuyên bố học thuật: Kết quả dự báo là sản phẩm thực nghiệm của mô hình Machine Learning phục vụ Đồ án Tốt nghiệp tại HCMUNRE, đóng vai trò công cụ hỗ trợ ra quyết định (DSS).',
                      style: TextStyle(fontSize: 11, color: AppTheme.bodyText, height: 1.35),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
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
          border: Border.all(color: AppTheme.riskLow.withValues(alpha: 0.3)),
        ),
        child: Row(
          children: [
            const Icon(Icons.cloud_done, color: AppTheme.riskLow, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'Đã lưu hồ sơ vào PostgreSQL (Mã hồ sơ: #${result.recordId ?? "N/A"})',
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppTheme.riskLow),
                overflow: TextOverflow.ellipsis,
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
          border: Border.all(color: AppTheme.riskMedium.withValues(alpha: 0.3)),
        ),
        child: Row(
          children: [
            const Icon(Icons.cloud_off, color: AppTheme.riskMedium, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                result.persistenceMessage.isNotEmpty
                    ? result.persistenceMessage
                    : 'Chưa kết nối CSDL PostgreSQL (Hoạt động ở chế độ Graceful)',
                style: const TextStyle(fontSize: 12, color: AppTheme.riskMedium, fontWeight: FontWeight.w600),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
      );
    }
  }

  Widget _buildMetricColumn(String label, String value, Color color, String sublabel) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: AppTheme.bodyText, fontWeight: FontWeight.w500),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w800,
            color: color,
            letterSpacing: 0.3,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          sublabel,
          style: const TextStyle(fontSize: 10.5, color: AppTheme.textMuted),
        ),
      ],
    );
  }
}
