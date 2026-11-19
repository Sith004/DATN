import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Thẻ Header Đồ án Tốt nghiệp phong cách Ngân hàng số VCB-inspired
/// Thiết kế chống tràn viền 100% bằng cách sử dụng Layout thích ứng (Flexible & Wrap)
class BankingHeader extends StatelessWidget {
  final String title;
  final String subtitle;
  final String studentName;
  final String studentId;

  const BankingHeader({
    super.key,
    this.title = 'HỆ THỐNG ĐÁNH GIÁ RỦI RO TÍN DỤNG',
    this.subtitle = 'Mô hình Học máy Phân loại & Dự báo (UCI Dataset)',
    this.studentName = 'Nguyễn Trọng Thể',
    this.studentId = '1150080117',
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppTheme.primaryGreen, AppTheme.primaryDark],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryGreen.withValues(alpha: 0.25),
            blurRadius: 12,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Dòng nhãn danh mục & icon
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(7),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.18),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.account_balance, color: Colors.white, size: 20),
              ),
              const SizedBox(width: 10),
              const Expanded(
                child: Text(
                  'KHÓA LUẬN TỐT NGHIỆP — ĐH TÀI NGUYÊN & MÔI TRƯỜNG TP.HCM',
                  style: TextStyle(
                    color: Colors.white70,
                    fontSize: 10.5,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 0.6,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Tên đề tài lớn
          Text(
            title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16.5,
              fontWeight: FontWeight.w800,
              height: 1.28,
              letterSpacing: 0.2,
            ),
          ),
          const SizedBox(height: 5),

          // Mô tả ngắn
          Text(
            subtitle,
            style: TextStyle(
              color: Colors.white.withValues(alpha: 0.85),
              fontSize: 12,
              height: 1.3,
            ),
          ),
          const SizedBox(height: 14),

          // Vạch ngăn cách tinh tế
          Divider(color: Colors.white.withValues(alpha: 0.2), height: 1),
          const SizedBox(height: 12),

          // Thông tin sinh viên & MSSV - DÙNG WRAP ĐỂ KHÔNG BAO GIỜ BỊ OVERFLOW
          Wrap(
            spacing: 10,
            runSpacing: 8,
            crossAxisAlignment: WrapCrossAlignment.center,
            alignment: WrapAlignment.spaceBetween,
            children: [
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.person_outline, color: Colors.white70, size: 16),
                  const SizedBox(width: 5),
                  ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 160),
                    child: Text(
                      'SV: $studentName',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12.5,
                        fontWeight: FontWeight.w600,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 3.5),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.18),
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: Colors.white.withValues(alpha: 0.25), width: 0.8),
                ),
                child: Text(
                  'MSSV: $studentId',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 0.3,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

/// Thẻ Hành động Nghiệp vụ phong cách Ngân hàng số (VCB Quick Action Tile)
class BankingActionCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color iconColor;
  final Color iconBgColor;
  final VoidCallback onTap;
  final Widget? trailingBadge;

  const BankingActionCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.onTap,
    this.iconColor = AppTheme.primaryGreen,
    this.iconBgColor = AppTheme.primaryLight,
    this.trailingBadge,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(14),
        child: Ink(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 15),
          decoration: BoxDecoration(
            color: AppTheme.surfaceWhite,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppTheme.cardBorder, width: 1),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.03),
                blurRadius: 8,
                offset: const Offset(0, 3),
              ),
            ],
          ),
          child: Row(
            children: [
              Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  color: iconBgColor,
                  borderRadius: BorderRadius.circular(11),
                ),
                child: Icon(icon, color: iconColor, size: 24),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w700,
                        color: AppTheme.headingNavy,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 12,
                        color: AppTheme.bodyText,
                        height: 1.3,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              if (trailingBadge != null) ...[
                trailingBadge!,
                const SizedBox(width: 6),
              ],
              const Icon(Icons.arrow_forward_ios, size: 14, color: AppTheme.textMuted),
            ],
          ),
        ),
      ),
    );
  }
}

/// Tiêu đề phân đoạn nghiệp vụ (Section Header)
class SectionTitle extends StatelessWidget {
  final String title;
  final String? subtitle;
  final IconData? icon;

  const SectionTitle({
    super.key,
    required this.title,
    this.subtitle,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8, top: 4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 4,
                height: 16,
                decoration: BoxDecoration(
                  color: AppTheme.primaryGreen,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              const SizedBox(width: 8),
              if (icon != null) ...[
                Icon(icon, size: 17, color: AppTheme.primaryGreen),
                const SizedBox(width: 6),
              ],
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: 14.5,
                    fontWeight: FontWeight.w700,
                    color: AppTheme.headingNavy,
                    letterSpacing: 0.1,
                  ),
                ),
              ),
            ],
          ),
          if (subtitle != null) ...[
            const SizedBox(height: 3),
            Padding(
              padding: const EdgeInsets.only(left: 12),
              child: Text(
                subtitle!,
                style: const TextStyle(
                  fontSize: 11.5,
                  color: AppTheme.bodyText,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

/// Huy hiệu hiển thị mức độ Rủi ro (Risk Badge) - Có nhãn chữ, icon và màu ngữ nghĩa
class RiskBadge extends StatelessWidget {
  final String riskLevel;
  final bool isDefault;
  final double probability;

  const RiskBadge({
    super.key,
    required this.riskLevel,
    required this.isDefault,
    required this.probability,
  });

  @override
  Widget build(BuildContext context) {
    Color color;
    Color bgColor;
    IconData icon;
    String label;

    if (riskLevel.toLowerCase().contains('high') || isDefault) {
      color = AppTheme.riskHigh;
      bgColor = AppTheme.riskHighBg;
      icon = Icons.warning_amber_rounded;
      label = 'RỦI RO CAO (DEFAULT)';
    } else if (riskLevel.toLowerCase().contains('medium')) {
      color = AppTheme.riskMedium;
      bgColor = AppTheme.riskMediumBg;
      icon = Icons.info_outline;
      label = 'RỦI RO TRUNG BÌNH (RANH GIỚI)';
    } else {
      color = AppTheme.riskLow;
      bgColor = AppTheme.riskLowBg;
      icon = Icons.verified_user_outlined;
      label = 'RỦI RO THẤP (AN TOÀN)';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: color, width: 1.5),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(width: 8),
          Flexible(
            child: Text(
              label,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w800,
                color: color,
                letterSpacing: 0.3,
              ),
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}

/// Thẻ trạng thái một thành phần hệ thống chống tràn viền
class SystemStatusTile extends StatelessWidget {
  final String title;
  final String statusText;
  final bool isOnline;
  final IconData icon;

  const SystemStatusTile({
    super.key,
    required this.title,
    required this.statusText,
    required this.isOnline,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    final statusColor = isOnline ? AppTheme.riskLow : AppTheme.riskHigh;
    final statusBg = isOnline ? AppTheme.riskLowBg : AppTheme.riskHighBg;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: AppTheme.backgroundLight,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: AppTheme.cardBorder, width: 0.8),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(7),
            decoration: BoxDecoration(
              color: statusBg,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: statusColor, size: 18),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 12,
                    color: AppTheme.bodyText,
                    fontWeight: FontWeight.w500,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Text(
                  statusText,
                  style: TextStyle(
                    fontSize: 12.5,
                    fontWeight: FontWeight.w700,
                    color: statusColor,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: statusColor,
              shape: BoxShape.circle,
            ),
          ),
        ],
      ),
    );
  }
}
