import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../core/app_router.dart';
import '../widgets/feature_card.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    final isTablet = screenWidth > 600;
    final maxWidth = isTablet ? 500.0 : screenWidth;
    const double imageOpacity = 0.5;

    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SafeArea(
        child: Center(
          child: Container(
            constraints: BoxConstraints(maxWidth: maxWidth),
            child: Padding(
              padding: EdgeInsets.symmetric(
                horizontal: screenWidth * 0.05,
                vertical: screenHeight * 0.02,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Logo y título
                  _buildHeader(isTablet),
                  SizedBox(height: screenHeight * 0.02),

                  // Card principal con PageView
                  Expanded(
                    child: _buildMainCard(screenHeight, isTablet, imageOpacity),
                  ),
                  SizedBox(height: screenHeight * 0.02),

                  // Botones
                  _buildActionButtons(context, isTablet, screenHeight),
                  SizedBox(height: screenHeight * 0.015),

                  // Términos y condiciones
                  _buildTermsText(context, isTablet),
                  SizedBox(height: screenHeight * 0.01),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(bool isTablet) {
    return Row(
      children: [
        Container(
          width: isTablet ? 60 : 50,
          height: isTablet ? 60 : 50,
          decoration: const BoxDecoration(
            color: AppTheme.primaryColor,
            shape: BoxShape.circle,
          ),
          child: Icon(
            Icons.wifi,
            color: Colors.white,
            size: isTablet ? 32 : 28,
          ),
        ),
        const SizedBox(width: 12),
        Text(
          'Aulatap',
          style: TextStyle(
            fontSize: isTablet ? 32 : 28,
            fontWeight: FontWeight.bold,
            color: AppTheme.textPrimary,
          ),
        ),
      ],
    );
  }

  Widget _buildMainCard(double screenHeight, bool isTablet, double imageOpacity) {
    return Container(
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
      child: Column(
        children: [
          Expanded(
            child: PageView(
              controller: _pageController,
              onPageChanged: (int page) {
                setState(() {
                  _currentPage = page;
                });
              },
              children: [
                _buildPage1(screenHeight, isTablet, imageOpacity),
                _buildPage2(screenHeight, isTablet),
                _buildPage3(screenHeight, isTablet),
              ],
            ),
          ),
          _buildPageIndicator(screenHeight, isTablet),
        ],
      ),
    );
  }

  Widget _buildPageIndicator(double screenHeight, bool isTablet) {
    return Padding(
      padding: EdgeInsets.only(bottom: screenHeight * 0.02),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: List.generate(3, (index) {
          return Container(
            margin: const EdgeInsets.symmetric(horizontal: 4),
            width: isTablet ? 10 : 8,
            height: isTablet ? 10 : 8,
            decoration: BoxDecoration(
              color: _currentPage == index
                  ? AppTheme.primaryColor
                  : Colors.grey[300],
              shape: BoxShape.circle,
            ),
          );
        }),
      ),
    );
  }

  Widget _buildPage1(double screenHeight, bool isTablet, double imageOpacity) {
    return SingleChildScrollView(
      child: Column(
        children: [
          _buildImage(
            'assets/images/asistencia.jpg',
            screenHeight,
            Icons.nfc,
            AppTheme.page1Color,
            imageOpacity,
            isTablet,
          ),
          Padding(
            padding: EdgeInsets.all(screenHeight * 0.025),
            child: Column(
              children: [
                Text(
                  'Asistencia con un toque',
                  style: TextStyle(
                    fontSize: isTablet ? 26 : 22,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textPrimary,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: screenHeight * 0.012),
                Text(
                  'Registra la asistencia con NFC de forma rápida, segura y sin listas en papel.',
                  style: TextStyle(
                    fontSize: isTablet ? 16 : 14,
                    color: AppTheme.textSecondary,
                    height: 1.4,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: screenHeight * 0.02),
                FeatureCard(
                  icon: Icons.nfc,
                  text: 'Lectura NFC automática',
                  isTablet: isTablet,
                ),
                SizedBox(height: screenHeight * 0.012),
                FeatureCard(
                  icon: Icons.shield_outlined,
                  text: 'Seguridad con biometría',
                  isTablet: isTablet,
                ),
                SizedBox(height: screenHeight * 0.012),
                FeatureCard(
                  icon: Icons.access_time,
                  text: 'Historial y reportes',
                  isTablet: isTablet,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPage2(double screenHeight, bool isTablet) {
    return SingleChildScrollView(
      child: Column(
        children: [
          _buildImage(
            'assets/images/reportes.jpg',
            screenHeight,
            Icons.analytics_outlined,
            AppTheme.page2Color,
            0.5,
            isTablet,
          ),
          Padding(
            padding: EdgeInsets.all(screenHeight * 0.025),
            child: Column(
              children: [
                Text(
                  'Reportes en tiempo real',
                  style: TextStyle(
                    fontSize: isTablet ? 26 : 22,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textPrimary,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: screenHeight * 0.012),
                Text(
                  'Accede a estadísticas detalladas y exporta reportes de asistencia cuando los necesites.',
                  style: TextStyle(
                    fontSize: isTablet ? 16 : 14,
                    color: AppTheme.textSecondary,
                    height: 1.4,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: screenHeight * 0.02),
                FeatureCard(
                  icon: Icons.bar_chart,
                  text: 'Gráficas estadísticas',
                  isTablet: isTablet,
                ),
                SizedBox(height: screenHeight * 0.012),
                FeatureCard(
                  icon: Icons.file_download_outlined,
                  text: 'Exportación a Excel/PDF',
                  isTablet: isTablet,
                ),
                SizedBox(height: screenHeight * 0.012),
                FeatureCard(
                  icon: Icons.notifications_active,
                  text: 'Notificaciones automáticas',
                  isTablet: isTablet,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPage3(double screenHeight, bool isTablet) {
    return SingleChildScrollView(
      child: Column(
        children: [
          _buildImage(
            'assets/images/nube.jpg',
            screenHeight,
            Icons.cloud_done_outlined,
            AppTheme.page3Color,
            0.5,
            isTablet,
          ),
          Padding(
            padding: EdgeInsets.all(screenHeight * 0.025),
            child: Column(
              children: [
                Text(
                  'Todo en la nube',
                  style: TextStyle(
                    fontSize: isTablet ? 26 : 22,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textPrimary,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: screenHeight * 0.012),
                Text(
                  'Tus datos siempre seguros y accesibles desde cualquier dispositivo.',
                  style: TextStyle(
                    fontSize: isTablet ? 16 : 14,
                    color: AppTheme.textSecondary,
                    height: 1.4,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: screenHeight * 0.02),
                FeatureCard(
                  icon: Icons.cloud_upload,
                  text: 'Sincronización automática',
                  isTablet: isTablet,
                ),
                SizedBox(height: screenHeight * 0.012),
                FeatureCard(
                  icon: Icons.backup,
                  text: 'Respaldo automático',
                  isTablet: isTablet,
                ),
                SizedBox(height: screenHeight * 0.012),
                FeatureCard(
                  icon: Icons.devices,
                  text: 'Acceso multiplataforma',
                  isTablet: isTablet,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildImage(
      String assetPath,
      double screenHeight,
      IconData fallbackIcon,
      Color fallbackColor,
      double opacity,
      bool isTablet,
      ) {
    return ClipRRect(
      borderRadius: const BorderRadius.only(
        topLeft: Radius.circular(16),
        topRight: Radius.circular(16),
      ),
      child: Container(
        height: screenHeight * 0.22,
        constraints: const BoxConstraints(
          minHeight: 150,
          maxHeight: 250,
        ),
        child: Image.asset(
          assetPath,
          width: double.infinity,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return Container(
              color: fallbackColor,
              child: Center(
                child: Icon(
                  fallbackIcon,
                  size: isTablet ? 100 : 80,
                  color: Colors.white.withValues(alpha: opacity),
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildActionButtons(BuildContext context, bool isTablet, double screenHeight) {
    return Column(
      children: [
        SizedBox(
          width: double.infinity,
          height: isTablet ? 60 : 52,
          child: ElevatedButton(
            onPressed: () {
              Navigator.pushNamed(context, AppRouter.login);
            },
            child: const Text('Iniciar sesión'),
          ),
        ),
        SizedBox(height: screenHeight * 0.012),
        SizedBox(
          width: double.infinity,
          height: isTablet ? 60 : 52,
          child: ElevatedButton(
            onPressed: () {
              Navigator.pushNamed(context, AppRouter.register);
            },
            child: const Text('Crear cuenta'),
          ),
        ),
      ],
    );
  }

  Widget _buildTermsText(BuildContext context, bool isTablet) {
    return Center(
      child: Wrap(
        alignment: WrapAlignment.center,
        crossAxisAlignment: WrapCrossAlignment.center,
        children: [
          Text(
            'Al continuar, aceptas los ',
            style: TextStyle(
              fontSize: isTablet ? 15 : 13,
              color: AppTheme.textSecondary,
              height: 1.4,
            ),
          ),
          GestureDetector(
            onTap: () => _showTermsDialog(context),
            child: Text(
              'Términos',
              style: TextStyle(
                fontSize: isTablet ? 15 : 13,
                color: AppTheme.primaryColor,
                fontWeight: FontWeight.w600,
                height: 1.4,
                decoration: TextDecoration.underline,
              ),
            ),
          ),
          Text(
            ' y la ',
            style: TextStyle(
              fontSize: isTablet ? 15 : 13,
              color: AppTheme.textSecondary,
              height: 1.4,
            ),
          ),
          GestureDetector(
            onTap: () => _showPrivacyDialog(context),
            child: Text(
              'Política de privacidad',
              style: TextStyle(
                fontSize: isTablet ? 15 : 13,
                color: AppTheme.primaryColor,
                fontWeight: FontWeight.w600,
                height: 1.4,
                decoration: TextDecoration.underline,
              ),
            ),
          ),
          Text(
            '.',
            style: TextStyle(
              fontSize: isTablet ? 15 : 13,
              color: AppTheme.textSecondary,
              height: 1.4,
            ),
          ),
        ],
      ),
    );
  }

  void _showTermsDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text(
            'Términos y Condiciones',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          content: const SingleChildScrollView(
            child: Text(
              '1. Aceptación de términos\n\n'
                  'Al utilizar Aulatap, aceptas estos términos y condiciones en su totalidad.\n\n'
                  '2. Uso del servicio\n\n'
                  'El servicio está destinado exclusivamente para el registro de asistencia mediante tecnología NFC.\n\n'
                  '3. Responsabilidades del usuario\n\n'
                  '- Mantener la confidencialidad de tu cuenta\n'
                  '- Usar el servicio de forma responsable\n'
                  '- No compartir tus credenciales con terceros\n\n'
                  '4. Privacidad y datos\n\n'
                  'Tus datos serán tratados conforme a nuestra Política de Privacidad.\n\n'
                  '5. Modificaciones\n\n'
                  'Nos reservamos el derecho de modificar estos términos en cualquier momento.',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cerrar'),
            ),
          ],
        );
      },
    );
  }

  void _showPrivacyDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text(
            'Política de Privacidad',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          content: const SingleChildScrollView(
            child: Text(
              '1. Recopilación de información\n\n'
                  'Recopilamos información necesaria para el registro de asistencia, incluyendo:\n'
                  '- Nombre completo\n'
                  '- Identificación del dispositivo NFC\n'
                  '- Hora y fecha de registro\n\n'
                  '2. Uso de la información\n\n'
                  'La información recopilada se utiliza exclusivamente para:\n'
                  '- Registro de asistencia\n'
                  '- Generación de reportes\n'
                  '- Mejora del servicio\n\n'
                  '3. Seguridad\n\n'
                  'Implementamos medidas de seguridad para proteger tus datos, incluyendo cifrado y autenticación biométrica.\n\n'
                  '4. Compartir información\n\n'
                  'No compartimos tu información personal con terceros sin tu consentimiento.\n\n'
                  '5. Tus derechos\n\n'
                  'Tienes derecho a acceder, rectificar y eliminar tus datos personales en cualquier momento.',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cerrar'),
            ),
          ],
        );
      },
    );
  }
}