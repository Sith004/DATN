import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/prediction_history.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';

class PredictionHistoryScreen extends StatefulWidget {
  const PredictionHistoryScreen({super.key});

  @override
  State<PredictionHistoryScreen> createState() => _PredictionHistoryScreenState();
}

class _PredictionHistoryScreenState extends State<PredictionHistoryScreen> {
  final List<PredictionHistoryItem> _items = [];
  bool _isLoading = true;
  String? _errorMessage;
  int _currentPage = 1;
  final int _pageSize = 15;
  int _totalRecords = 0;
  bool _hasMore = true;
  bool _isLoadingMore = false;

  final ScrollController _scrollController = ScrollController();
  final NumberFormat _currencyFormat = NumberFormat.currency(locale: 'vi_VN', symbol: 'NT\$', decimalDigits: 0);

  @override
  void initState() {
    super.initState();
    _fetchHistory(page: 1, isRefresh: true);
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 200 &&
        !_isLoadingMore &&
        _hasMore) {
      _loadMore();
    }
  }

  Future<void> _fetchHistory({int page = 1, bool isRefresh = false}) async {
    if (isRefresh) {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });
    }

    try {
      final response = await ApiService.getHistory(page: page, pageSize: _pageSize);

      if (mounted) {
        setState(() {
          if (isRefresh) {
            _items.clear();
          }
          _items.addAll(response.items);
          _totalRecords = response.total;
          _currentPage = page;
          _hasMore = _items.length < _totalRecords;
          _isLoading = false;
          _isLoadingMore = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString();
          _isLoading = false;
          _isLoadingMore = false;
        });
      }
    }
  }

  Future<void> _loadMore() async {
    if (_isLoadingMore || !_hasMore) return;

    setState(() {
      _isLoadingMore = true;
    });

    await _fetchHistory(page: _currentPage + 1, isRefresh: false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SỔ PHỤ LỊCH SỬ THẨM ĐỊNH'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Làm mới dữ liệu',
            onPressed: () => _fetchHistory(page: 1, isRefresh: true),
          ),
        ],
      ),
      body: RefreshIndicator(
        color: AppTheme.primaryGreen,
        onRefresh: () => _fetchHistory(page: 1, isRefresh: true),
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(color: AppTheme.primaryGreen),
            SizedBox(height: 14),
            Text(
              'Đang tải sổ phụ lịch sử từ PostgreSQL...',
              style: TextStyle(color: AppTheme.bodyText, fontSize: 13),
            ),
          ],
        ),
      );
    }

    if (_errorMessage != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.cloud_off_outlined, color: AppTheme.riskHigh, size: 54),
              const SizedBox(height: 14),
              const Text(
                'Không thể tải dữ liệu lịch sử',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.headingNavy),
              ),
              const SizedBox(height: 8),
              Text(
                _errorMessage!,
                textAlign: TextAlign.center,
                style: const TextStyle(color: AppTheme.bodyText, fontSize: 13),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                icon: const Icon(Icons.refresh, size: 18),
                label: const Text('Thử lại'),
                onPressed: () => _fetchHistory(page: 1, isRefresh: true),
              ),
            ],
          ),
        ),
      );
    }

    if (_items.isEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(18),
                decoration: const BoxDecoration(
                  color: AppTheme.primaryLight,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.assignment_outlined, size: 48, color: AppTheme.primaryGreen),
              ),
              const SizedBox(height: 16),
              const Text(
                'Chưa có hồ sơ thẩm định nào',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.headingNavy),
              ),
              const SizedBox(height: 6),
              const Text(
                'Các hồ sơ sau khi thực hiện thẩm định thành công sẽ tự động lưu trữ tại đây.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 13, color: AppTheme.bodyText),
              ),
            ],
          ),
        ),
      );
    }

    return Column(
      children: [
        // Thanh thông tin tổng số lượng hồ sơ
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: const BoxDecoration(
            color: AppTheme.primaryLight,
            border: Border(bottom: BorderSide(color: AppTheme.cardBorder)),
          ),
          child: Row(
            children: [
              const Icon(Icons.storage_outlined, size: 16, color: AppTheme.primaryGreen),
              const SizedBox(width: 8),
              Text(
                'Cơ sở dữ liệu: $_totalRecords hồ sơ đã ghi nhận',
                style: const TextStyle(
                  fontSize: 12.5,
                  fontWeight: FontWeight.w700,
                  color: AppTheme.primaryDark,
                ),
              ),
              const Spacer(),
              const Text(
                'Mới nhất',
                style: TextStyle(fontSize: 11.5, color: AppTheme.bodyText, fontWeight: FontWeight.w500),
              ),
            ],
          ),
        ),

        // Danh sách hồ sơ lịch sử
        Expanded(
          child: ListView.separated(
            controller: _scrollController,
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            itemCount: _items.length + (_hasMore ? 1 : 0),
            separatorBuilder: (context, index) => const SizedBox(height: 8),
            itemBuilder: (context, index) {
              if (index == _items.length) {
                return const Center(
                  child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    child: SizedBox(
                      width: 22,
                      height: 22,
                      child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.primaryGreen),
                    ),
                  ),
                );
              }

              final item = _items[index];
              return _buildHistoryCard(item);
            },
          ),
        ),
      ],
    );
  }

  Widget _buildHistoryCard(PredictionHistoryItem item) {
    final double probPercent = item.defaultProbability * 100;
    final bool isDefault = item.defaultProbability >= 0.60;

    Color riskColor;
    Color riskBg;
    if (isDefault) {
      riskColor = AppTheme.riskHigh;
      riskBg = AppTheme.riskHighBg;
    } else if (item.riskLevel.toLowerCase().contains('medium')) {
      riskColor = AppTheme.riskMedium;
      riskBg = AppTheme.riskMediumBg;
    } else {
      riskColor = AppTheme.riskLow;
      riskBg = AppTheme.riskLowBg;
    }

    // Format thời gian hiển thị
    String formattedTime = item.createdAt;
    try {
      final parsed = DateTime.parse(item.createdAt).toLocal();
      formattedTime = DateFormat('dd/MM/yyyy HH:mm:ss').format(parsed);
    } catch (_) {}

    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppTheme.backgroundLight,
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: AppTheme.cardBorder),
                  ),
                  child: Text(
                    '#${item.id}',
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.headingNavy),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    formattedTime,
                    style: const TextStyle(fontSize: 11.5, color: AppTheme.textMuted),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: riskBg,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    isDefault ? 'DEFAULT' : 'NON-DEFAULT',
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w800,
                      color: riskColor,
                    ),
                  ),
                ),
              ],
            ),
            const Divider(height: 16, color: AppTheme.dividerColor),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Hạn mức (LIMIT_BAL)', style: TextStyle(fontSize: 11, color: AppTheme.bodyText)),
                      const SizedBox(height: 2),
                      Text(
                        _currencyFormat.format(item.limitBal),
                        style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700, color: AppTheme.headingNavy),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Độ tuổi (AGE)', style: TextStyle(fontSize: 11, color: AppTheme.bodyText)),
                      const SizedBox(height: 2),
                      Text(
                        '${item.age} tuổi',
                        style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w600, color: AppTheme.headingNavy),
                      ),
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    const Text('Xác suất vỡ nợ', style: TextStyle(fontSize: 11, color: AppTheme.bodyText)),
                    const SizedBox(height: 2),
                    Text(
                      '${probPercent.toStringAsFixed(1)}%',
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: riskColor,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
