import 'package:flutter/material.dart';
import '../models/customer_input.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';
import 'prediction_result_screen.dart';

class CustomerInputFormScreen extends StatefulWidget {
  const CustomerInputFormScreen({super.key});

  @override
  State<CustomerInputFormScreen> createState() => _CustomerInputFormScreenState();
}

class _CustomerInputFormScreenState extends State<CustomerInputFormScreen> {
  final _formKey = GlobalKey<FormState>();

  // Text controllers for numerical fields
  late TextEditingController _limitBalCtrl;
  late TextEditingController _ageCtrl;

  // Categorical fields
  int _sex = 2; // 1: Nam, 2: Nữ
  int _education = 2; // 1: Sau ĐH, 2: ĐH, 3: THPT, 4: Khác
  int _marriage = 2; // 1: Đã kết hôn, 2: Độc thân, 3: Khác

  // Repayment status 6 months (-2..8)
  late List<int> _payStatus;

  // Bill amounts 6 months
  late List<TextEditingController> _billCtrls;

  // Payment amounts 6 months
  late List<TextEditingController> _payCtrls;

  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _initControllersWithPreset(CustomerInput.presetNormal());
  }

  void _initControllersWithPreset(CustomerInput preset) {
    _limitBalCtrl = TextEditingController(text: preset.limitBal.toInt().toString());
    _ageCtrl = TextEditingController(text: preset.age.toString());
    _sex = preset.sex;
    _education = preset.education;
    _marriage = preset.marriage;

    _payStatus = [
      preset.pay0,
      preset.pay2,
      preset.pay3,
      preset.pay4,
      preset.pay5,
      preset.pay6,
    ];

    _billCtrls = [
      TextEditingController(text: preset.billAmt1.toInt().toString()),
      TextEditingController(text: preset.billAmt2.toInt().toString()),
      TextEditingController(text: preset.billAmt3.toInt().toString()),
      TextEditingController(text: preset.billAmt4.toInt().toString()),
      TextEditingController(text: preset.billAmt5.toInt().toString()),
      TextEditingController(text: preset.billAmt6.toInt().toString()),
    ];

    _payCtrls = [
      TextEditingController(text: preset.payAmt1.toInt().toString()),
      TextEditingController(text: preset.payAmt2.toInt().toString()),
      TextEditingController(text: preset.payAmt3.toInt().toString()),
      TextEditingController(text: preset.payAmt4.toInt().toString()),
      TextEditingController(text: preset.payAmt5.toInt().toString()),
      TextEditingController(text: preset.payAmt6.toInt().toString()),
    ];
  }

  void _applyPreset(CustomerInput preset) {
    setState(() {
      _limitBalCtrl.text = preset.limitBal.toInt().toString();
      _ageCtrl.text = preset.age.toString();
      _sex = preset.sex;
      _education = preset.education;
      _marriage = preset.marriage;

      _payStatus = [
        preset.pay0,
        preset.pay2,
        preset.pay3,
        preset.pay4,
        preset.pay5,
        preset.pay6,
      ];

      _billCtrls[0].text = preset.billAmt1.toInt().toString();
      _billCtrls[1].text = preset.billAmt2.toInt().toString();
      _billCtrls[2].text = preset.billAmt3.toInt().toString();
      _billCtrls[3].text = preset.billAmt4.toInt().toString();
      _billCtrls[4].text = preset.billAmt5.toInt().toString();
      _billCtrls[5].text = preset.billAmt6.toInt().toString();

      _payCtrls[0].text = preset.payAmt1.toInt().toString();
      _payCtrls[1].text = preset.payAmt2.toInt().toString();
      _payCtrls[2].text = preset.payAmt3.toInt().toString();
      _payCtrls[3].text = preset.payAmt4.toInt().toString();
      _payCtrls[4].text = preset.payAmt5.toInt().toString();
      _payCtrls[5].text = preset.payAmt6.toInt().toString();
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Đã nạp bộ dữ liệu mẫu thành công.'),
        duration: Duration(seconds: 1),
      ),
    );
  }

  @override
  void dispose() {
    _limitBalCtrl.dispose();
    _ageCtrl.dispose();
    for (var c in _billCtrls) {
      c.dispose();
    }
    for (var c in _payCtrls) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _submitForm() async {
    if (_isSubmitting) return; // Prevent duplicate submission

    if (!_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Vui lòng kiểm tra và sửa các trường dữ liệu chưa hợp lệ.'),
          backgroundColor: AppTheme.riskHigh,
        ),
      );
      return;
    }

    setState(() {
      _isSubmitting = true;
    });

    try {
      final input = CustomerInput(
        limitBal: double.parse(_limitBalCtrl.text.trim()),
        age: int.parse(_ageCtrl.text.trim()),
        sex: _sex,
        education: _education,
        marriage: _marriage,
        pay0: _payStatus[0],
        pay2: _payStatus[1],
        pay3: _payStatus[2],
        pay4: _payStatus[3],
        pay5: _payStatus[4],
        pay6: _payStatus[5],
        billAmt1: double.parse(_billCtrls[0].text.trim()),
        billAmt2: double.parse(_billCtrls[1].text.trim()),
        billAmt3: double.parse(_billCtrls[2].text.trim()),
        billAmt4: double.parse(_billCtrls[3].text.trim()),
        billAmt5: double.parse(_billCtrls[4].text.trim()),
        billAmt6: double.parse(_billCtrls[5].text.trim()),
        payAmt1: double.parse(_payCtrls[0].text.trim()),
        payAmt2: double.parse(_payCtrls[1].text.trim()),
        payAmt3: double.parse(_payCtrls[2].text.trim()),
        payAmt4: double.parse(_payCtrls[3].text.trim()),
        payAmt5: double.parse(_payCtrls[4].text.trim()),
        payAmt6: double.parse(_payCtrls[5].text.trim()),
      );

      final result = await ApiService.predict(input);

      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => PredictionResultScreen(result: result, input: input),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });

        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            title: const Row(
              children: [
                Icon(Icons.error_outline, color: AppTheme.riskHigh),
                SizedBox(width: 8),
                Text('Lỗi Dự Báo'),
              ],
            ),
            content: Text(e.toString()),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('Đóng'),
              ),
            ],
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('HỒ SƠ KHÁCH HÀNG (23 BIẾN)'),
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Presets bar
              _buildPresetsBar(),

              const SizedBox(height: 14),

              // Section 1: Thông tin nhân khẩu & Hạn mức
              _buildSectionHeader('1. Thông tin Định danh & Hạn mức', Icons.person_outline),
              _buildDemographicsCard(),

              const SizedBox(height: 14),

              // Section 2: Lịch sử thanh toán (PAY_0 .. PAY_6)
              _buildSectionHeader('2. Lịch sử Trạng thái Thanh toán (T9..T4)', Icons.payment),
              _buildPaymentStatusCard(),

              const SizedBox(height: 14),

              // Section 3: Dư nợ hóa đơn (BILL_AMT1 .. BILL_AMT6)
              _buildSectionHeader(r'3. Dư nợ Hóa đơn 6 tháng (NT$)', Icons.receipt_long),
              _buildBillAmountsCard(),

              const SizedBox(height: 14),

              // Section 4: Số tiền đã thanh toán (PAY_AMT1 .. PAY_AMT6)
              _buildSectionHeader(r'4. Số tiền đã Thanh toán 6 tháng (NT$)', Icons.price_check),
              _buildPaymentAmountsCard(),

              const SizedBox(height: 20),

              // Submit Button
              ElevatedButton(
                onPressed: _isSubmitting ? null : _submitForm,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryNavy,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: _isSubmitting
                    ? const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                          ),
                          SizedBox(width: 12),
                          Text('Đang phân tích Machine Learning...', style: TextStyle(fontSize: 16)),
                        ],
                      )
                    : const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.bolt, color: Colors.amberAccent),
                          SizedBox(width: 8),
                          Text('TIẾN HÀNH DỰ BÁO RỦI RO', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                        ],
                      ),
              ),

              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPresetsBar() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Dữ liệu mẫu thử nghiệm (Quick Presets):',
          style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 8),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(
            children: [
              ActionChip(
                avatar: const Icon(Icons.person, size: 16, color: AppTheme.accentCyan),
                label: const Text('Bình thường (Low Risk)'),
                onPressed: () => _applyPreset(CustomerInput.presetNormal()),
              ),
              const SizedBox(width: 8),
              ActionChip(
                avatar: const Icon(Icons.warning_amber, size: 16, color: AppTheme.riskHigh),
                label: const Text('Rủi ro cao (High Risk)'),
                onPressed: () => _applyPreset(CustomerInput.presetHighRisk()),
              ),
              const SizedBox(width: 8),
              ActionChip(
                avatar: const Icon(Icons.shield_outlined, size: 16, color: AppTheme.riskLow),
                label: const Text('Rất an toàn (Low Risk)'),
                onPressed: () => _applyPreset(CustomerInput.presetLowRisk()),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 18, color: AppTheme.secondaryBlue),
        const SizedBox(width: 6),
        Text(
          title,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: AppTheme.primaryNavy,
          ),
        ),
      ],
    );
  }

  Widget _buildDemographicsCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  flex: 3,
                  child: TextFormField(
                    controller: _limitBalCtrl,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Hạn mức (LIMIT_BAL)',
                      suffixText: 'NT\$',
                    ),
                    validator: (v) {
                      if (v == null || v.isEmpty) return 'Bắt buộc';
                      final val = double.tryParse(v);
                      if (val == null || val <= 0) return '> 0';
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  flex: 2,
                  child: TextFormField(
                    controller: _ageCtrl,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Tuổi (AGE)',
                      suffixText: 'tuổi',
                    ),
                    validator: (v) {
                      if (v == null || v.isEmpty) return 'Bắt buộc';
                      final val = int.tryParse(v);
                      if (val == null || val < 18 || val > 100) return '18-100';
                      return null;
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<int>(
                    value: _sex,
                    decoration: const InputDecoration(labelText: 'Giới tính (SEX)'),
                    items: const [
                      DropdownMenuItem(value: 1, child: Text('1 - Nam')),
                      DropdownMenuItem(value: 2, child: Text('2 - Nữ')),
                    ],
                    onChanged: (v) => setState(() => _sex = v!),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: DropdownButtonFormField<int>(
                    value: _marriage,
                    decoration: const InputDecoration(labelText: 'Hôn nhân (MARRIAGE)'),
                    items: const [
                      DropdownMenuItem(value: 1, child: Text('1 - Đã kết hôn')),
                      DropdownMenuItem(value: 2, child: Text('2 - Độc thân')),
                      DropdownMenuItem(value: 3, child: Text('3 - Khác')),
                    ],
                    onChanged: (v) => setState(() => _marriage = v!),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<int>(
              value: _education,
              decoration: const InputDecoration(labelText: 'Học vấn (EDUCATION)'),
              items: const [
                DropdownMenuItem(value: 1, child: Text('1 - Sau đại học (Master / Ph.D)')),
                DropdownMenuItem(value: 2, child: Text('2 - Đại học (University)')),
                DropdownMenuItem(value: 3, child: Text('3 - Trung học phổ thông (High School)')),
                DropdownMenuItem(value: 4, child: Text('4 - Khác (Others)')),
              ],
              onChanged: (v) => setState(() => _education = v!),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPaymentStatusCard() {
    final months = ['T9 (PAY_0)', 'T8 (PAY_2)', 'T7 (PAY_3)', 'T6 (PAY_4)', 'T5 (PAY_5)', 'T4 (PAY_6)'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Chú giải: -1: Đúng hạn, 0: Đã trả tối thiểu, 1..8: Trễ 1..8 tháng',
              style: TextStyle(fontSize: 12, color: Color(0xFF64748B)),
            ),
            const SizedBox(height: 10),
            for (int i = 0; i < 6; i++) ...[
              Row(
                children: [
                  Expanded(
                    flex: 3,
                    child: Text(
                      months[i],
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                    ),
                  ),
                  Expanded(
                    flex: 4,
                    child: DropdownButtonFormField<int>(
                      value: _payStatus[i],
                      isDense: true,
                      decoration: InputDecoration(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      items: const [
                        DropdownMenuItem(value: -2, child: Text('-2: Không dùng')),
                        DropdownMenuItem(value: -1, child: Text('-1: Đúng hạn')),
                        DropdownMenuItem(value: 0, child: Text(' 0: Dùng thẻ')),
                        DropdownMenuItem(value: 1, child: Text(' 1: Trễ 1 tháng')),
                        DropdownMenuItem(value: 2, child: Text(' 2: Trễ 2 tháng')),
                        DropdownMenuItem(value: 3, child: Text(' 3: Trễ 3 tháng')),
                        DropdownMenuItem(value: 4, child: Text(' 4: Trễ 4 tháng')),
                        DropdownMenuItem(value: 5, child: Text(' 5: Trễ 5 tháng')),
                        DropdownMenuItem(value: 6, child: Text(' 6: Trễ 6 tháng')),
                        DropdownMenuItem(value: 7, child: Text(' 7: Trễ 7 tháng')),
                        DropdownMenuItem(value: 8, child: Text(' 8: Trễ 8 tháng')),
                      ],
                      onChanged: (v) => setState(() => _payStatus[i] = v!),
                    ),
                  ),
                ],
              ),
              if (i < 5) const SizedBox(height: 8),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildBillAmountsCard() {
    final labels = ['T9 (BILL_AMT1)', 'T8 (BILL_AMT2)', 'T7 (BILL_AMT3)', 'T6 (BILL_AMT4)', 'T5 (BILL_AMT5)', 'T4 (BILL_AMT6)'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            for (int i = 0; i < 6; i += 2) ...[
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _billCtrls[i],
                      keyboardType: const TextInputType.numberWithOptions(signed: true),
                      decoration: InputDecoration(
                        labelText: labels[i],
                        suffixText: 'NT\$',
                        isDense: true,
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Bắt buộc';
                        if (double.tryParse(v) == null) return 'Phải là số';
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: _billCtrls[i + 1],
                      keyboardType: const TextInputType.numberWithOptions(signed: true),
                      decoration: InputDecoration(
                        labelText: labels[i + 1],
                        suffixText: 'NT\$',
                        isDense: true,
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Bắt buộc';
                        if (double.tryParse(v) == null) return 'Phải là số';
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              if (i < 4) const SizedBox(height: 10),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildPaymentAmountsCard() {
    final labels = ['T9 (PAY_AMT1)', 'T8 (PAY_AMT2)', 'T7 (PAY_AMT3)', 'T6 (PAY_AMT4)', 'T5 (PAY_AMT5)', 'T4 (PAY_AMT6)'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            for (int i = 0; i < 6; i += 2) ...[
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _payCtrls[i],
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: labels[i],
                        suffixText: 'NT\$',
                        isDense: true,
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Bắt buộc';
                        final val = double.tryParse(v);
                        if (val == null || val < 0) return '>= 0';
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: _payCtrls[i + 1],
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: labels[i + 1],
                        suffixText: 'NT\$',
                        isDense: true,
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Bắt buộc';
                        final val = double.tryParse(v);
                        if (val == null || val < 0) return '>= 0';
                        return null;
                      },
                    ),
                  ),
                ],
              ),
              if (i < 4) const SizedBox(height: 10),
            ],
          ],
        ),
      ),
    );
  }
}
