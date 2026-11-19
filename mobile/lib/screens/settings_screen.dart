import 'package:flutter/material.dart';
import '../config/api_config.dart';
import '../models/health_status.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';
import '../widgets/banking_components.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final TextEditingController _urlController = TextEditingController();
  bool _isTesting = false;
  HealthStatus? _testResult;
  String? _testError;
  int? _latencyMs;

  @override
  void initState() {
    super.initState();
    _loadCurrentUrl();
  }

  Future<void> _loadCurrentUrl() async {
    final currentUrl = await ApiConfig.getBaseUrl();
    setState(() {
      _urlController.text = currentUrl;
    });
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _testConnection() async {
    final newUrl = _urlController.text.trim();
    if (newUrl.isEmpty) return;

    // Lưu tạm thời để test
    await ApiConfig.setBaseUrl(newUrl);

    setState(() {
      _isTesting = true;
      _testResult = null;
      _testError = null;
      _latencyMs = null;
    });

    final stopwatch = Stopwatch()..start();
    try {
      final status = await ApiService.checkHealth();
      stopwatch.stop();

      if (mounted) {
        setState(() {
          _testResult = status;
          _latencyMs = stopwatch.elapsedMilliseconds;
          _isTesting = false;
        });
      }
    } catch (e) {
      stopwatch.stop();
      if (mounted) {
        setState(() {
          _testError = e.toString();
          _isTesting = false;
        });
      }
    }
  }

  Future<void> _saveAndExit() async {
    final newUrl = _urlController.text.trim();
    if (newUrl.isNotEmpty) {
      await ApiConfig.setBaseUrl(newUrl);
    }
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Đã lưu cấu hình máy chủ: $newUrl'),
          backgroundColor: AppTheme.primaryGreen,
          behavior: SnackBarBehavior.floating,
        ),
      );
      Navigator.pop(context);
    }
  }

  void _applyPreset(String url) {
    setState(() {
      _urlController.text = url;
      _testResult = null;
      _testError = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CÀI ĐẶT HẠ TẦNG KẾT NỐI'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. Phân đoạn Cấu hình Máy chủ
            const SectionTitle(
              title: '1. Địa chỉ Máy chủ FastAPI Backend',
              subtitle: 'Đường dẫn Base URL để Mobile App gửi yêu cầu suy luận và đồng bộ CSDL',
              icon: Icons.link,
            ),
            const SizedBox(height: 4),

            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    TextField(
                      controller: _urlController,
                      decoration: const InputDecoration(
                        labelText: 'API Base URL *',
                        hintText: 'http://192.168.100.11:8000',
                        prefixIcon: Icon(Icons.dns_outlined, color: AppTheme.primaryGreen, size: 20),
                        helperText: 'Không bao gồm dấu gạch chéo cuối (/api...)',
                      ),
                    ),
                    const SizedBox(height: 12),

                    const Text(
                      'Địa chỉ gợi ý (Quick Presets):',
                      style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppTheme.headingNavy),
                    ),
                    const SizedBox(height: 6),

                    Wrap(
                      spacing: 8,
                      runSpacing: 6,
                      children: [
                        ActionChip(
                          avatar: const Icon(Icons.wifi, size: 14, color: AppTheme.primaryGreen),
                          label: const Text('Wi-Fi Host (192.168.100.11)', style: TextStyle(fontSize: 11.5)),
                          onPressed: () => _applyPreset(ApiConfig.defaultBaseUrl),
                        ),
                        ActionChip(
                          avatar: const Icon(Icons.phone_android, size: 14, color: AppTheme.headingNavy),
                          label: const Text('Android Emulator (10.0.2.2)', style: TextStyle(fontSize: 11.5)),
                          onPressed: () => _applyPreset(ApiConfig.emulatorBaseUrl),
                        ),
                        ActionChip(
                          avatar: const Icon(Icons.laptop, size: 14, color: AppTheme.bodyText),
                          label: const Text('Localhost (127.0.0.1)', style: TextStyle(fontSize: 11.5)),
                          onPressed: () => _applyPreset(ApiConfig.localhostBaseUrl),
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),

                    // Nút kiểm tra Ping trực tiếp
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        icon: _isTesting
                            ? const SizedBox(
                                width: 16,
                                height: 16,
                                child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.primaryGreen),
                              )
                            : const Icon(Icons.network_ping, size: 18),
                        label: Text(_isTesting ? 'Đang gửi gói tin Ping...' : 'Kiểm tra Kết nối Trực tiếp'),
                        onPressed: _isTesting ? null : _testConnection,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 14),

            // 2. Kết quả Kiểm tra Ping Live
            if (_testResult != null) ...[
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: AppTheme.riskLowBg,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppTheme.riskLow.withValues(alpha: 0.4)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.check_circle, color: AppTheme.riskLow, size: 20),
                        const SizedBox(width: 8),
                        const Text(
                          'Kết nối Thành công',
                          style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.riskLow, fontSize: 14),
                        ),
                        const Spacer(),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(6),
                          ),
                          child: Text(
                            '${_latencyMs}ms',
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11.5, color: AppTheme.riskLow),
                          ),
                        ),
                      ],
                    ),
                    const Divider(height: 14, color: Colors.black12),
                    Text('• Phiên bản API: ${_testResult!.apiVersion}', style: const TextStyle(fontSize: 12)),
                    Text('• Mô hình XGBoost: ${_testResult!.modelReady ? "Sẵn sàng (Ngưỡng 0.60)" : "Chưa tải"}', style: const TextStyle(fontSize: 12)),
                    Text('• CSDL PostgreSQL: ${_testResult!.databaseConnected ? "Đã kết nối (Port 15432)" : "Chế độ Graceful"}', style: const TextStyle(fontSize: 12)),
                  ],
                ),
              ),
              const SizedBox(height: 14),
            ] else if (_testError != null) ...[
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: AppTheme.riskHighBg,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppTheme.riskHigh.withValues(alpha: 0.3)),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.error_outline, color: AppTheme.riskHigh, size: 22),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Kết nối Thất bại',
                            style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.riskHigh, fontSize: 14),
                          ),
                          const SizedBox(height: 4),
                          Text(_testError!, style: const TextStyle(fontSize: 12, color: AppTheme.bodyText)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),
            ],

            // 3. Thông tin Đồ án & Bản quyền
            const SectionTitle(
              title: '2. Thông tin Bản quyền & Đồ án',
              subtitle: 'Đồ án Tốt nghiệp Đại học Khóa 2022 - 2026',
              icon: Icons.info_outline,
            ),
            const SizedBox(height: 4),

            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    _buildInfoRow('Đề tài', 'Đánh giá Rủi ro Tín dụng (Credit Risk ML)'),
                    const Divider(height: 16, color: AppTheme.dividerColor),
                    _buildInfoRow('Sinh viên', 'Nguyễn Trọng Thể'),
                    const Divider(height: 16, color: AppTheme.dividerColor),
                    _buildInfoRow('MSSV', '1150080117'),
                    const Divider(height: 16, color: AppTheme.dividerColor),
                    _buildInfoRow('Khoa / Trường', 'Khoa CNTT — ĐH Tài nguyên & Môi trường TP.HCM'),
                    const Divider(height: 16, color: AppTheme.dividerColor),
                    _buildInfoRow('GVHD', 'TS. Dương Thị Thúy Nga'),
                    const Divider(height: 16, color: AppTheme.dividerColor),
                    _buildInfoRow('Phiên bản Mobile', 'v1.0.0+1 (VCB-Inspired Modern Banking)'),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Nút Lưu cấu hình
            ElevatedButton.icon(
              icon: const Icon(Icons.save, size: 18),
              label: const Text('LƯU VÀ ÁP DỤNG CẤU HÌNH'),
              onPressed: _saveAndExit,
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 110,
          child: Text(
            label,
            style: const TextStyle(fontSize: 12.5, color: AppTheme.bodyText, fontWeight: FontWeight.w500),
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: AppTheme.headingNavy),
          ),
        ),
      ],
    );
  }
}
