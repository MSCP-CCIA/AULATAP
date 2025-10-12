// lib/ui/screens/register_screen.dart
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../core/app_router.dart';
import '../../core/navigation_utils.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController(text: '');
  bool _authInProgress = false; // controla la barra animada
  int _currentStep = 0;

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  void _handleBack() {
    if (_currentStep > 0) {
      setState(() => _currentStep--); // volver de Paso 2 a Paso 1
      return;
    }
    // Si no hay historial, vuelve a Login o a donde definas
    Nav.backOrFallback(context, AppRouter.login);
  }

  void _continueWithMicrosoft() {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _authInProgress = true; // muestra/activa la barra indeterminada
    });

    // TODO: integra MSAL/OAuth aquí. Al finalizar:
    // setState(() {
    //   _authInProgress = false;
    //   _currentStep = 1; // opcional: pasar al paso 2
    // });
  }

  void _verifyAndContinue() {
    Nav.goToClearingStack(context, AppRouter.home);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (bool didPop, Object? result) {
        if (didPop) return;
        _handleBack();
      },
      child: Scaffold(
        backgroundColor: AppTheme.backgroundColor,
        body: SafeArea(
          child: Stack(
            children: [
              SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24.0)
                    .copyWith(bottom: 120),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(height: size.height * 0.02),

                      // Header
                      Row(
                        children: [
                          IconButton(
                            icon: const Icon(Icons.arrow_back,
                                color: AppTheme.textPrimary),
                            onPressed: _handleBack,
                            padding: EdgeInsets.zero,
                            constraints: const BoxConstraints(),
                          ),
                          const SizedBox(width: 16),
                          const Text(
                            'Verifica tu cuenta',
                            style: TextStyle(
                              color: AppTheme.textPrimary,
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),

                      SizedBox(height: size.height * 0.02),

                      // Tarjeta: Confirma tu correo (Paso 1 de 2)
                      _buildConfirmEmailCard(),

                      const SizedBox(height: 16),

                      // Tarjeta: Información básica
                      _buildInfoBasicCard(),

                      const SizedBox(height: 24),
                    ],
                  ),
                ),
              ),

              // Footer fijo
              Positioned(
                left: 0,
                right: 0,
                bottom: 0,
                child: Container(
                  decoration: BoxDecoration(
                    color: AppTheme.backgroundColor,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.06),
                        blurRadius: 10,
                        offset: const Offset(0, -2),
                      ),
                    ],
                  ),
                  padding:
                  const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  child: Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () =>
                              Nav.backOrFallback(context, AppRouter.login),
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            side:
                            const BorderSide(color: AppTheme.primaryColor),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text(
                            'Más tarde',
                            style: TextStyle(
                              color: AppTheme.primaryColor,
                              fontSize: 15,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton(
                          onPressed: _verifyAndContinue,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.primaryColor,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 0,
                          ),
                          child: const Text(
                            'Verificar y continuar',
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ---------- Secciones ----------

  Widget _buildConfirmEmailCard() {
    return _card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _stepChip('Paso 1 de 2'),
          const SizedBox(height: 16),
          const Text(
            'Confirma tu correo',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w700,
              color: AppTheme.textPrimary,
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Usa tu correo institucional con Microsoft para crear tu cuenta.',
            style: TextStyle(
              fontSize: 13,
              color: AppTheme.textSecondary,
              height: 1.4,
            ),
          ),
          const SizedBox(height: 20),

          // Campo correo
          TextFormField(
            controller: _emailController,
            keyboardType: TextInputType.emailAddress,
            style: const TextStyle(fontSize: 14),
            decoration: InputDecoration(
              hintText: 'sebastian.otalora01@usa.edu.co',
              hintStyle: TextStyle(fontSize: 13, color: Colors.grey[400]),
              prefixIcon: const Icon(Icons.email_outlined, size: 20),
              filled: true,
              fillColor: Colors.grey[50],
              contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.grey[300]!),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.grey[300]!),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide:
                const BorderSide(color: AppTheme.primaryColor, width: 2),
              ),
            ),
            validator: (v) {
              if (v == null || v.trim().isEmpty) {
                return 'Por favor ingresa tu correo';
              }
              if (!RegExp(r'^[^@]+@[^@]+\.[^@]+$').hasMatch(v.trim())) {
                return 'Ingresa un correo válido';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),

          // Botón Microsoft
          SizedBox(
            width: double.infinity,
            height: 48,
            child: ElevatedButton(
              onPressed: _continueWithMicrosoft,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF34C759), // verde
                foregroundColor: Colors.white,
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _microsoftLogo(size: 16), // logo sin overflow
                  const SizedBox(width: 10),
                  const Text(
                    'Continuar con Microsoft',
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),

          // Nota + barra animada (visible sólo al pulsar)
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.info_outline, size: 18, color: Colors.grey[700]),
              const SizedBox(width: 8),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Serás redirigido a Microsoft para autenticarte con tu institución.',
                      style: TextStyle(
                        fontSize: 12,
                        color: AppTheme.textSecondary,
                        height: 1.4,
                      ),
                    ),
                    _progressArea(), // <- aparece/animada tras click
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildInfoBasicCard() {
    return _card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Información básica',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w700,
              color: AppTheme.textPrimary,
            ),
          ),
          const SizedBox(height: 16),
          _infoField(
            label: 'Nombre y apellido (se completará automáticamente)',
            icon: Icons.person_outline,
          ),
          const SizedBox(height: 12),
          _infoField(
            label: 'Rol (Estudiante o Docente)',
            icon: Icons.business_outlined,
          ),
          const SizedBox(height: 8),
          const Text(
            'Estos datos se sincronizan tras la verificación con Microsoft.',
            style: TextStyle(
              fontSize: 13,
              color: AppTheme.textSecondary,
              height: 1.4,
            ),
          ),
        ],
      ),
    );
  }

  // ---------- Helpers UI ----------

  Widget _card({required Widget child}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: child,
    );
  }

  Widget _stepChip(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppTheme.primaryColor.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        text,
        style: const TextStyle(
          fontSize: 11,
          color: AppTheme.primaryColor,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }

  Widget _infoField({required String label, required IconData icon}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Row(
        children: [
          Icon(icon, size: 20, color: Colors.grey[600]),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              label,
              style: TextStyle(
                fontSize: 13,
                color: Colors.grey[600],
                height: 1.4,
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Área de progreso que aparece/desaparece con animación.
  Widget _progressArea() {
    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 250),
      child: _authInProgress
          ? Padding(
        key: const ValueKey('progress'),
        padding: const EdgeInsets.only(top: 8),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(6),
          child: const LinearProgressIndicator(
            value: null, // indeterminado (animado)
            minHeight: 6,
            backgroundColor: Color(0xFFEFF1F5),
            color: AppTheme.primaryColor,
          ),
        ),
      )
          : const SizedBox(key: ValueKey('no-progress'), height: 0),
    );
  }

  /// Logo de Microsoft 2x2 sin overflow (ajusta gaps a la caja).
  Widget _microsoftLogo({double size = 16}) {
    const gap = 1.0;                 // espacio entre cuadros
    final tile = (size - gap) / 2;   // cada cuadro ajustado al gap
    Widget sq(Color c) => Container(width: tile, height: tile, color: c);

    return SizedBox(
      width: size,
      height: size,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(mainAxisSize: MainAxisSize.min, children: [
            sq(const Color(0xFFF25022)), const SizedBox(width: gap),
            sq(const Color(0xFF7FBA00)),
          ]),
          const SizedBox(height: gap),
          Row(mainAxisSize: MainAxisSize.min, children: [
            sq(const Color(0xFF00A4EF)), const SizedBox(width: gap),
            sq(const Color(0xFFFFB900)),
          ]),
        ],
      ),
    );
  }
}
