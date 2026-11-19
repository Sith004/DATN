import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:credit_risk_app/main.dart';
import 'package:credit_risk_app/models/customer_input.dart';
import 'package:credit_risk_app/models/prediction_result.dart';
import 'package:credit_risk_app/screens/customer_input_form_screen.dart';
import 'package:credit_risk_app/screens/prediction_result_screen.dart';
import 'package:credit_risk_app/screens/settings_screen.dart';
import 'package:credit_risk_app/theme/app_theme.dart';

void main() {
  testWidgets('Test 1: App renders Home Dashboard VCB-inspired smoke test', (WidgetTester tester) async {
    // Build app
    await tester.pumpWidget(const CreditRiskMobileApp());
    await tester.pump();

    // Verify key titles and student info are rendered
    expect(find.text('ĐÁNH GIÁ RỦI RO TÍN DỤNG'), findsOneWidget);
    expect(find.text('ỨNG DỤNG MACHINE LEARNING TRONG DỰ BÁO RỦI RO TÍN DỤNG'), findsOneWidget);
    expect(find.text('SV: Nguyễn Trọng Thể'), findsOneWidget);
    expect(find.text('MSSV: 1150080117'), findsOneWidget);
    expect(find.text('Đánh giá Rủi ro Khách hàng'), findsOneWidget);
    expect(find.text('Sổ phụ Lịch sử Thẩm định'), findsOneWidget);
  });

  testWidgets('Test 2: Home Dashboard does NOT overflow on narrow screen (320x640)', (WidgetTester tester) async {
    // Set screen size to narrow phone (320x640)
    tester.view.physicalSize = const Size(320, 640);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    FlutterErrorDetails? caughtDetails;
    final previousOnError = FlutterError.onError;
    FlutterError.onError = (FlutterErrorDetails details) {
      caughtDetails = details;
    };

    await tester.pumpWidget(const CreditRiskMobileApp());
    await tester.pump();

    FlutterError.onError = previousOnError;

    expect(caughtDetails, isNull);
    expect(find.text('SV: Nguyễn Trọng Thể'), findsOneWidget);
    expect(find.text('MSSV: 1150080117'), findsOneWidget);
  });

  testWidgets('Test 3: CustomerInputFormScreen renders 23 fields & Quick Presets', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: AppTheme.lightTheme,
        home: const CustomerInputFormScreen(),
      ),
    );
    await tester.pump();

    // Check title and presets
    expect(find.text('HỒ SƠ KHÁCH HÀNG (23 BIẾN)'), findsOneWidget);
    expect(find.text('Rủi ro thấp (<30%)'), findsOneWidget);
    expect(find.text('Bình thường (~12%)'), findsOneWidget);
    expect(find.text('Rủi ro cao (>=60%)'), findsOneWidget);
    expect(find.text('TIẾN HÀNH THẨM ĐỊNH RỦI RO'), findsOneWidget);
  });

  testWidgets('Test 4: PredictionResultScreen displays risk badge, probability and SHAP factors', (WidgetTester tester) async {
    final mockResult = PredictionResult(
      predictionProbability: 0.7822,
      predictionLabel: 'Default',
      riskLevel: 'High Risk',
      threshold: 0.60,
      modelVersion: 'xgboost_tuned_v1',
      recordId: 101,
      persisted: true,
      persistenceMessage: 'Đã lưu thành công',
      topRiskFactors: [
        RiskFactor(feature: 'MAX_PAY_DELAY', shapValue: 0.48, rawValue: 3.0, direction: '+ Tăng rủi ro'),
        RiskFactor(feature: 'PAY_0', shapValue: 0.42, rawValue: 3.0, direction: '+ Tăng rủi ro'),
      ],
    );

    final mockInput = CustomerInput.presetHighRisk();

    await tester.pumpWidget(
      MaterialApp(
        theme: AppTheme.lightTheme,
        home: PredictionResultScreen(result: mockResult, input: mockInput),
      ),
    );
    await tester.pump();

    expect(find.text('KẾT QUẢ THẨM ĐỊNH TÍN DỤNG'), findsOneWidget);
    expect(find.text('CẢNH BÁO: KHÁCH HÀNG VỠ NỢ'), findsOneWidget);
    expect(find.text('78.22%'), findsOneWidget);
    expect(find.text('60%'), findsOneWidget);
    expect(find.text('MAX_PAY_DELAY'), findsOneWidget);
    expect(find.text('PAY_0'), findsOneWidget);
  });

  testWidgets('Test 5: SettingsScreen renders Base URL input and Preset chips', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: AppTheme.lightTheme,
        home: const SettingsScreen(),
      ),
    );
    await tester.pump();

    expect(find.text('CÀI ĐẶT HẠ TẦNG KẾT NỐI'), findsOneWidget);
    expect(find.text('Kiểm tra Kết nối Trực tiếp'), findsOneWidget);
    expect(find.text('LƯU VÀ ÁP DỤNG CẤU HÌNH'), findsOneWidget);
  });
}
