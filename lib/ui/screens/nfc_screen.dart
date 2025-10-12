// lib/ui/screens/nfc_screen.dart
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:nfc_manager/nfc_manager.dart';
import '../../core/app_theme.dart';
import '../../core/app_router.dart';

const kBlue = Color(0xFF0A84FF);
const kStroke = Color(0xFFE6EBF0);
const kMint = Color(0xFFE7F5EC);
const kMintDeep = Color(0xFF16A34A);
const kIconMint = Color(0xFFEAF6EF);

class NfcScreen extends StatefulWidget {
  const NfcScreen({super.key});
  @override
  State<NfcScreen> createState() => _NfcScreenState();
}

class _NfcScreenState extends State<NfcScreen> {
  final TextEditingController _search = TextEditingController();

  final List<ClassItem> _classes = [
    ClassItem(title: 'Matemática I', room: 'Aula 204', start: '08:00', end: '09:30'),
    ClassItem(title: 'Historia', room: 'Sala 3', start: '10:00', end: '11:30'),
    ClassItem(title: 'Física II', room: 'Lab 2', start: '13:00', end: '14:30'),
  ];
  int _selectedIndex = 0;

  bool _isScanning = false;
  final List<NfcRecord> _records = [];

  @override
  void dispose() {
    _search.dispose();
    if (_isScanning) NfcManager.instance.stopSession();
    super.dispose();
  }

  Future<void> _startScan() async {
    final availability = await NfcManager.instance.checkAvailability();
    if (availability != NfcAvailability.enabled) {
      _snack('NFC no disponible o desactivado');
      return;
    }
    setState(() => _isScanning = true);

    await NfcManager.instance.startSession(
      pollingOptions: {
        NfcPollingOption.iso14443,
        NfcPollingOption.iso15693,
        NfcPollingOption.iso18092,
      },
      onDiscovered: (NfcTag tag) async {
        final uid = _extractIdentifier(tag) ?? 'desconocido';
        final now = TimeOfDay.now();
        final cls = _classes[_selectedIndex];

        setState(() {
          _records.insert(
            0,
            NfcRecord(
              displayName: 'UID $uid',
              classTitle: cls.title,
              timeLabel:
              '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}',
              statusOk: true,
            ),
          );
        });
      },
    );
  }

  Future<void> _stopScan() async {
    try {
      await NfcManager.instance.stopSession();
    } finally {
      setState(() => _isScanning = false);
    }
  }

  /// Extrae el `identifier` buscando en el mapa `tag.data` (sin tech-classes).
  String? _extractIdentifier(NfcTag tag) {
    // ignore: invalid_use_of_protected_member
    final raw = tag.data; // Map anidado con la info del tag
    if (raw is! Map) return null;

    Uint8List? walk(Object? node) {
      if (node is Map) {
        for (final e in node.entries) {
          final k = e.key;
          final v = e.value;
          if (k == 'identifier' && v is Uint8List) return v;
          final nested = walk(v);
          if (nested != null) return nested;
        }
      }
      return null;
    }

    final idBytes = walk(raw);
    if (idBytes == null) return null;
    return idBytes
        .map((b) => b.toRadixString(16).padLeft(2, '0'))
        .join(':')
        .toUpperCase();
  }

  void _snack(String msg) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));

  void _openChangeClassSheet() async {
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) => _ChangeClassSheet(
        classes: _classes,
        selectedIndex: _selectedIndex,
        onSelect: (i) => setState(() => _selectedIndex = i),
        onDelete: (i) => setState(() {
          if (_classes.length == 1) return;
          if (i <= _selectedIndex) {
            _selectedIndex = (_selectedIndex - 1).clamp(0, _classes.length - 2);
          }
          _classes.removeAt(i);
        }),
        onAdd: (item) => setState(() {
          _classes.add(item);
          _selectedIndex = _classes.length - 1;
        }),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final cls = _classes[_selectedIndex];

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
                  decoration: InputDecoration(
                    hintText: 'Buscar clase, grupo o alumno',
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

            // Card de escaneo
            SliverToBoxAdapter(
              child: Padding(
                padding:
                const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: Container(
                  padding: const EdgeInsets.fromLTRB(16, 20, 16, 16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(28),
                    border: Border.all(color: kStroke),
                  ),
                  child: Column(
                    children: [
                      // Ilustración
                      SizedBox(
                        height: 160,
                        child: Stack(
                          alignment: Alignment.center,
                          children: [
                            Positioned(
                              child: Container(
                                width: 148,
                                height: 104,
                                decoration: BoxDecoration(
                                  color: kIconMint,
                                  borderRadius: BorderRadius.circular(22),
                                ),
                              ),
                            ),
                            Container(
                              width: 146,
                              height: 146,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: kMintDeep.withValues(alpha: 0.15),
                                  width: 8,
                                ),
                              ),
                            ),
                            Container(
                              width: 104,
                              height: 104,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: kMintDeep.withValues(alpha: 0.25),
                                  width: 8,
                                ),
                              ),
                            ),
                            Container(
                              width: 66,
                              height: 66,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: kMintDeep.withValues(alpha: 0.35),
                                  width: 8,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 10),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: const [
                          Icon(Icons.podcasts_rounded,
                              size: 18, color: AppTheme.textSecondary),
                          SizedBox(width: 6),
                          Text(
                            'Escaneo NFC en progreso',
                            style: TextStyle(
                                fontWeight: FontWeight.w700,
                                color: AppTheme.textPrimary),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Mantenga el carnet cerca del dispositivo',
                        style: TextStyle(
                            color: AppTheme.textSecondary, fontSize: 12),
                      ),

                      const SizedBox(height: 16),

                      // Chips: clase y horario
                      Row(
                        children: [
                          Expanded(
                            child: _ChipStroke(
                              leading: Icons.menu_book_rounded,
                              labelTop: '${cls.title} • ${cls.room}',
                              labelBottom: null,
                            ),
                          ),
                          const SizedBox(width: 8),
                          _TimePill(text: '${cls.start} - ${cls.end}'),
                        ],
                      ),

                      const SizedBox(height: 12),

                      // Botón Cambiar clase
                      SizedBox(
                        width: double.infinity,
                        child: TextButton.icon(
                          onPressed: _openChangeClassSheet,
                          icon: const Icon(Icons.cached_rounded),
                          label: const Text('Cambiar clase',
                              style: TextStyle(fontWeight: FontWeight.w700)),
                          style: TextButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            backgroundColor: kMint,
                            foregroundColor: kMintDeep,
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(28)),
                          ),
                        ),
                      ),
                      const SizedBox(height: 10),

                      // Botón principal
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: _isScanning ? _stopScan : _startScan,
                          icon: const Icon(Icons.wifi_tethering),
                          label: Text(_isScanning
                              ? 'Detener escaneo'
                              : 'Iniciar escaneo'),
                          style: ElevatedButton.styleFrom(
                            padding:
                            const EdgeInsets.symmetric(vertical: 16),
                            backgroundColor: kBlue,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(28)),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // Últimos registros
            const SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.fromLTRB(16, 14, 16, 8),
                child: Text(
                  'Últimos registros',
                  style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: AppTheme.textPrimary),
                ),
              ),
            ),
            SliverList(
              delegate: SliverChildBuilderDelegate(
                    (ctx, i) => Padding(
                  padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
                  child: _RecordTile(record: _records[i]),
                ),
                childCount: _records.length,
              ),
            ),
            const SliverToBoxAdapter(child: SizedBox(height: 90)),
          ],
        ),
      ),

      bottomNavigationBar: AulatapBottomNav(
        currentIndex: 1,
        onTap: (i) {
          switch (i) {
            case 0:
              Navigator.pushReplacementNamed(context, AppRouter.home);
              break;
            case 1:
              break;
            case 2:
              Navigator.pushReplacementNamed(context, AppRouter.history);
              break;
            case 3:
              Navigator.pushReplacementNamed(context, AppRouter.settings);
              break;
          }
        },
      ),
    );
  }
}

// ====== UI helpers ======
class _ChipStroke extends StatelessWidget {
  final IconData leading;
  final String labelTop;
  final String? labelBottom;
  const _ChipStroke({required this.leading, required this.labelTop, this.labelBottom});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: kStroke),
      ),
      child: Row(
        children: [
          Icon(leading, size: 18, color: AppTheme.textPrimary),
          const SizedBox(width: 8),
          Expanded(
            child: (labelBottom == null)
                ? Text(
              labelTop,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontWeight: FontWeight.w700,
                color: AppTheme.textPrimary,
                height: 1.15,
              ),
            )
                : Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  labelTop,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    fontWeight: FontWeight.w700,
                    color: AppTheme.textPrimary,
                    height: 1.1,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  labelBottom!,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                      fontSize: 12, color: AppTheme.textSecondary),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _TimePill extends StatelessWidget {
  final String text;
  const _TimePill({required this.text});
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: kMint,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Text(
        text,
        style: const TextStyle(
          fontWeight: FontWeight.w700,
          color: kMintDeep,
        ),
      ),
    );
  }
}

class _RecordTile extends StatelessWidget {
  final NfcRecord record;
  const _RecordTile({required this.record});
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
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
                Text(
                  record.displayName,
                  style: const TextStyle(
                    fontWeight: FontWeight.w700,
                    color: AppTheme.textPrimary,
                  ),
                ),
                const SizedBox(height: 2),
                Row(
                  children: [
                    Text(
                      record.classTitle,
                      style: const TextStyle(
                          fontSize: 12, color: AppTheme.textSecondary),
                    ),
                    const SizedBox(width: 6),
                    const Icon(Icons.brightness_1,
                        size: 4, color: AppTheme.textSecondary),
                    const SizedBox(width: 6),
                    Text(
                      record.timeLabel,
                      style: const TextStyle(
                          fontSize: 12, color: AppTheme.textSecondary),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: kMint,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Text(
              record.statusOk ? 'OK' : 'ERR',
              style: TextStyle(
                color: record.statusOk ? kMintDeep : Colors.red,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ====== Bottom nav ======
class AulatapBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;
  final Color activeColor;
  const AulatapBottomNav({
    super.key,
    required this.currentIndex,
    required this.onTap,
    this.activeColor = kBlue,
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
                  fontSize: 12, fontWeight: FontWeight.w600, color: fg),
            ),
          ],
        ),
      ),
    );
  }
}

// ====== Modelos ======
class ClassItem {
  final String title;
  final String room;
  final String start;
  final String end;
  ClassItem({required this.title, required this.room, required this.start, required this.end});
}

class NfcRecord {
  final String displayName;
  final String classTitle;
  final String timeLabel;
  final bool statusOk;
  NfcRecord({required this.displayName, required this.classTitle, required this.timeLabel, required this.statusOk});
}

// ====== Sheet elegir/agregar/eliminar clase ======
class _ChangeClassSheet extends StatefulWidget {
  final List<ClassItem> classes;
  final int selectedIndex;
  final ValueChanged<int> onSelect;
  final ValueChanged<int> onDelete;
  final ValueChanged<ClassItem> onAdd;
  const _ChangeClassSheet({
    required this.classes,
    required this.selectedIndex,
    required this.onSelect,
    required this.onDelete,
    required this.onAdd,
  });

  @override
  State<_ChangeClassSheet> createState() => _ChangeClassSheetState();
}

class _ChangeClassSheetState extends State<_ChangeClassSheet> {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(height: 12),
          Container(
            width: 44,
            height: 4,
            decoration: BoxDecoration(
              color: Colors.black12,
              borderRadius: BorderRadius.circular(4),
            ),
          ),
          const SizedBox(height: 10),
          const Text('Seleccionar clase',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
          const SizedBox(height: 6),
          Flexible(
            child: ListView.separated(
              shrinkWrap: true,
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
              itemCount: widget.classes.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (ctx, i) {
                final c = widget.classes[i];
                final sel = i == widget.selectedIndex;
                return Container(
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(
                      color: sel ? kBlue : kStroke,
                      width: sel ? 2 : 1,
                    ),
                  ),
                  child: ListTile(
                    leading: const Icon(Icons.menu_book_rounded),
                    title: Text('${c.title} • ${c.room}',
                        style: const TextStyle(fontWeight: FontWeight.w700)),
                    subtitle: Text('${c.start} - ${c.end}'),
                    onTap: () {
                      widget.onSelect(i);
                      Navigator.pop(context);
                    },
                    trailing: IconButton(
                      icon:
                      const Icon(Icons.delete_outline, color: Colors.red),
                      onPressed: () =>
                          setState(() => widget.onDelete(i)),
                      tooltip: 'Eliminar',
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 6),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () async {
                  final newItem = await showDialog<ClassItem>(
                    context: context,
                    builder: (_) => const _AddClassDialog(),
                  );
                  if (newItem != null) widget.onAdd(newItem);
                },
                icon: const Icon(Icons.add),
                label: const Text('Agregar clase',
                    style: TextStyle(fontWeight: FontWeight.w700)),
                style: OutlinedButton.styleFrom(
                  foregroundColor: kBlue,
                  side: const BorderSide(color: kBlue),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14)),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _AddClassDialog extends StatefulWidget {
  const _AddClassDialog();
  @override
  State<_AddClassDialog> createState() => _AddClassDialogState();
}

class _AddClassDialogState extends State<_AddClassDialog> {
  final _form = GlobalKey<FormState>();
  final _title = TextEditingController();
  final _room = TextEditingController();
  final _start = TextEditingController();
  final _end = TextEditingController();

  @override
  void dispose() {
    _title.dispose();
    _room.dispose();
    _start.dispose();
    _end.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Nueva clase'),
      content: Form(
        key: _form,
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          TextFormField(
            controller: _title,
            decoration: const InputDecoration(
                labelText: 'Nombre (p.ej., Matemática I)'),
            validator: (v) => v == null || v.isEmpty ? 'Requerido' : null,
          ),
          TextFormField(
              controller: _room,
              decoration: const InputDecoration(labelText: 'Aula/Sala')),
          Row(children: [
            Expanded(
              child: TextFormField(
                  controller: _start,
                  decoration:
                  const InputDecoration(labelText: 'Inicio (HH:MM)')),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: TextFormField(
                  controller: _end,
                  decoration:
                  const InputDecoration(labelText: 'Fin (HH:MM)')),
            ),
          ]),
        ]),
      ),
      actions: [
        TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () {
            if (_form.currentState?.validate() != true) return;
            Navigator.pop(
              context,
              ClassItem(
                title: _title.text.trim(),
                room: _room.text.trim(),
                start: _start.text.trim(),
                end: _end.text.trim(),
              ),
            );
          },
          child: const Text('Guardar'),
        ),
      ],
    );
  }
}
