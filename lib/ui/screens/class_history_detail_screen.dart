import 'package:flutter/material.dart';
import '../../core/app_theme.dart';

const kBlue     = Color(0xFF0A84FF);
const kStroke   = Color(0xFFE6EBF0);
const kMint     = Color(0xFFE7F5EC);
const kMintDeep = Color(0xFF16A34A);

// Aviso/ausente
const kWarnBg   = Color(0xFFFFF3CD);
const kWarnText = Color(0xFFB58900);

class ClassHistoryDetailArgs {
  final String course;
  final String dateLabel;  // ej. "Mar 12"
  final String timeRange;  // ej. "08:00 - 09:30"
  final int present;
  final int total;

  const ClassHistoryDetailArgs({
    required this.course,
    required this.dateLabel,
    required this.timeRange,
    required this.present,
    required this.total,
  });

  factory ClassHistoryDetailArgs.fromMap(Map m) => ClassHistoryDetailArgs(
    course: m['course'] ?? 'Curso',
    dateLabel: m['dateLabel'] ?? 'Hoy',
    timeRange: m['timeRange'] ?? '--:--',
    present: m['present'] ?? 0,
    total: m['total'] ?? 0,
  );
}

class ClassHistoryDetailScreen extends StatefulWidget {
  const ClassHistoryDetailScreen({super.key});

  @override
  State<ClassHistoryDetailScreen> createState() =>
      _ClassHistoryDetailScreenState();
}

enum StudentFilter { all, present, absent }

class _ClassHistoryDetailScreenState extends State<ClassHistoryDetailScreen> {
  final _search = TextEditingController();
  StudentFilter _filter = StudentFilter.all;

  late final ClassHistoryDetailArgs _args;

  // Mock de alumnos (reemplaza con tu backend)
  final List<_StudentEntry> _students = [
    _StudentEntry('María López', true,  '08:05', 'Mat I'),
    _StudentEntry('Juan Pérez',  false, null,    'Mat I'),
    _StudentEntry('Camila Díaz', true,  '08:03', 'Mat I'),
    _StudentEntry('Luis Gómez',  true,  '08:12', 'Mat I'),
    _StudentEntry('Ana Torres',  false, null,    'Mat I'),
    _StudentEntry('Pedro Ruiz',  true,  '08:07', 'Mat I'),
  ];

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final a = ModalRoute.of(context)?.settings.arguments;
    if (a is ClassHistoryDetailArgs) {
      _args = a;
    } else if (a is Map) {
      _args = ClassHistoryDetailArgs.fromMap(a);
    } else {
      _args = const ClassHistoryDetailArgs(
        course: 'Matemática I',
        dateLabel: 'Mar 12',
        timeRange: '08:00 - 09:30',
        present: 26,
        total: 28,
      );
    }
  }

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  List<_StudentEntry> get _visible {
    final q = _search.text.trim().toLowerCase();
    Iterable<_StudentEntry> items = _students;

    if (_filter == StudentFilter.present) {
      items = items.where((e) => e.present);
    } else if (_filter == StudentFilter.absent) {
      items = items.where((e) => !e.present);
    }

    if (q.isNotEmpty) {
      items = items.where((e) => e.name.toLowerCase().contains(q));
    }

    return items.toList()..sort((a, b) => a.name.compareTo(b.name));
  }

  @override
  Widget build(BuildContext context) {
    final presentCount = _students.where((e) => e.present).length;
    final absentCount  = _students.length - presentCount;

    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // Header con back
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(8, 8, 16, 0),
                child: Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.arrow_back_rounded),
                      onPressed: () => Navigator.pop(context),
                    ),
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
                            backgroundImage:
                            AssetImage('assets/images/avatar_sample.jpg'),
                          ),
                          SizedBox(width: 4),
                          Icon(Icons.expand_more,
                              size: 18, color: AppTheme.textPrimary),
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
                    hintText: 'Buscar alumno',
                    hintStyle: TextStyle(color: Colors.grey[600], fontSize: 14),
                    prefixIcon: const Icon(Icons.search, size: 20),
                    contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 14),
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

            // Tarjeta resumen + Exportar
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
                child: Container(
                  padding: const EdgeInsets.fromLTRB(14, 12, 12, 12),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: kStroke),
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 34, height: 34,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: kStroke),
                        ),
                        child: const Icon(Icons.menu_book_rounded,
                            size: 18, color: AppTheme.textPrimary),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('${_args.course} • ${_args.dateLabel}',
                                style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                  color: AppTheme.textPrimary,
                                )),
                            const SizedBox(height: 4),
                            Text(
                              '${_args.timeRange} • ${_args.present}/${_args.total} presentes',
                              style: const TextStyle(
                                fontSize: 12,
                                color: AppTheme.textSecondary,
                              ),
                            ),
                          ],
                        ),
                      ),
                      TextButton.icon(
                        onPressed: _exportCsv,
                        icon: const Icon(Icons.download_rounded),
                        label: const Text('Exportar',
                            style: TextStyle(fontWeight: FontWeight.w700)),
                        style: TextButton.styleFrom(
                          backgroundColor: kMint,
                          foregroundColor: kMintDeep,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 12, vertical: 10),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(20),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // Filtros (Todos / Presentes / Ausentes)
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                child: Row(
                  children: [
                    _FilterPill(
                      text: 'Todos',
                      selected: _filter == StudentFilter.all,
                      onTap: () => setState(() => _filter = StudentFilter.all),
                    ),
                    const SizedBox(width: 8),
                    _FilterPill(
                      text: 'Presentes ($presentCount)',
                      selected: _filter == StudentFilter.present,
                      onTap: () =>
                          setState(() => _filter = StudentFilter.present),
                    ),
                    const SizedBox(width: 8),
                    _FilterPill(
                      text: 'Ausentes ($absentCount)',
                      selected: _filter == StudentFilter.absent,
                      onTap: () =>
                          setState(() => _filter = StudentFilter.absent),
                    ),
                  ],
                ),
              ),
            ),

            // Lista de alumnos
            SliverList.builder(
              itemBuilder: (ctx, i) {
                final e = _visible[i];
                return Padding(
                  padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                  child: _StudentTile(entry: e),
                );
              },
              itemCount: _visible.length,
            ),

            const SliverToBoxAdapter(child: SizedBox(height: 90)),
          ],
        ),
      ),
    );
  }

  void _exportCsv() {
    // Aquí podemos exportar los datos
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Exportación simulada (conecta tu backend).')),
    );
  }
}


class _FilterPill extends StatelessWidget {
  final String text;
  final bool selected;
  final VoidCallback onTap;
  const _FilterPill({
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
          color: selected ? kMint : const Color(0xFFEFF6F9),
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

class _StudentTile extends StatelessWidget {
  final _StudentEntry entry;
  const _StudentTile({required this.entry});

  @override
  Widget build(BuildContext context) {
    final trailing = entry.present
        ? Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: kMint,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Text(
        entry.time ?? 'OK',
        style: const TextStyle(
            color: kMintDeep, fontWeight: FontWeight.w700),
      ),
    )
        : Container(
      width: 26, height: 26,
      decoration: BoxDecoration(
        color: kWarnBg,
        borderRadius: BorderRadius.circular(13),
      ),
      child: const Icon(Icons.remove, size: 18, color: kWarnText),
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
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(entry.name,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        color: AppTheme.textPrimary)),
                const SizedBox(height: 2),
                Row(children: [
                  Text(entry.group,
                      style: const TextStyle(
                          fontSize: 12, color: AppTheme.textSecondary)),
                  const SizedBox(width: 6),
                  const Icon(Icons.brightness_1,
                      size: 4, color: AppTheme.textSecondary),
                  const SizedBox(width: 6),
                  Text(entry.present ? 'Presente' : 'Ausente',
                      style: const TextStyle(
                          fontSize: 12, color: AppTheme.textSecondary)),
                ]),
              ],
            ),
          ),
          trailing,
        ],
      ),
    );
  }
}

class _StudentEntry {
  final String name;
  final bool present;
  final String? time; // hora de lectura NFC si presente
  final String group; // p.ej. "Mat I"
  _StudentEntry(this.name, this.present, this.time, this.group);
}
