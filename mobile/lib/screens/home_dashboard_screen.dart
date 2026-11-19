import 'package:flutter/material.dart';
import '../models/health_status.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';
import '../widgets/banking_components.dart';
import 'customer_input_form_screen.dart';
import 'prediction_history_screen.dart';
import 'settings_screen.dart';

class HomeDashboardScreen extends StatefulWidget {
  const HomeDashboardScreen({super.key});

  @override
  State<HomeDashboardScreen> createState() => _HomeDashboardScreenState();
}

class _HomeDashboardScreenState extends State<HomeDashboardScreen> {
  HealthStatus? _healthStatus;
  bool _isLoadingHealth = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _checkServerStatus();
  }

  Future<void> _checkServerStatus() async {
    setState(() {
      _isLoadingHealth = true;
      _errorMessage = null;
    });

    try {
      final status = await ApiService.checkHealth();
      if (mounted) {
        setState(() {
          _healthStatus = status;
          _isLoadingHealth = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString();
          _isLoadingHealth = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ĐÁNH GIÁ RỦI RO TÍN DỤNG'),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune),
            tooltip: 'Cài đặt kết nối',
            onPressed: () async {
              await Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              );
              _checkServerStatus();
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        color: AppTheme.primaryGreen,
        onRefresh: _checkServerStatus,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 1. Academic Header Banner phong cách ngân hàng (Không bao giờ tràn)
              const BankingHeader(
                title: 'ỨNG DỤNG MACHINE LEARNING TRONG DỰ BÁO RỦI RO TÍN DỤNG',
                subtitle: 'Phân loại rủi ro vỡ nợ khách hàng thẻ tín dụng (Default Risk Scoring)',
                studentName: 'Nguyễn Trọng Thể',
                studentId: '1150080117',
              ),

              const SizedBox(height: 16),

              // 2. Chức năng Nghiệp vụ Chính (VCB Primary Action Cards)
              const SectionTitle(
                title: 'Nghiệp vụ Thẩm định Tín dụng',
                subtitle: 'Hệ sinh thái Hỗ trợ ra Quyết định (Decision Support System)',
              ),
              const SizedBox(height: 4),

              BankingActionCard(
                title: 'Đánh giá Rủi ro Khách hàng',
                subtitle: 'Nhập 23 thuộc tính tài chính & nhân khẩu học để tính xác suất vỡ nợ qua XGBoost',
                icon: Icons.analytics_outlined,
                iconColor: AppTheme.primaryGreen,
                iconBgColor: AppTheme.primaryLight,
                trailingBadge: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppTheme.primaryGreen,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Text(
                    'Mô hình 0.60',
                    style: TextStyle(color: Colors.white, fontSize: 10.5, fontWeight: FontWeight.bold),
                  ),
                ),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const CustomerInputFormScreen(),
                    ),
                  );
                },
              ),

              const SizedBox(height: 10),

              BankingActionCard(
                title: 'Sổ phụ Lịch sử Thẩm định',
                subtitle: 'Truy xuất hồ sơ dự báo được lưu trữ an toàn trong PostgreSQL 16',
                icon: Icons.history_edu,
                iconColor: AppTheme.headingNavy,
                iconBgColor: const Color(0xFFEAEFF4),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const PredictionHistoryScreen(),
                    ),
                  );
                },
              ),

              const SizedBox(height: 18),

              // 3. Thông số Mô hình Tuyển chọn (Chương 3)
              const SectionTitle(
                title: 'Mô hình Tuyển chọn (XGBoost Tuned)',
                subtitle: 'Huấn luyện trên 23,972 mẫu & kiểm định độc lập trên 5,993 mẫu',
                icon: Icons.verified_outlined,
              ),
              const SizedBox(height: 4),

              Card(
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          _buildMetricBox('Mô hình', 'XGBoost Tuned', Icons.psychology_outlined),
                          const SizedBox(width: 8),
                          _buildMetricBox('Ngưỡng (Threshold)', '0.60 (Tối ưu)', Icons.tune),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          _buildMetricBox('ROC-AUC', '0.7769', null),
                          const SizedBox(width: 8),
                          _buildMetricBox('PR-AUC', '0.5620', null),
                          const SizedBox(width: 8),
                          _buildMetricBox('F1-Score', '0.5409', null),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 18),

              // 4. Trạng thái Hệ thống Kết nối (Khu vực thông tin phụ - Chống tràn 100%)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Expanded(
                    child: SectionTitle(
                      title: 'Trạng thái Hạ tầng Kết nối',
                      subtitle: 'FastAPI REST, ML Pipeline & PostgreSQL',
                      icon: Icons.dns_outlined,
                    ),
                  ),
                  if (_isLoadingHealth)
                    const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.primaryGreen),
                    )
                  else
                    IconButton(
                      icon: const Icon(Icons.refresh, size: 20, color: AppTheme.primaryGreen),
                      onPressed: _checkServerStatus,
                      tooltip: 'Kiểm tra kết nối lại',
                      padding: EdgeInsets.zero,
                      constraints: const BoxConstraints(),
                    ),
                ],
              ),
              const SizedBox(height: 4),

              if (_healthStatus != null) ...[
                SystemStatusTile(
                  title: 'FastAPI Backend Engine',
                  statusText: 'Hoạt động bình thường (v${_healthStatus!.apiVersion})',
                  isOnline: _healthStatus!.isHealthy,
                  icon: Icons.api,
                ),
                const SizedBox(height: 6),
                SystemStatusTile(
                  title: 'XGBoost Model Pipeline',
                  statusText: _healthStatus!.modelReady ? 'Đã tải mô hình (Ngưỡng 0.60)' : 'Chưa tải mô hình',
                  isOnline: _healthStatus!.modelReady,
                  icon: Icons.memory,
                ),
                const SizedBox(height: 6),
                SystemStatusTile(
                  title: 'Cơ sở dữ liệu PostgreSQL',
                  statusText: _healthStatus!.databaseConnected
                      ? 'Đã kết nối (credit_app schema)'
                      : 'Mất kết nối (Chế độ Graceful)',
                  isOnline: _healthStatus!.databaseConnected,
                  icon: Icons.storage,
                ),
              ] else if (_errorMessage != null) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppTheme.riskHighBg,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: AppTheme.riskHigh.withValues(alpha: 0.3)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.cloud_off, color: AppTheme.riskHigh, size: 22),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Không thể kết nối máy chủ FastAPI',
                              style: TextStyle(
                                color: AppTheme.riskHigh,
                                fontWeight: FontWeight.w700,
                                fontSize: 13,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              _errorMessage!,
                              style: const TextStyle(color: AppTheme.bodyText, fontSize: 11.5),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ] else ...[
                const Center(
                  child: Padding(
                    padding: EdgeInsets.all(12),
                    child: Text(
                      'Đang kiểm tra kết nối tới máy chủ...',
                      style: TextStyle(color: AppTheme.bodyText, fontSize: 13),
                    ),
                  ),
                ),
              ],

              const SizedBox(height: 22),

              // 5. Academic Footer
              Center(
                child: Text(
                  'Khóa luận Tốt nghiệp Đại học — Ngành Công nghệ Thông tin\n'
                  'Trường ĐH Tài nguyên & Môi trường TP.HCM (HCMUNRE)\n'
                  'Giảng viên hướng dẫn: TS. Dương Thị Thúy Nga',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 11.5,
                    color: AppTheme.bodyText,
                    height: 1.45,
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMetricBox(String title, String value, IconData? icon) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
        decoration: BoxDecoration(
          color: AppTheme.backgroundLight,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: AppTheme.cardBorder, width: 0.8),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                if (icon != null) ...[
                  Icon(icon, size: 13, color: AppTheme.primaryGreen),
                  const SizedBox(width: 4),
                ],
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 10.5,
                      color: AppTheme.bodyText,
                      fontWeight: FontWeight.w500,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 3),
            Text(
              value,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w800,
                color: AppTheme.headingNavy,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}
