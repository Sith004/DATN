import 'package:flutter/material.dart';
import '../models/health_status.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';
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
            icon: const Icon(Icons.settings),
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
        onRefresh: _checkServerStatus,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 1. Academic Header Banner
              _buildAcademicHeader(),

              const SizedBox(height: 14),

              // 2. Server & Database Live Health Card
              _buildConnectionStatusCard(),

              const SizedBox(height: 14),

              // 3. Model Verified Metrics Card
              _buildModelMetricsCard(),

              const SizedBox(height: 18),

              // 4. Primary Actions
              _buildActionCard(
                title: 'Dự báo Rủi ro Khách hàng',
                subtitle: 'Nhập 23 thuộc tính để tính xác suất vỡ nợ qua mô hình XGBoost',
                icon: Icons.analytics_outlined,
                color: AppTheme.accentCyan,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const CustomerInputFormScreen(),
                    ),
                  );
                },
              ),

              const SizedBox(height: 12),

              _buildActionCard(
                title: 'Lịch sử Dự báo (PostgreSQL)',
                subtitle: 'Xem các hồ sơ dự báo được lưu trữ an toàn trong cơ sở dữ liệu',
                icon: Icons.history,
                color: AppTheme.primaryNavy,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const PredictionHistoryScreen(),
                    ),
                  );
                },
              ),

              const SizedBox(height: 20),

              // 5. Academic Disclaimer Footer
              Center(
                child: Text(
                  'Hệ thống thử nghiệm phục vụ Đồ án Tốt nghiệp Đại học\n'
                  'Khoa CNTT — Trường ĐH Tài nguyên & Môi trường TP.HCM',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade600,
                    height: 1.4,
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

  Widget _buildAcademicHeader() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppTheme.primaryNavy, Color(0xFF2D6A9F)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryNavy.withValues(alpha: 0.25),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.15),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.school, color: Colors.white, size: 24),
              ),
              const SizedBox(width: 12),
              const Expanded(
                child: Text(
                  'KHÓA LUẬN TỐT NGHIỆP',
                  style: TextStyle(
                    color: Colors.white70,
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 1.0,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          const Text(
            'ỨNG DỤNG MACHINE LEARNING TRONG DỰ BÁO RỦI RO TÍN DỤNG',
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold,
              height: 1.3,
            ),
          ),
          const Divider(color: Colors.white24, height: 20),
          Row(
            children: [
              const Icon(Icons.person, color: Colors.white70, size: 16),
              const SizedBox(width: 6),
              const Text(
                'Sinh viên: Nguyễn Trọng Thể',
                style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w500),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.2),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Text(
                  'MSSV: 1150080117',
                  style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildConnectionStatusCard() {
    bool isConnected = _healthStatus?.isHealthy ?? false;
    Color statusColor = isConnected ? AppTheme.riskLow : AppTheme.riskHigh;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  isConnected ? Icons.cloud_done : Icons.cloud_off,
                  color: statusColor,
                  size: 22,
                ),
                const SizedBox(width: 10),
                const Text(
                  'Trạng thái Hệ thống Backend',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                if (_isLoadingHealth)
                  const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                else
                  IconButton(
                    icon: const Icon(Icons.refresh, size: 20),
                    onPressed: _checkServerStatus,
                    tooltip: 'Kiểm tra lại',
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            if (_healthStatus != null) ...[
              _buildStatusRow(
                'FastAPI Server',
                'Hoạt động (v${_healthStatus!.apiVersion})',
                AppTheme.riskLow,
              ),
              const SizedBox(height: 6),
              _buildStatusRow(
                'Mô hình XGBoost',
                _healthStatus!.modelReady ? 'Đã tải thành công' : 'Chưa tải',
                _healthStatus!.modelReady ? AppTheme.riskLow : AppTheme.riskHigh,
              ),
              const SizedBox(height: 6),
              _buildStatusRow(
                'Cơ sở dữ liệu PostgreSQL',
                _healthStatus!.databaseConnected ? 'Đã kết nối an toàn (Port 15432)' : 'Mất kết nối',
                _healthStatus!.databaseConnected ? AppTheme.riskLow : AppTheme.riskMedium,
              ),
            ] else if (_errorMessage != null) ...[
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppTheme.riskHighBg,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.warning, color: AppTheme.riskHigh, size: 20),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        _errorMessage!,
                        style: const TextStyle(color: AppTheme.riskHigh, fontSize: 13),
                      ),
                    ),
                  ],
                ),
              ),
            ] else ...[
              const Text('Đang kiểm tra kết nối...', style: TextStyle(color: Colors.grey)),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStatusRow(String label, String value, Color color) {
    return Row(
      children: [
        Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 8),
        Text(label, style: const TextStyle(fontSize: 13, color: Color(0xFF64748B))),
        const Spacer(),
        Text(
          value,
          style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: color),
        ),
      ],
    );
  }

  Widget _buildModelMetricsCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.verified, color: AppTheme.primaryNavy, size: 20),
                SizedBox(width: 8),
                Text(
                  'Thông số Mô hình Tuyển chọn (Week 8)',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                _buildMetricBox('Mô hình', 'XGBoost Tuned'),
                const SizedBox(width: 8),
                _buildMetricBox('Ngưỡng (Threshold)', '0.60'),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                _buildMetricBox('ROC-AUC', '0.7769'),
                const SizedBox(width: 8),
                _buildMetricBox('PR-AUC', '0.5620'),
                const SizedBox(width: 8),
                _buildMetricBox('F1-Score', '0.5409'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricBox(String title, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
        decoration: BoxDecoration(
          color: const Color(0xFFF1F5F9),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Column(
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 11, color: Color(0xFF64748B)),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 4),
            Text(
              value,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
                color: AppTheme.primaryNavy,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard({
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(14),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: const TextStyle(fontSize: 13, color: Color(0xFF64748B)),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 16, color: Color(0xFF94A3B8)),
            ],
          ),
        ),
      ),
    );
  }
}
