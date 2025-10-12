import 'package:flutter/material.dart';
import '../../core/app_theme.dart';

class StubScaffold extends StatelessWidget {
  final String title;
  final IconData icon;
  const StubScaffold({super.key, required this.title, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      appBar: AppBar(
        title: Text(title),
        centerTitle: false,
        elevation: 0,
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 72, color: AppTheme.primaryColor),
            const SizedBox(height: 12),
            Text(title,
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w700,
                  color: AppTheme.textPrimary,
                )),
            const SizedBox(height: 6),
            const Text('Pantalla provisional. Implementa aquí tu UI.',
                style: TextStyle(color: AppTheme.textSecondary)),
          ],
        ),
      ),
    );
  }
}

// Stubs específicos
class NfcScreen extends StatelessWidget {
  const NfcScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const StubScaffold(title: 'NFC', icon: Icons.nfc);
}

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const StubScaffold(title: 'Historial', icon: Icons.schedule_outlined);
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const StubScaffold(title: 'Ajustes', icon: Icons.tune_rounded);
}

class TakeAttendanceScreen extends StatelessWidget {
  const TakeAttendanceScreen({super.key});
  @override
  Widget build(BuildContext context) => const StubScaffold(
      title: 'Tomar asistencia', icon: Icons.wifi_tethering);
}

class ClassHistoryScreen extends StatelessWidget {
  const ClassHistoryScreen({super.key});
  @override
  Widget build(BuildContext context) => const StubScaffold(
      title: 'Historial de clases', icon: Icons.history);
}

class CurrentListScreen extends StatelessWidget {
  const CurrentListScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const StubScaffold(title: 'Lista actual', icon: Icons.view_list);
}

class ConfigurationScreen extends StatelessWidget {
  const ConfigurationScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const StubScaffold(title: 'Configuración', icon: Icons.settings);
}

class UnknownRouteScreen extends StatelessWidget {
  final String routeName;
  const UnknownRouteScreen({super.key, required this.routeName});
  @override
  Widget build(BuildContext context) => StubScaffold(
    title: 'Ruta no encontrada: $routeName',
    icon: Icons.error_outline,
  );
}
