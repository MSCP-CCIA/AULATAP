import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../core/app_router.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _searchController = TextEditingController();

  // Paleta local para igualar la maqueta
  static const _blue = Color(0xFF0A84FF);
  static const _cardStroke = Color(0xFFE6EBF0);
  static const _iconMint = Color(0xFFEAF6EF);
  static const _okGreen = Color(0xFF22C55E);
  static const _textPrimary = AppTheme.textPrimary;
  static const _bg = AppTheme.backgroundColor;

  // Mock de próximas clases
  final List<_UpcomingClass> _upcoming = const [
    _UpcomingClass(
      title: 'Matemática I · Aula 204',
      timeRange: '08:00 – 09:30',
      students: 28,
      statusColor: _okGreen,
    ),
    _UpcomingClass(
      title: 'Historia · Sala 3',
      timeRange: '10:00 – 11:30',
      students: 31,
      statusColor: _okGreen,
    ),
    _UpcomingClass(
      title: 'Física II · Lab 2',
      timeRange: '13:00 – 14:30',
      students: 24,
      statusColor: _okGreen,
    ),
  ];

  int _currentTab = 0;

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _onBottomTap(int i) {
    if (i == _currentTab) return;
    setState(() => _currentTab = i);
    switch (i) {
      case 0:
        break;
      case 1:
        Navigator.pushNamed(context, AppRouter.nfc);
        break;
      case 2:
        Navigator.pushNamed(context, AppRouter.history);
        break;
      case 3:
        Navigator.pushNamed(context, AppRouter.settings);
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _bg,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
                child: _buildHeader(),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: _buildSearchField(),
              ),
            ),

            // Grid de acciones (cards con borde)
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              sliver: SliverGrid(
                delegate: SliverChildListDelegate.fixed([
                  _ActionCard(
                    icon: Icons.wifi_tethering,
                    iconBg: _iconMint,
                    title: 'Tomar\nasistencia',
                    subtitle: 'Escanea carnet NFC',
                    onTap: () => Navigator.pushNamed(context, AppRouter.takeAttendance),
                  ),
                  _ActionCard(
                    icon: Icons.history,
                    iconBg: _iconMint,
                    title: 'Historial de\nclases',
                    subtitle: 'Ver sesiones previas',
                    onTap: () => Navigator.pushNamed(context, AppRouter.classHistory),
                  ),
                  _ActionCard(
                    icon: Icons.view_list_rounded,
                    iconBg: _iconMint,
                    title: 'Lista actual',
                    subtitle: 'Presentes y ausentes',
                    onTap: () => Navigator.pushNamed(context, AppRouter.currentList),
                  ),
                  _ActionCard(
                    icon: Icons.settings_rounded,
                    iconBg: _iconMint,
                    title: 'Configuración',
                    subtitle: 'Preferencias',
                    onTap: () => Navigator.pushNamed(context, AppRouter.configuration),
                  ),
                ]),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  mainAxisSpacing: 14,
                  crossAxisSpacing: 14,
                  childAspectRatio: 1.17,
                ),
              ),
            ),

            // Próximas clases
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 10, 16, 8),
                child: const Text(
                  'Próximas clases',
                  style: TextStyle(
                    fontSize: 18, fontWeight: FontWeight.w700, color: _textPrimary,
                  ),
                ),
              ),
            ),
            SliverList(
              delegate: SliverChildBuilderDelegate(
                    (ctx, i) {
                  final c = _upcoming[i];
                  return Padding(
                    padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                    child: _UpcomingTile(
                      data: c,
                      onTake: () => Navigator.pushNamed(context, AppRouter.takeAttendance),
                    ),
                  );
                },
                childCount: _upcoming.length,
              ),
            ),
            const SliverToBoxAdapter(child: SizedBox(height: 90)),
          ],
        ),
      ),

      // Bottom navigation con "pill" azul en el seleccionado
      bottomNavigationBar: AulatapBottomNav(
        currentIndex: _currentTab,
        onTap: _onBottomTap,
        activeColor: _blue,
      ),
    );
  }

  // ===== Header =====
  Widget _buildHeader() {
    return Row(
      children: [
        const Expanded(
          child: Text(
            'Aulatap',
            style: TextStyle(
              fontSize: 24, fontWeight: FontWeight.w800, color: _textPrimary,
            ),
          ),
        ),
        Material(
          color: Colors.transparent,
          child: InkWell(
            borderRadius: BorderRadius.circular(20),
            onTap: () {},
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: const [
                CircleAvatar(
                  radius: 16,
                  backgroundImage: AssetImage('assets/images/avatar_sample.jpg'),
                ),
                SizedBox(width: 4),
                Icon(Icons.expand_more, size: 18, color: _textPrimary),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // ===== Buscador =====
  Widget _buildSearchField() {
    return ConstrainedBox(
      constraints: const BoxConstraints(minHeight: 50),
      child: TextField(
        controller: _searchController,
        textInputAction: TextInputAction.search,
        decoration: InputDecoration(
          hintText: 'Buscar clase, grupo o alumno',
          hintStyle: TextStyle(color: Colors.grey[600], fontSize: 14),
          prefixIcon: const Icon(Icons.search, size: 20),
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(24),
            borderSide: const BorderSide(color: _cardStroke),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(24),
            borderSide: const BorderSide(color: _cardStroke),
          ),
          focusedBorder: const OutlineInputBorder(
            borderRadius: BorderRadius.all(Radius.circular(24)),
            borderSide: BorderSide(color: _blue, width: 2),
          ),
        ),
        onSubmitted: (_) {},
      ),
    );
  }
}

// ===================================================================
// Widgets auxiliares
// ===================================================================

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final Color iconBg;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _ActionCard({
    required this.icon,
    required this.iconBg,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  static const _stroke = Color(0xFFE6EBF0);
  static const _textPrimary = AppTheme.textPrimary;
  static const _textSecondary = AppTheme.textSecondary;
  static const _accent = Color(0xFF0A84FF);

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(20),
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: _stroke),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 36, height: 36,
                decoration: BoxDecoration(
                  color: iconBg, borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(icon, size: 20, color: _accent),
              ),
              const SizedBox(height: 14),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 16, fontWeight: FontWeight.w800, height: 1.15, color: _textPrimary,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                subtitle,
                style: const TextStyle(fontSize: 12, color: _textSecondary, height: 1.35),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _UpcomingClass {
  final String title;
  final String timeRange;
  final int students;
  final Color statusColor;
  const _UpcomingClass({
    required this.title,
    required this.timeRange,
    required this.students,
    required this.statusColor,
  });
}

class _UpcomingTile extends StatelessWidget {
  final _UpcomingClass data;
  final VoidCallback onTake;

  const _UpcomingTile({required this.data, required this.onTake});

  static const _stroke = Color(0xFFE6EBF0);
  static const _chipBg = Color(0xFFE7F5EC);
  static const _chipFg = Color(0xFF16A34A); // verde texto

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: _stroke),
        ),
        child: Row(
          children: [
            Container(
              width: 10, height: 10,
              decoration: BoxDecoration(color: data.statusColor, shape: BoxShape.circle),
            ),
            const SizedBox(width: 10),

            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    data.title,
                    style: const TextStyle(
                      fontSize: 15, fontWeight: FontWeight.w700, color: AppTheme.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      const Icon(Icons.access_time, size: 14, color: AppTheme.textSecondary),
                      const SizedBox(width: 4),
                      Text(
                        '${data.timeRange}  •  ${data.students} alumnos',
                        style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            TextButton(
              onPressed: onTake,
              style: TextButton.styleFrom(
                backgroundColor: _chipBg,
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
              ),
              child: const Text(
                'Tomar',
                style: TextStyle(color: _chipFg, fontWeight: FontWeight.w700),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Bottom bar personalizada con "pill" azul
class AulatapBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;
  final Color activeColor;

  const AulatapBottomNav({
    super.key,
    required this.currentIndex,
    required this.onTap,
    this.activeColor = const Color(0xFF0A84FF),
  });

  @override
  Widget build(BuildContext context) {
    final items = const [
      _NavItemData(icon: Icons.home_rounded, label: 'Inicio'),
      _NavItemData(icon: Icons.nfc, label: 'NFC'),
      _NavItemData(icon: Icons.schedule_outlined, label: 'Historial'),
      _NavItemData(icon: Icons.tune_rounded, label: 'Ajustes'),
    ];

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.06), // <- reemplazo de withOpacity
            blurRadius: 12,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          height: 72,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: List.generate(items.length, (i) {
              final it = items[i];
              final selected = i == currentIndex;
              return _NavItem(
                data: it,
                selected: selected,
                activeColor: activeColor,
                onTap: () => onTap(i),
              );
            }),
          ),
        ),
      ),
    );
  }
}

class _NavItemData {
  final IconData icon;
  final String label;
  const _NavItemData({required this.icon, required this.label});
}

class _NavItem extends StatelessWidget {
  final _NavItemData data;
  final bool selected;
  final VoidCallback onTap;
  final Color activeColor;

  const _NavItem({
    required this.data,
    required this.selected,
    required this.onTap,
    required this.activeColor,
  });

  @override
  Widget build(BuildContext context) {
    final fg = selected ? Colors.white : AppTheme.textSecondary;
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: selected ? activeColor : Colors.transparent,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(data.icon, color: fg),
            const SizedBox(height: 4),
            Text(
              data.label,
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: fg,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
