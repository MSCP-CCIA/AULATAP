// lib/core/app_router.dart
import 'package:flutter/material.dart';

// NFC real
import '../ui/screens/nfc_screen.dart' as real;

// Stubs (ocultamos SettingsScreen para no confundirla con la real)
import '../ui/screens/stub_screens.dart' as stub hide SettingsScreen;

// Pantallas reales
import '../ui/screens/login_screen.dart';
import '../ui/screens/register_screen.dart';
import '../ui/screens/onboarding_screen.dart';
import '../ui/screens/home_screen.dart';
import '../ui/screens/history_screen.dart';
import '../ui/screens/class_history_detail_screen.dart';
import '../ui/screens/settings_screen.dart';

class AppRouter {
  // Rutas públicas
  static const String onboarding    = '/onboarding';
  static const String login         = '/login';
  static const String register      = '/register';
  static const String home          = '/home';

  // Rutas usadas por HomeScreen
  static const String nfc           = '/nfc';
  static const String history       = '/history';
  static const String settings      = '/settings';

  static const String takeAttendance = '/take-attendance';
  static const String classHistory   = '/class-history';
  static const String currentList    = '/current-list';
  static const String configuration  = '/configuration';

  static Route<dynamic> onGenerateRoute(RouteSettings routeSettings) {
    switch (routeSettings.name) {
      case onboarding:
        return MaterialPageRoute(builder: (_) => const OnboardingScreen());
      case login:
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case register:
        return MaterialPageRoute(builder: (_) => const RegisterScreen());
      case home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());

      case nfc:
        return MaterialPageRoute(builder: (_) => const real.NfcScreen());

      case history:
        return MaterialPageRoute(builder: (_) => const HistoryScreen());

      case classHistory:
        return MaterialPageRoute(
          builder: (_) => const ClassHistoryDetailScreen(),
          settings: routeSettings,
        );

      case settings:
        return MaterialPageRoute(builder: (_) => const SettingsScreen());


      case takeAttendance:
        return MaterialPageRoute(builder: (_) => const stub.TakeAttendanceScreen());
      case currentList:
        return MaterialPageRoute(builder: (_) => const stub.CurrentListScreen());
      case configuration:
        return MaterialPageRoute(builder: (_) => const stub.ConfigurationScreen());

      default:
        return MaterialPageRoute(
          builder: (_) => stub.UnknownRouteScreen(routeName: routeSettings.name ?? ''),
        );
    }
  }
}
