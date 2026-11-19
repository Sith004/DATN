import 'package:flutter/material.dart';

/// Design System phong cách Ngân hàng Hiện đại (VCB-Inspired Financial Banking)
/// Được xây dựng riêng cho Đề tài Nghiên cứu Rủi ro Tín dụng DATN - Nguyễn Trọng Thể
class AppTheme {
  // ── 1. Bảng màu Nhận diện Cốt lõi (Core Brand Palette) ──────────────────────
  static const Color primaryGreen = Color(0xFF087C45); // Xanh lá tài chính VCB-inspired
  static const Color primaryDark = Color(0xFF075B35);  // Xanh lá đậm (Gradient / AppBar)
  static const Color primaryLight = Color(0xFFE8F5EE); // Nền xanh nhạt cho chip & badge
  static const Color accentGold = Color(0xFFE5A93C);   // Màu điểm xuyết vàng hoàng kim

  // ── 2. Nền và Bề mặt (Background & Surfaces) ──────────────────────────────
  static const Color backgroundLight = Color(0xFFF5F7F9); // Nền xám mát ngân hàng
  static const Color surfaceWhite = Color(0xFFFFFFFF);    // Bề mặt thẻ trắng sáng
  static const Color cardBorder = Color(0xFFE1E7ED);       // Đường viền thẻ thanh lịch
  static const Color dividerColor = Color(0xFFEAEFF4);

  // ── 3. Màu Văn bản (Typography Colors) ────────────────────────────────────
  static const Color headingNavy = Color(0xFF17324D);      // Tiêu đề xanh navy trầm
  static const Color bodyText = Color(0xFF526579);         // Nội dung phụ xám ghi
  static const Color textMuted = Color(0xFF8A9BA8);        // Chú thích nhạt

  // ── 4. Màu Đánh giá Rủi ro (Risk & Status Semantic Colors) ─────────────────
  // Rủi ro Thấp (< 30% default prob)
  static const Color riskLow = Color(0xFF218653);
  static const Color riskLowBg = Color(0xFFEAF7EE);

  // Rủi ro Trung bình / Ranh giới (30% - 59%)
  static const Color riskMedium = Color(0xFFD99118);
  static const Color riskMediumBg = Color(0xFFFFF7E6);

  // Rủi ro Cao (>= 60% threshold default)
  static const Color riskHigh = Color(0xFFC63F45);
  static const Color riskHighBg = Color(0xFFFDECEE);

  // ── 5. ThemeData Chuẩn Material 3 ──────────────────────────────────────────
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryGreen,
        primary: primaryGreen,
        secondary: accentGold,
        surface: surfaceWhite,
      ),
      scaffoldBackgroundColor: backgroundLight,
      fontFamily: null, // Sử dụng system font mặc định của Android hỗ trợ tiếng Việt sắc nét

      // Cấu hình AppBar phong cách ngân hàng sang trọng
      appBarTheme: const AppBarTheme(
        backgroundColor: primaryGreen,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: Colors.white,
          fontSize: 17,
          fontWeight: FontWeight.w700,
          letterSpacing: 0.4,
        ),
        iconTheme: IconThemeData(color: Colors.white),
      ),

      // Thẻ Card phẳng với viền mỏng và đổ bóng tinh tế
      cardTheme: CardThemeData(
        color: surfaceWhite,
        elevation: 0.8,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
          side: const BorderSide(color: cardBorder, width: 1),
        ),
        margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 0),
      ),

      // Trường nhập liệu chuẩn Banking Input
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: cardBorder),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: cardBorder),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: primaryGreen, width: 1.8),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: riskHigh, width: 1.2),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: riskHigh, width: 1.8),
        ),
        labelStyle: const TextStyle(color: bodyText, fontSize: 13.5),
        hintStyle: const TextStyle(color: textMuted, fontSize: 13.5),
        helperStyle: const TextStyle(fontSize: 11, color: bodyText),
        errorStyle: const TextStyle(fontSize: 11, color: riskHigh, fontWeight: FontWeight.w500),
      ),

      // Nút bấm chính phong cách ngân hàng số
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGreen,
          foregroundColor: Colors.white,
          elevation: 1.5,
          padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: const TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w700,
            letterSpacing: 0.3,
          ),
        ),
      ),

      // Nút bấm thứ cấp viền mỏng
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: primaryGreen,
          side: const BorderSide(color: primaryGreen, width: 1.3),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 13),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),

      // Chip chức năng
      chipTheme: ChipThemeData(
        backgroundColor: backgroundLight,
        selectedColor: primaryLight,
        labelStyle: const TextStyle(color: headingNavy, fontSize: 12.5, fontWeight: FontWeight.w500),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
          side: const BorderSide(color: cardBorder),
        ),
      ),
    );
  }
}
