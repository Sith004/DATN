class CustomerInput {
  double limitBal;
  int age;
  int sex; // 1: Nam, 2: Nữ
  int education; // 1: Sau ĐH, 2: ĐH, 3: THPT, 4: Khác
  int marriage; // 1: Đã kết hôn, 2: Độc thân, 3: Khác

  // Trạng thái thanh toán 6 tháng
  int pay0;
  int pay2;
  int pay3;
  int pay4;
  int pay5;
  int pay6;

  // Hóa đơn 6 tháng
  double billAmt1;
  double billAmt2;
  double billAmt3;
  double billAmt4;
  double billAmt5;
  double billAmt6;

  // Số tiền thanh toán 6 tháng
  double payAmt1;
  double payAmt2;
  double payAmt3;
  double payAmt4;
  double payAmt5;
  double payAmt6;

  CustomerInput({
    required this.limitBal,
    required this.age,
    required this.sex,
    required this.education,
    required this.marriage,
    required this.pay0,
    required this.pay2,
    required this.pay3,
    required this.pay4,
    required this.pay5,
    required this.pay6,
    required this.billAmt1,
    required this.billAmt2,
    required this.billAmt3,
    required this.billAmt4,
    required this.billAmt5,
    required this.billAmt6,
    required this.payAmt1,
    required this.payAmt2,
    required this.payAmt3,
    required this.payAmt4,
    required this.payAmt5,
    required this.payAmt6,
  });

  Map<String, dynamic> toJson() {
    return {
      'LIMIT_BAL': limitBal,
      'AGE': age,
      'SEX': sex,
      'EDUCATION': education,
      'MARRIAGE': marriage,
      'PAY_0': pay0,
      'PAY_2': pay2,
      'PAY_3': pay3,
      'PAY_4': pay4,
      'PAY_5': pay5,
      'PAY_6': pay6,
      'BILL_AMT1': billAmt1,
      'BILL_AMT2': billAmt2,
      'BILL_AMT3': billAmt3,
      'BILL_AMT4': billAmt4,
      'BILL_AMT5': billAmt5,
      'BILL_AMT6': billAmt6,
      'PAY_AMT1': payAmt1,
      'PAY_AMT2': payAmt2,
      'PAY_AMT3': payAmt3,
      'PAY_AMT4': payAmt4,
      'PAY_AMT5': payAmt5,
      'PAY_AMT6': payAmt6,
    };
  }

  // Preset 1: Khách hàng bình thường (Normal)
  factory CustomerInput.presetNormal() {
    return CustomerInput(
      limitBal: 200000.0,
      age: 35,
      sex: 2,
      education: 2,
      marriage: 2,
      pay0: 0,
      pay2: 0,
      pay3: 0,
      pay4: 0,
      pay5: 0,
      pay6: 0,
      billAmt1: 25000.0,
      billAmt2: 22000.0,
      billAmt3: 20000.0,
      billAmt4: 18000.0,
      billAmt5: 15000.0,
      billAmt6: 12000.0,
      payAmt1: 3000.0,
      payAmt2: 2500.0,
      payAmt3: 2000.0,
      payAmt4: 2000.0,
      payAmt5: 1500.0,
      payAmt6: 1500.0,
    );
  }

  // Preset 2: Khách hàng rủi ro cao (High Risk)
  factory CustomerInput.presetHighRisk() {
    return CustomerInput(
      limitBal: 50000.0,
      age: 28,
      sex: 1,
      education: 3,
      marriage: 1,
      pay0: 3,
      pay2: 3,
      pay3: 2,
      pay4: 2,
      pay5: 1,
      pay6: 1,
      billAmt1: 48000.0,
      billAmt2: 46000.0,
      billAmt3: 44000.0,
      billAmt4: 42000.0,
      billAmt5: 40000.0,
      billAmt6: 38000.0,
      payAmt1: 0.0,
      payAmt2: 0.0,
      payAmt3: 500.0,
      payAmt4: 0.0,
      payAmt5: 0.0,
      payAmt6: 0.0,
    );
  }

  // Preset 3: Khách hàng rủi ro thấp (Low Risk)
  factory CustomerInput.presetLowRisk() {
    return CustomerInput(
      limitBal: 500000.0,
      age: 45,
      sex: 2,
      education: 1,
      marriage: 1,
      pay0: -1,
      pay2: -1,
      pay3: -1,
      pay4: -1,
      pay5: -1,
      pay6: -1,
      billAmt1: 20000.0,
      billAmt2: 18000.0,
      billAmt3: 15000.0,
      billAmt4: 12000.0,
      billAmt5: 10000.0,
      billAmt6: 8000.0,
      payAmt1: 20000.0,
      payAmt2: 18000.0,
      payAmt3: 15000.0,
      payAmt4: 12000.0,
      payAmt5: 10000.0,
      payAmt6: 8000.0,
    );
  }
}
