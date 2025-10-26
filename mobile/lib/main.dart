import 'package:flutter/material.dart';
import 'core/app_router.dart';
import 'core/app_theme.dart';

void main() => runApp(const AulatapApp());

class AulatapApp extends StatelessWidget {
  const AulatapApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Aulatap',
      theme: ThemeData(
        primaryColor: AppTheme.primaryColor,
        useMaterial3: false,
      ),
      initialRoute: AppRouter.onboarding,   // o AppRouter.home
      onGenerateRoute: AppRouter.onGenerateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}
