import 'package:flutter/material.dart';
import '../models/customer_input.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';
import '../widgets/banking_components.dart';
import 'prediction_result_screen.dart';

class CustomerInputFormScreen extends StatefulWidget {
  const CustomerInputFormScreen({super.key});

  @override
  State<CustomerInputFormScreen> createState() => _CustomerInputFormScreenState();
}

class _CustomerInputFormScreenState extends State<CustomerInputFormScreen> {
  final _formKey = GlobalKey<FormState>();

  // Bộ điều khiển cho các trường số học
  late TextEditingController _limitBalCtrl;
  late TextEditingController _ageCtrl;

  // Trường phân loại (Categorical)
  int _sex = 2; // 1: Nam, 2: Nữ
  int _education = 2; // 1: Sau ĐH, 2: ĐH, 3: THPT, 4: Khác
  int _marriage = 2; // 1: Đã kết hôn, 2: Độc thân, 3: Khác

  // Trạng thái thanh toán 6 tháng từ T9/2005 (PAY_0) đến T4/2005 (PAY_6)
  late List<int> _payStatus;

  // Dư nợ hóa đơn 6 tháng (BILL_AMT1 .. BILL_AMT6)
  late List<TextEditingController> _billCtrls;

  // Số tiền đã thanh toán 6 tháng (PAY_AMT1 .. PAY_AMT6)
  late List<TextEditingController> _payCtrls;

  bool _isSubmitting = false;

  // Tên tháng tương ứng từ T9/2005 đến T4/2005
  final List<String> _monthNames = const [
    'Tháng 9/2005 (Kỳ gần nhất)',
    'Tháng 8/2005',
    'Tháng 7/2005',
    'Tháng 6/2005',
    'Tháng 5/2005',
    'Tháng 4/2005 (Kỳ xa nhất)',
  ];

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

  void _applyPreset(CustomerInput preset, String presetName) {
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
      SnackBar(
        content: Text('Đã nạp hồ sơ mẫu: $presetName'),
        duration: const Duration(seconds: 2),
        backgroundColor: AppTheme.primaryGreen,
        behavior: SnackBarBehavior.floating,
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
    if (_isSubmitting) return;

    if (!_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Vui lòng kiểm tra và hoàn thiện các trường dữ liệu bắt buộc.'),
          backgroundColor: AppTheme.riskHigh,
          behavior: SnackBarBehavior.floating,
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
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            title: const Row(
              children: [
                Icon(Icons.error_outline, color: AppTheme.riskHigh, size: 24),
                SizedBox(width: 8),
                Text('Lỗi Thẩm Định', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ],
            ),
            content: Text(
              e.toString(),
              style: const TextStyle(fontSize: 13, height: 1.4),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('Đóng', style: TextStyle(color: AppTheme.primaryGreen, fontWeight: FontWeight.bold)),
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
              // Thanh chọn nhanh dữ liệu mẫu phong cách Ngân hàng
              _buildPresetsBar(),

              const SizedBox(height: 16),

              // Phân đoạn 1: Thông tin Định danh & Hạn mức
              const SectionTitle(
                title: '1. Thông tin Định danh & Hạn mức',
                subtitle: 'Hạn mức tín dụng được cấp và thông tin nhân khẩu học cơ bản',
                icon: Icons.badge_outlined,
              ),
              _buildDemographicsCard(),

              const SizedBox(height: 16),

              // Phân đoạn 2: Lịch sử Trạng thái Thanh toán (T9..T4)
              const SectionTitle(
                title: '2. Lịch sử Trạng thái Trả nợ (6 tháng)',
                subtitle: '-2: Không dùng, -1: Trả đủ, 0: Trả tối thiểu, 1-8: Chậm n tháng',
                icon: Icons.history,
              ),
              _buildPaymentStatusCard(),

              const SizedBox(height: 16),

              // Phân đoạn 3: Dư nợ Hóa đơn 6 tháng (NT$)
              const SectionTitle(
                title: '3. Dư nợ Sao kê Hóa đơn (NT\$)',
                subtitle: 'Số tiền nợ ghi nhận trong sao kê thẻ từ T9/2005 đến T4/2005',
                icon: Icons.receipt_long_outlined,
              ),
              _buildBillAmountsCard(),

              const SizedBox(height: 16),

              // Phân đoạn 4: Số tiền đã thanh toán 6 tháng (NT$)
              const SectionTitle(
                title: '4. Số tiền Khách hàng đã Thanh toán (NT\$)',
                subtitle: 'Số tiền thực tế khách hàng đã thanh toán trong kỳ sao kê trước',
                icon: Icons.price_check_outlined,
              ),
              _buildPaymentAmountsCard(),

              const SizedBox(height: 22),

              // Nút Submit Đánh giá Rủi ro phong cách Banking VCB
              ElevatedButton(
                onPressed: _isSubmitting ? null : _submitForm,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryGreen,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  elevation: 2,
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
                          Text('Đang thẩm định qua XGBoost Tuned...', style: TextStyle(fontSize: 15)),
                        ],
                      )
                    : const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.verified_outlined, color: Colors.white, size: 20),
                          SizedBox(width: 8),
                          Text(
                            'TIẾN HÀNH THẨM ĐỊNH RỦI RO',
                            style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, letterSpacing: 0.5),
                          ),
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
          style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: AppTheme.headingNavy),
        ),
        const SizedBox(height: 8),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(
            children: [
              ActionChip(
                avatar: const Icon(Icons.verified_user_outlined, size: 16, color: AppTheme.riskLow),
                backgroundColor: AppTheme.riskLowBg,
                label: const Text('Rủi ro thấp (<30%)', style: TextStyle(fontWeight: FontWeight.w700, color: AppTheme.riskLow, fontSize: 12)),
                onPressed: () => _applyPreset(CustomerInput.presetLowRisk(), 'Rủi ro Thấp (Low Risk)'),
              ),
              const SizedBox(width: 8),
              ActionChip(
                avatar: const Icon(Icons.person_outline, size: 16, color: AppTheme.primaryGreen),
                backgroundColor: AppTheme.primaryLight,
                label: const Text('Bình thường (~12%)', style: TextStyle(fontWeight: FontWeight.w700, color: AppTheme.primaryGreen, fontSize: 12)),
                onPressed: () => _applyPreset(CustomerInput.presetNormal(), 'Khách hàng Bình thường'),
              ),
              const SizedBox(width: 8),
              ActionChip(
                avatar: const Icon(Icons.warning_amber_rounded, size: 16, color: AppTheme.riskHigh),
                backgroundColor: AppTheme.riskHighBg,
                label: const Text('Rủi ro cao (>=60%)', style: TextStyle(fontWeight: FontWeight.w700, color: AppTheme.riskHigh, fontSize: 12)),
                onPressed: () => _applyPreset(CustomerInput.presetHighRisk(), 'Rủi ro Cao (High Risk)'),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildDemographicsCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextFormField(
              controller: _limitBalCtrl,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Hạn mức tín dụng được cấp (LIMIT_BAL) *',
                helperText: 'Đơn vị: NT\$ (Tân Đài tệ). Ví dụ: 200,000 NT\$',
                prefixIcon: Icon(Icons.credit_card, color: AppTheme.primaryGreen, size: 20),
              ),
              validator: (v) {
                if (v == null || v.trim().isEmpty) return 'Bắt buộc nhập hạn mức';
                final val = double.tryParse(v.trim());
                if (val == null || val <= 0) return 'Hạn mức phải là số dương lớn hơn 0';
                return null;
              },
            ),
            const SizedBox(height: 14),
            Row(
              children: [
                Expanded(
                  flex: 2,
                  child: TextFormField(
                    controller: _ageCtrl,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Độ tuổi (AGE) *',
                      helperText: 'Từ 18 đến 100 tuổi',
                      prefixIcon: Icon(Icons.cake_outlined, color: AppTheme.primaryGreen, size: 20),
                    ),
                    validator: (v) {
                      if (v == null || v.trim().isEmpty) return 'Nhập tuổi';
                      final val = int.tryParse(v.trim());
                      if (val == null || val < 18 || val > 100) return 'Từ 18-100';
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  flex: 3,
                  child: DropdownButtonFormField<int>(
                    initialValue: _sex,
                    decoration: const InputDecoration(
                      labelText: 'Giới tính (SEX)',
                      prefixIcon: Icon(Icons.people_outline, color: AppTheme.primaryGreen, size: 20),
                    ),
                    items: const [
                      DropdownMenuItem(value: 1, child: Text('Nam (1)')),
                      DropdownMenuItem(value: 2, child: Text('Nữ (2)')),
                    ],
                    onChanged: (val) {
                      if (val != null) setState(() => _sex = val);
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),
            DropdownButtonFormField<int>(
              initialValue: _education,
              decoration: const InputDecoration(
                labelText: 'Trình độ học vấn (EDUCATION)',
                prefixIcon: Icon(Icons.school_outlined, color: AppTheme.primaryGreen, size: 20),
              ),
              items: const [
                DropdownMenuItem(value: 1, child: Text('1 - Sau Đại học (Graduate)')),
                DropdownMenuItem(value: 2, child: Text('2 - Đại học (University)')),
                DropdownMenuItem(value: 3, child: Text('3 - Trung học phổ thông (High School)')),
                DropdownMenuItem(value: 4, child: Text('4 - Khác (Others)')),
              ],
              onChanged: (val) {
                if (val != null) setState(() => _education = val);
              },
            ),
            const SizedBox(height: 14),
            DropdownButtonFormField<int>(
              initialValue: _marriage,
              decoration: const InputDecoration(
                labelText: 'Tình trạng hôn nhân (MARRIAGE)',
                prefixIcon: Icon(Icons.favorite_outline, color: AppTheme.primaryGreen, size: 20),
              ),
              items: const [
                DropdownMenuItem(value: 1, child: Text('1 - Đã kết hôn (Married)')),
                DropdownMenuItem(value: 2, child: Text('2 - Độc thân (Single)')),
                DropdownMenuItem(value: 3, child: Text('3 - Khác (Others)')),
              ],
              onChanged: (val) {
                if (val != null) setState(() => _marriage = val);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPaymentStatusCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            for (int i = 0; i < 6; i++) ...[
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 5),
                child: Row(
                  children: [
                    Expanded(
                      flex: 4,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _monthNames[i],
                            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13, color: AppTheme.headingNavy),
                          ),
                          Text(
                            'Trường PAY_${i == 0 ? 0 : i + 1}',
                            style: const TextStyle(fontSize: 11, color: AppTheme.bodyText),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      flex: 4,
                      child: DropdownButtonFormField<int>(
                        initialValue: _payStatus[i],
                        isExpanded: true,
                        decoration: InputDecoration(
                          contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                        items: const [
                          DropdownMenuItem(value: -2, child: Text('-2: Không dùng')),
                          DropdownMenuItem(value: -1, child: Text('-1: Trả đủ')),
                          DropdownMenuItem(value: 0, child: Text('0: Trả tối thiểu')),
                          DropdownMenuItem(value: 1, child: Text('1: Chậm 1 tháng')),
                          DropdownMenuItem(value: 2, child: Text('2: Chậm 2 tháng')),
                          DropdownMenuItem(value: 3, child: Text('3: Chậm 3 tháng')),
                          DropdownMenuItem(value: 4, child: Text('4: Chậm 4 tháng')),
                          DropdownMenuItem(value: 5, child: Text('5: Chậm 5 tháng')),
                          DropdownMenuItem(value: 6, child: Text('6: Chậm 6 tháng')),
                          DropdownMenuItem(value: 7, child: Text('7: Chậm 7 tháng')),
                          DropdownMenuItem(value: 8, child: Text('8: Chậm >=8 tháng')),
                        ],
                        onChanged: (val) {
                          if (val != null) setState(() => _payStatus[i] = val);
                        },
                      ),
                    ),
                  ],
                ),
              ),
              if (i < 5) const Divider(height: 8, color: AppTheme.dividerColor),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildBillAmountsCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            for (int i = 0; i < 6; i++) ...[
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: TextFormField(
                  controller: _billCtrls[i],
                  keyboardType: const TextInputType.numberWithOptions(signed: true, decimal: true),
                  decoration: InputDecoration(
                    labelText: 'Dư nợ ${_monthNames[i]} (BILL_AMT${i + 1})',
                    suffixText: 'NT\$',
                    prefixIcon: const Icon(Icons.receipt, color: AppTheme.primaryGreen, size: 18),
                  ),
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Bắt buộc nhập số tiền';
                    if (double.tryParse(v.trim()) == null) return 'Phải là số hợp lệ';
                    return null;
                  },
                ),
              ),
              if (i < 5) const SizedBox(height: 6),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildPaymentAmountsCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            for (int i = 0; i < 6; i++) ...[
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: TextFormField(
                  controller: _payCtrls[i],
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: InputDecoration(
                    labelText: 'Thanh toán ${_monthNames[i]} (PAY_AMT${i + 1})',
                    suffixText: 'NT\$',
                    prefixIcon: const Icon(Icons.payments_outlined, color: AppTheme.primaryGreen, size: 18),
                  ),
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Bắt buộc nhập số tiền';
                    final val = double.tryParse(v.trim());
                    if (val == null || val < 0) return 'Số tiền thanh toán phải >= 0';
                    return null;
                  },
                ),
              ),
              if (i < 5) const SizedBox(height: 6),
            ],
          ],
        ),
      ),
    );
  }
}
