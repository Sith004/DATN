import 'package:flutter_test/flutter_test.dart';
import 'package:credit_risk_app/main.dart';

void main() {
  testWidgets('App renders Home Dashboard smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const CreditRiskMobileApp());
    await tester.pump();

    // Verify key titles and student info are rendered
    expect(find.text('ĐÁNH GIÁ RỦI RO TÍN DỤNG'), findsOneWidget);
    expect(find.text('Sinh viên: Nguyễn Trọng Thể'), findsOneWidget);
    expect(find.text('MSSV: 1150080117'), findsOneWidget);
  });
}
