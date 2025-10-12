// lib/core/auth_ms.dart
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:aad_oauth/aad_oauth.dart';
import 'package:aad_oauth/model/config.dart';
import 'package:http/http.dart' as http;

class MsAuth {
  MsAuth._();

  static final navKey = GlobalKey<NavigatorState>();
  static late AadOAuth _oauth;

  /// Llama esto una sola vez (en main) con tus IDs reales.
  static void init({
    required String tenantId,
    required String clientId,
  }) {
    final config = Config(
      tenant: tenantId,
      clientId: clientId,
      scope: 'openid profile offline_access User.Read',
      // Para apps nativas sin secreto (PKCE):
      redirectUri: 'https://login.microsoftonline.com/common/oauth2/nativeclient',
      navigatorKey: navKey,
      loader: const Center(child: CircularProgressIndicator()),
      webUseRedirect: true,
    );
    _oauth = AadOAuth(config);
  }

  /// Inicia sesión e intenta devolver un access token válido.
  static Future<String> signInAndGetAccessToken() async {
    await _oauth.login(); // abre el flujo interactivo
    final token = await _oauth.getAccessToken();
    if (token == null || token.isEmpty) {
      throw Exception('No se obtuvo token de acceso.');
    }
    return token;
  }

  /// Devuelve /me de Graph con nombre y correo.
  static Future<UserProfile> getProfile() async {
    final token = await _oauth.getAccessToken();
    if (token == null || token.isEmpty) {
      throw Exception('Sin token. Inicia sesión primero.');
    }
    final me = await _getMe(token);
    final name = (me['displayName'] as String?) ?? '';
    final mail = (me['mail'] as String?) ?? (me['userPrincipalName'] as String? ?? '');
    return UserProfile(displayName: name, email: mail);
  }

  static Future<Map<String, dynamic>> _getMe(String token) async {
    final uri = Uri.parse(
      'https://graph.microsoft.com/v1.0/me?'
      r'$select=displayName,mail,userPrincipalName',
    );
    final r = await http.get(uri, headers: {'Authorization': 'Bearer $token'});
    if (r.statusCode != 200) {
      throw Exception('Graph /me falló (${r.statusCode})');
    }
    return json.decode(r.body) as Map<String, dynamic>;
  }
}

class UserProfile {
  final String displayName;
  final String email;
  const UserProfile({required this.displayName, required this.email});
}
