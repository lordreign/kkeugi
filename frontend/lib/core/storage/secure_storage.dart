import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// JWT pair secure storage wrapper.
/// Android: KeyStore-backed encryption.
class SecureStorage {
  SecureStorage._();

  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
  );

  static const _kAccess = 'access_token';
  static const _kRefresh = 'refresh_token';

  static Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _storage.write(key: _kAccess, value: accessToken);
    await _storage.write(key: _kRefresh, value: refreshToken);
  }

  static Future<String?> readAccessToken() => _storage.read(key: _kAccess);
  static Future<String?> readRefreshToken() => _storage.read(key: _kRefresh);

  static Future<void> clear() async {
    await _storage.delete(key: _kAccess);
    await _storage.delete(key: _kRefresh);
  }

  static Future<bool> hasTokens() async {
    final access = await readAccessToken();
    return access != null;
  }
}
