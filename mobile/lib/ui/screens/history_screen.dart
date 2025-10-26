// lib/ui/screens/history_screen.dart
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import '../../core/app_router.dart';

// Colores usados antes
const kBlue     = Color(0xFF0A84FF);
const kStroke   = Color(0xFFE6EBF0);
const kMint     = Color(0xFFE7F5EC);
const kMintDeep = Color(0xFF16A34A);

// Celestes del bloque de filtros (coinciden con el look)
const kPanelBg  = Colors.white;
const kChipBg   = Color(0xFFEFF6F9);

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

enum HistoryFilter { all, week, byCourse }

class _HistoryScreenState extends State<HistoryScreen> {
  final TextEditingController _search = TextEditingController();
  HistoryFilter _filter = HistoryFilter.all;

  // Mock de sesiones (usa DateTime para filtrar “Esta semana”)
  final List<_Session> _sessions = [
    _Session(
      course: 'Matemática I',
      date: DateTime.now().subtract(const Duration(days: 1)),
      dateLabel: 'Mar 12',
      timeRange: '08:00 - 09:30',
      present: 26, total: 28, courseCode: 'Mat I',
    ),
    _Session(
      course: 'Historia',
      date: DateTime.now().subtract(const Duration(days: 2)),
      dateLabel: 'Mar 11',
      timeRange: '10:00 - 11:30',
      present: 26, total: 31, courseCode: 'Hist',
    ),
    _Session(
      course: 'Química',
      date: DateTime.now().subtract(const Duration(days: 3)),
      dateLabel: 'Mar 10',
      timeRange: '12:00 - 13:30',
      present: 24, total: 27, courseCode: 'Quím',
    ),
  ];

  // Mock de detalle reciente
  final List<_Recent> _recents = const [
    _Recent(name: 'María López', badge: 'Mat I', statusText: null, absent: false),
    _Recent(name: 'Juan Pérez',  badge: null,    statusText: 'Ausente', absent: true),
  ];

  List<_Session> get _visibleSessions {
    final q = _search.text.trim().toLowerCase();
    Iterable<_Session> items = _sessions;

    // Filtro por texto (curso o fecha)
    if (q.isNotEmpty) {
      items = items.where((s) =>
      s.course.toLowerCase().contains(q) ||
          s.dateLabel.toLowerCase().contains(q));
    }

    // Filtros por chips
    switch (_filter) {
      case HistoryFilter.week:
        final now = DateTime.now();
        final sevenDaysAgo = now.subtract(const Duration(days: 7));
        items = items.where((s) => s.date.isAfter(sevenDaysAgo));
        items = items.toList()..sort((a, b) => b.date.compareTo(a.date));
        break;
      case HistoryFilter.byCourse:
        final list = items.toList()..sort((a, b) => a.course.compareTo(b.course));
        items = list;
        break;
      case HistoryFilter.all:
        items = items.toList()..sort((a, b) => b.date.compareTo(a.date));
        break;
    }

    return items.toList();
  }

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // Header
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
                child: Row(
                  children: [
                    const Expanded(
                      child: Text(
                        'AulaTap',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.w800,
                          color: AppTheme.textPrimary,
                        ),
                      ),
                    ),
                    InkWell(
                      borderRadius: BorderRadius.circular(20),
                      onTap: () {},
                      child: Row(
                        children: const [
                          CircleAvatar(
                            radius: 16,
                            backgroundImage: AssetImage('assets/images/avatar_sample.jpg'),
                          ),
                          SizedBox(width: 4),
                          Icon(Icons.expand_more, size: 18, color: AppTheme.textPrimary),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Buscador
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: TextField(
                  controller: _search,
                  onChanged: (_) => setState(() {}),
                  decoration: InputDecoration(
                    hintText: 'Buscar por curso o fecha',
                    hintStyle: TextStyle(color: Colors.grey[600], fontSize: 14),
                    prefixIcon: const Icon(Icons.search, size: 20),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                    filled: true,
                    fillColor: Colors.white,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(24),
                      borderSide: const BorderSide(color: kStroke),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(24),
                      borderSide: const BorderSide(color: kStroke),
                    ),
                    focusedBorder: const OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(24)),
                      borderSide: BorderSide(color: kBlue, width: 2),
                    ),
                  ),
                ),
              ),
            ),

            // Panel de filtros + título
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
                child: Container(
                  decoration: BoxDecoration(
                    color: kPanelBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: kStroke),
                  ),
                  child: Column(
                    children: [
                      Padding(
                        padding: const EdgeInsets.fromLTRB(14, 12, 14, 10),
                        child: Row(
                          children: const [
                            Expanded(
                              child: Text(
                                'Historial de clases',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w800,
                                  color: AppTheme.textPrimary,
                                ),
                              ),
                            ),
                            Text(
                              'Últimos 30 días',
                              style: TextStyle(
                                color: AppTheme.textSecondary,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.fromLTRB(12, 0, 12, 12),
                        child: Row(
                          children: [
                            _FilterChipPill(
                              text: 'Todos',
                              selected: _filter == HistoryFilter.all,
                              onTap: () => setState(() => _filter = HistoryFilter.all),
                            ),
                            const SizedBox(width: 8),
                            _FilterChipPill(
                              text: 'Esta semana',
                              selected: _filter == HistoryFilter.week,
                              onTap: () => setState(() => _filter = HistoryFilter.week),
                            ),
                            const SizedBox(width: 8),
                            _FilterChipPill(
                              text: 'Por curso',
                              selected: _filter == HistoryFilter.byCourse,
                              onTap: () => setState(() => _filter = HistoryFilter.byCourse),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // Lista de sesiones
            SliverList.builder(
              itemBuilder: (ctx, i) {
                final s = _visibleSessions[i];
                return Padding(
                  padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                  child: _SessionItem(
                    session: s,
                    onView: () {
                      Navigator.pushNamed(
                        context,
                        AppRouter.classHistory,
                        arguments: {
                          'course': s.course,
                          'dateLabel': s.dateLabel,
                          'timeRange': s.timeRange,
                          'present': s.present,
                          'total': s.total,
                        },
                      );
                    },
                  ),
                );
              },
              itemCount: _visibleSessions.length,
            ),

            // Detalle reciente
            const SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.fromLTRB(16, 14, 16, 8),
                child: Text(
                  'Detalle reciente',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                    color: AppTheme.textPrimary,
                  ),
                ),
              ),
            ),
            SliverList.builder(
              itemBuilder: (ctx, i) => Padding(
                padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                child: _RecentTile(item: _recents[i]),
              ),
              itemCount: _recents.length,
            ),

            const SliverToBoxAdapter(child: SizedBox(height: 90)),
          ],
        ),
      ),

      // Bottom nav
      bottomNavigationBar: _AulatapBottomNav(
        currentIndex: 2,
        onTap: (i) {
          switch (i) {
            case 0: Navigator.pushReplacementNamed(context, AppRouter.home); break;
            case 1: Navigator.pushReplacementNamed(context, AppRouter.nfc); break;
            case 2: break;
            case 3: Navigator.pushReplacementNamed(context, AppRouter.settings); break;
          }
        },
      ),
    );
  }
}

// ===================== Widgets auxiliares =====================

class _FilterChipPill extends StatelessWidget {
  final String text;
  final bool selected;
  final VoidCallback onTap;
  const _FilterChipPill({
    required this.text,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(18),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: selected ? kMint : kChipBg,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(
            // reemplazo de withOpacity(.2)
            color: selected ? kMintDeep.withValues(alpha: 0.2) : kStroke,
          ),
        ),
        child: Text(
          text,
          style: TextStyle(
            fontWeight: FontWeight.w700,
            color: selected ? kMintDeep : AppTheme.textPrimary,
          ),
        ),
      ),
    );
  }
}

class _SessionItem extends StatelessWidget {
  final _Session session;
  final VoidCallback onView;
  const _SessionItem({required this.session, required this.onView});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(14, 12, 12, 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: kStroke),
      ),
      child: Row(
        children: [
          // Punto estado
          Container(
            width: 10, height: 10,
            decoration: const BoxDecoration(color: kMintDeep, shape: BoxShape.circle),
          ),
          const SizedBox(width: 10),

          // Texto
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${session.course} • ${session.dateLabel}',
                    style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      color: AppTheme.textPrimary,
                    )),
                const SizedBox(height: 4),
                Text('${session.timeRange} • ${session.present}/${session.total} presentes',
                    style: const TextStyle(
                      fontSize: 12,
                      color: AppTheme.textSecondary,
                    )),
              ],
            ),
          ),

          // Botón Ver
          TextButton(
            onPressed: onView,
            style: TextButton.styleFrom(
              backgroundColor: kMint,
              foregroundColor: kMintDeep,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            ),
            child: const Text('Ver', style: TextStyle(fontWeight: FontWeight.w700)),
          ),
        ],
      ),
    );
  }
}

class _RecentTile extends StatelessWidget {
  final _Recent item;
  const _RecentTile({required this.item});

  @override
  Widget build(BuildContext context) {
    final trailing = item.absent
        ? Container(
      width: 26, height: 26,
      decoration: BoxDecoration(
        color: const Color(0xFFFFF3CD),
        borderRadius: BorderRadius.circular(13),
      ),
      child: const Icon(Icons.remove, size: 18, color: Color(0xFFB58900)),
    )
        : Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: kMint,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Text(
        item.badge ?? '',
        style: const TextStyle(
          color: kMintDeep,
          fontWeight: FontWeight.w700,
        ),
      ),
    );

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: kStroke),
      ),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 18,
            backgroundImage: AssetImage('assets/images/avatar_sample.jpg'),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              item.name + (item.absent ? '   Ausente' : ''),
              overflow: TextOverflow.ellipsis,
              style: TextStyle(
                fontWeight: item.absent ? FontWeight.w600 : FontWeight.w700,
                color: item.absent ? AppTheme.textSecondary : AppTheme.textPrimary,
              ),
            ),
          ),
          trailing,
        ],
      ),
    );
  }
}

// ====== Bottom Nav minimal ======
class _AulatapBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;
  const _AulatapBottomNav({
    required this.currentIndex,
    required this.onTap,
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
            // reemplazo de withOpacity(.06)
            color: Colors.black.withValues(alpha: 0.06),
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
              final fg = selected ? Colors.white : AppTheme.textSecondary;
              return InkWell(
                onTap: () => onTap(i),
                borderRadius: BorderRadius.circular(16),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 180),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: selected ? kBlue : Colors.transparent,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(it.icon, color: fg),
                      const SizedBox(height: 4),
                      Text(it.label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: fg)),
                    ],
                  ),
                ),
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

// ===================== Modelos =====================
class _Session {
  final String course;
  final DateTime date;
  final String dateLabel; // p.ej. "Mar 12"
  final String timeRange;
  final int present;
  final int total;
  final String courseCode;

  const _Session({
    required this.course,
    required this.date,
    required this.dateLabel,
    required this.timeRange,
    required this.present,
    required this.total,
    required this.courseCode,
  });
}

class _Recent {
  final String name;
  final String? badge;      // ej. "Mat I"
  final String? statusText; // ej. "Ausente" (solo informativo)
  final bool absent;

  const _Recent({
    required this.name,
    required this.badge,
    required this.statusText,
    required this.absent,
  });
}
