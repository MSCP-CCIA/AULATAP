import 'package:flutter/material.dart';

class Nav {
  /// Vuelve a la pantalla anterior si existe en la pila.
  /// Si no hay historial, navega a [fallbackRoute] limpiando la pila.
  static void backOrFallback(BuildContext context, String fallbackRoute) {
    final nav = Navigator.of(context);
    if (nav.canPop()) {
      nav.pop();
    } else {
      nav.pushNamedAndRemoveUntil(fallbackRoute, (r) => false);
    }
  }

  /// Navega a una ruta y limpia toda la pila (útil tras login/registro).
  static void goToClearingStack(BuildContext context, String route) {
    Navigator.of(context).pushNamedAndRemoveUntil(route, (r) => false);
  }
}
