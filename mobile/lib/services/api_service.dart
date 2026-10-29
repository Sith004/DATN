import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/customer_input.dart';
import '../models/health_status.dart';
import '../models/prediction_history.dart';
import '../models/prediction_result.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;

  ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

class ApiService {
  static const Duration _defaultTimeout = Duration(seconds: 8);
  static const Duration _healthTimeout = Duration(seconds: 4);

  /// Kiểm tra trạng thái máy chủ FastAPI, ML Model và PostgreSQL
  static Future<HealthStatus> checkHealth() async {
    final baseUrl = await ApiConfig.getBaseUrl();
    final uri = Uri.parse('$baseUrl/health');

    try {
      final response = await http.get(uri).timeout(_healthTimeout);
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        return HealthStatus.fromJson(data);
      } else {
        throw ApiException(
          'Máy chủ phản hồi mã lỗi: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on SocketException catch (_) {
      throw ApiException('Không thể kết nối tới $baseUrl. Vui lòng kiểm tra Wi-Fi và IP máy chủ.');
    } on TimeoutException catch (_) {
      throw ApiException('Hết thời gian chờ phản hồi từ máy chủ (Timeout sau ${_healthTimeout.inSeconds}s).');
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('Lỗi kết nối máy chủ: $e');
    }
  }

  /// Gửi dữ liệu khách hàng lên FastAPI để thực hiện suy luận ML
  static Future<PredictionResult> predict(CustomerInput input) async {
    final baseUrl = await ApiConfig.getBaseUrl();
    final uri = Uri.parse('$baseUrl/api/v1/predictions');

    try {
      final response = await http
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(input.toJson()),
          )
          .timeout(_defaultTimeout);

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        return PredictionResult.fromJson(data);
      } else if (response.statusCode == 422) {
        final Map<String, dynamic> err = jsonDecode(utf8.decode(response.bodyBytes));
        throw ApiException('Dữ liệu nhập không hợp lệ (422): ${err['detail']}');
      } else {
        throw ApiException(
          'Lỗi máy chủ (${response.statusCode}): ${response.body}',
          statusCode: response.statusCode,
        );
      }
    } on SocketException catch (_) {
      throw ApiException('Mất kết nối mạng tới máy chủ. Vui lòng kiểm tra đường truyền.');
    } on TimeoutException catch (_) {
      throw ApiException('Yêu cầu dự báo bị quá thời gian chờ (${_defaultTimeout.inSeconds}s).');
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('Lỗi dự báo: $e');
    }
  }

  /// Truy vấn danh sách lịch sử dự báo từ PostgreSQL qua FastAPI
  static Future<PredictionHistoryResponse> getHistory({
    int page = 1,
    int pageSize = 10,
  }) async {
    final baseUrl = await ApiConfig.getBaseUrl();
    final uri = Uri.parse('$baseUrl/api/v1/predictions?page=$page&page_size=$pageSize');

    try {
      final response = await http.get(uri).timeout(_defaultTimeout);

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        return PredictionHistoryResponse.fromJson(data);
      } else {
        throw ApiException(
          'Không thể tải lịch sử dự báo (${response.statusCode})',
          statusCode: response.statusCode,
        );
      }
    } on SocketException catch (_) {
      throw ApiException('Không thể kết nối máy chủ để lấy lịch sử.');
    } on TimeoutException catch (_) {
      throw ApiException('Hết thời gian chờ phản hồi lịch sử.');
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('Lỗi lịch sử: $e');
    }
  }
}
