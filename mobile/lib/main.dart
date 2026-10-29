import 'package:flutter/material.dart';
import 'screens/home_dashboard_screen.dart';
import 'theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const CreditRiskMobileApp());
}

class CreditRiskMobileApp extends StatelessWidget {
  const CreditRiskMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Credit Risk ML - Nguyễn Trọng Thể',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const HomeDashboardScreen(),
    );
  }
}
