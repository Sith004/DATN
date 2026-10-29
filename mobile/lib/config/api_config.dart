import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiConfig {
  static const String _keyBaseUrl = 'api_base_url';
  
  // Default server address: Windows Host IP on Wi-Fi for physical phones
  static const String defaultBaseUrl = 'http://192.168.100.11:8000';

  // Common alternate presets
  static const String emulatorBaseUrl = 'http://10.0.2.2:8000';
  static const String localhostBaseUrl = 'http://127.0.0.1:8000';

  static String get effectiveDefaultUrl => kIsWeb ? localhostBaseUrl : defaultBaseUrl;

  static Future<String> getBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyBaseUrl) ?? effectiveDefaultUrl;
  }

  static Future<void> setBaseUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    // Normalize: strip trailing slash
    String normalized = url.trim();
    if (normalized.endsWith('/')) {
      normalized = normalized.substring(0, normalized.length - 1);
    }
    await prefs.setString(_keyBaseUrl, normalized);
  }

  static Future<void> resetToDefault() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyBaseUrl);
  }
}
