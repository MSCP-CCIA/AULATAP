// Pruebas para la aplicación Aulatap

import 'package:flutter_test/flutter_test.dart';

import 'package:aulatap/main.dart';

void main() {
  testWidgets('Verificar que la pantalla de bienvenida se muestra correctamente', (WidgetTester tester) async {
    // Construir la app
    await tester.pumpWidget(const AulatapApp());

    // Verificar que el título "Aulatap" aparece
    expect(find.text('Aulatap'), findsOneWidget);

    // Verificar que el título principal aparece
    expect(find.text('Asistencia con un toque'), findsOneWidget);

    // Verificar que los botones aparecen
    expect(find.text('Iniciar sesión'), findsOneWidget);
    expect(find.text('Crear cuenta'), findsOneWidget);

    // Verificar que las características aparecen
    expect(find.text('Lectura NFC automática'), findsOneWidget);
    expect(find.text('Seguridad con biometría'), findsOneWidget);
    expect(find.text('Historial y reportes'), findsOneWidget);
  });

  testWidgets('Verificar que los botones responden al tap', (WidgetTester tester) async {
    // Construir la app
    await tester.pumpWidget(const AulatapApp());

    // Encontrar y presionar el botón "Iniciar sesión"
    final loginButton = find.text('Iniciar sesión');
    expect(loginButton, findsOneWidget);
    await tester.tap(loginButton);
    await tester.pump();

    // Encontrar y presionar el botón "Crear cuenta"
    final signupButton = find.text('Crear cuenta');
    expect(signupButton, findsOneWidget);
    await tester.tap(signupButton);
    await tester.pump();

    // Si llegamos aquí, los botones funcionan correctamente
  });
}