import 'package:flutter/material.dart';
import '../config/api_config.dart';
import '../models/health_status.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';

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

    // Save temporarily for test
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
          backgroundColor: AppTheme.riskLow,
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
        title: const Text('CÀI ĐẶT MÁY CHỦ API'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Instructions Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.wifi, color: AppTheme.primaryNavy, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Kết nối Thiết bị Thật qua Mạng LAN Wi-Fi',
                          style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Để điện thoại Android thực tế có thể gọi được API, điện thoại và máy tính cần kết nối chung một mạng Wi-Fi. '
                      'Nhập địa chỉ IP Wi-Fi của máy tính đang chạy FastAPI kèm cổng 8000.',
                      style: TextStyle(fontSize: 12, color: Colors.grey.shade700, height: 1.4),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Base URL Input
            TextFormField(
              controller: _urlController,
              decoration: const InputDecoration(
                labelText: 'FastAPI Base URL',
                hintText: 'http://192.168.100.11:8000',
                prefixIcon: Icon(Icons.link),
              ),
              keyboardType: TextInputType.url,
            ),

            const SizedBox(height: 12),

            // Quick Presets
            const Text(
              'Chọn nhanh địa chỉ mẫu:',
              style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF64748B)),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                ActionChip(
                  avatar: const Icon(Icons.wifi, size: 16),
                  label: const Text('Wi-Fi LAN (192.168.100.11:8000)'),
                  onPressed: () => _applyPreset(ApiConfig.defaultBaseUrl),
                ),
                ActionChip(
                  avatar: const Icon(Icons.phone_android, size: 16),
                  label: const Text('Máy ảo Android (10.0.2.2:8000)'),
                  onPressed: () => _applyPreset(ApiConfig.emulatorBaseUrl),
                ),
                ActionChip(
                  avatar: const Icon(Icons.computer, size: 16),
                  label: const Text('Localhost (127.0.0.1:8000)'),
                  onPressed: () => _applyPreset(ApiConfig.localhostBaseUrl),
                ),
              ],
            ),

            const SizedBox(height: 16),

            // Test Connection Button
            OutlinedButton.icon(
              icon: _isTesting
                  ? const SizedBox(
                      width: 16,
                      height: 16,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.network_check),
              label: Text(_isTesting ? 'Đang kiểm tra...' : 'Kiểm tra kết nối (Ping /health)'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              onPressed: _isTesting ? null : _testConnection,
            ),

            const SizedBox(height: 14),

            // Test Result Box
            if (_testResult != null) ...[
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: AppTheme.riskLowBg,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppTheme.riskLow),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.check_circle, color: AppTheme.riskLow, size: 20),
                        const SizedBox(width: 8),
                        const Text(
                          'Kết nối thành công!',
                          style: TextStyle(color: AppTheme.riskLow, fontWeight: FontWeight.bold),
                        ),
                        const Spacer(),
                        if (_latencyMs != null)
                          Text(
                            'Ping: ${_latencyMs}ms',
                            style: const TextStyle(color: AppTheme.riskLow, fontSize: 12),
                          ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text('• Mô hình: ${_testResult!.modelName} (Ngưỡng: ${_testResult!.threshold})',
                        style: const TextStyle(fontSize: 12)),
                    Text('• Trạng thái CSDL: ${_testResult!.databaseStatusMessage}',
                        style: const TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ] else if (_testError != null) ...[
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: AppTheme.riskHighBg,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppTheme.riskHigh),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.error_outline, color: AppTheme.riskHigh, size: 22),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        _testError!,
                        style: const TextStyle(color: AppTheme.riskHigh, fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
            ],

            const SizedBox(height: 24),

            // Save and Exit Button
            ElevatedButton(
              onPressed: _saveAndExit,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: AppTheme.primaryNavy,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              child: const Text('LƯU VÀ QUAY LẠI', style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}
