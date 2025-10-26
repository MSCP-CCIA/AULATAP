import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../core/app_theme.dart';
import '../../core/app_router.dart';
import '../../core/navigation_utils.dart';

/// Paleta consistente
const kBlue       = Color(0xFF0A84FF);
const kStroke     = Color(0xFFE6EBF0);
const kMint       = Color(0xFFE7F5EC);
const kMintDeep   = Color(0xFF16A34A);

/// Keys de preferencias
const _kNotif     = 'pref.notifications';
const _kAutoNfc   = 'pref.auto_nfc';
const _kBiometric = 'pref.require_biometric';
const _kTheme     = 'pref.theme_mode';          // system | light | dark
const _kName      = 'profile.display_name';
const _kEmail     = 'profile.email';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  // Estado de preferencias
  bool _notifications = true;
  bool _autoNfc = false;
  bool _requireBiometric = true;
  String _themeMode = 'system'; // system | light | dark

  String _displayName = 'Prof. Carla Gómez';
  String _email       = 'c.gomez@instituto.edu';
  final int _assignedCourses = 6; // <- puede ser final

  bool _loading = true;
  bool _saving  = false;

  @override
  void initState() {
    super.initState();
    _loadPrefs();
  }

  Future<void> _loadPrefs() async {
    final sp = await SharedPreferences.getInstance();
    setState(() {
      _notifications    = sp.getBool(_kNotif)     ?? true;
      _autoNfc          = sp.getBool(_kAutoNfc)   ?? false;
      _requireBiometric = sp.getBool(_kBiometric) ?? true;
      _themeMode        = sp.getString(_kTheme)   ?? 'system';
      _displayName      = sp.getString(_kName)    ?? _displayName;
      _email            = sp.getString(_kEmail)   ?? _email;
      _loading = false;
    });
  }

  Future<void> _savePrefs() async {
    setState(() => _saving = true);
    final sp = await SharedPreferences.getInstance();
    await sp.setBool(_kNotif, _notifications);
    await sp.setBool(_kAutoNfc, _autoNfc);
    await sp.setBool(_kBiometric, _requireBiometric);
    await sp.setString(_kTheme, _themeMode);
    await sp.setString(_kName, _displayName);
    await sp.setString(_kEmail, _email);
    setState(() => _saving = false);

    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Cambios guardados')),
    );
  }

  // ---------- Selector de tema sin Radios deprecados ----------
  void _pickTheme() async {
    final selected = await showModalBottomSheet<String>(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(18)),
      ),
      builder: (ctx) {
        String temp = _themeMode;
        return StatefulBuilder(
          builder: (ctx, setSB) => Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 44, height: 4,
                  decoration: BoxDecoration(
                    color: Colors.black.withValues(alpha: .10),
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                const SizedBox(height: 10),
                const Text('Elegir tema',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),

                const SizedBox(height: 12),
                SegmentedButton<String>(
                  segments: const [
                    ButtonSegment<String>(
                      value: 'system',
                      label: Text('Sistema'),
                      icon: Icon(Icons.settings_suggest_outlined),
                    ),
                    ButtonSegment<String>(
                      value: 'light',
                      label: Text('Claro'),
                      icon: Icon(Icons.light_mode_outlined),
                    ),
                    ButtonSegment<String>(
                      value: 'dark',
                      label: Text('Oscuro'),
                      icon: Icon(Icons.dark_mode_outlined),
                    ),
                  ],
                  selected: {temp},
                  onSelectionChanged: (set) => setSB(() => temp = set.first),
                  showSelectedIcon: false,
                ),

                const SizedBox(height: 14),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => Navigator.pop(ctx, temp),
                    child: const Text('Aplicar'),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );

    if (selected != null && selected != _themeMode) {
      setState(() => _themeMode = selected);
    }
  }

  void _editProfile() async {
    final result = await showDialog<Map<String, String>>(
      context: context,
      builder: (_) => _EditProfileDialog(name: _displayName, email: _email),
    );
    if (result != null) {
      setState(() {
        _displayName = result['name']!.trim();
        _email = result['email']!.trim();
      });
    }
  }

  void _openDummy(String title) {
    Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => _DummyPage(title: title),
    ));
  }

  Future<void> _copyContact() async {
    await Clipboard.setData(const ClipboardData(text: 'soporte@aulatap.com'));
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Correo copiado: soporte@aulatap.com')),
    );
  }

  void _showTerms() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(18)),
      ),
      builder: (_) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 16),
        child: SingleChildScrollView(
          child: Column(
            children: const [
              SizedBox(height: 4),
              Text('Términos y privacidad',
                  style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
              SizedBox(height: 12),
              Text(
                'Aquí puedes enlazar tu documento real de Términos y Política de Privacidad.',
                style: TextStyle(color: AppTheme.textSecondary, height: 1.4),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _signOut() => Nav.goToClearingStack(context, AppRouter.login);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SafeArea(
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : CustomScrollView(
          slivers: [
            // Header
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
                child: Row(
                  children: [
                    const Expanded(
                      child: Text(
                        'Aulatap',
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

            // Título + badge
            const SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.fromLTRB(16, 12, 16, 10),
                child: _HeaderWithBadge(),
              ),
            ),

            // Perfil
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: _ProfileCard(
                  name: _displayName,
                  email: _email,
                  onEdit: _editProfile,
                ),
              ),
            ),

            // Preferencias
            const SliverToBoxAdapter(child: _SectionTitle('Preferencias')),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    _TileSwitch(
                      icon: Icons.notifications_none_rounded,
                      title: 'Notificaciones',
                      value: _notifications,
                      onChanged: (v) => setState(() => _notifications = v),
                    ),
                    const SizedBox(height: 10),
                    _TileSwitch(
                      icon: Icons.nfc,
                      title: 'NFC automático',
                      subtitle: 'Iniciar lectura al abrir la app',
                      value: _autoNfc,
                      onChanged: (v) => setState(() => _autoNfc = v),
                    ),
                    const SizedBox(height: 10),
                    _TileArrow(
                      icon: Icons.brightness_6_outlined,
                      title: 'Tema',
                      subtitle: _themeMode == 'system'
                          ? 'Usar sistema'
                          : (_themeMode == 'light' ? 'Claro' : 'Oscuro'),
                      onTap: _pickTheme,
                    ),
                  ],
                ),
              ),
            ),

            // Institución
            const SliverToBoxAdapter(child: _SectionTitle('Institución')),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    _TileArrow(
                      icon: Icons.lock_outline,
                      title: 'Cursos asignados',
                      subtitle: '$_assignedCourses cursos activos',
                      onTap: () => _openDummy('Cursos asignados'),
                    ),
                    const SizedBox(height: 10),
                    _TileArrow(
                      icon: Icons.list_alt_outlined,
                      title: 'Listas de estudiantes',
                      subtitle: 'Sincronizadas',
                      onTap: () => _openDummy('Listas de estudiantes'),
                    ),
                  ],
                ),
              ),
            ),

            // Seguridad
            const SliverToBoxAdapter(child: _SectionTitle('Seguridad')),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    _TileSwitch(
                      icon: Icons.verified_user_outlined,
                      title: 'Requerir biometría',
                      subtitle: 'Face/Touch ID para tomar asistencia',
                      value: _requireBiometric,
                      onChanged: (v) => setState(() => _requireBiometric = v),
                    ),
                    const SizedBox(height: 10),
                    _TileArrow(
                      icon: Icons.password_outlined,
                      title: 'Cambiar contraseña',
                      onTap: () => _openDummy('Cambiar contraseña'),
                    ),
                  ],
                ),
              ),
            ),

            // Soporte
            const SliverToBoxAdapter(child: _SectionTitle('Soporte')),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    _TileArrow(
                      icon: Icons.help_center_outlined,
                      title: 'Centro de ayuda',
                      onTap: () => _openDummy('Centro de ayuda'),
                    ),
                    const SizedBox(height: 10),
                    _TileArrow(
                      icon: Icons.alternate_email_outlined,
                      title: 'Contacto',
                      subtitle: 'soporte@aulatap.com',
                      onTap: _copyContact,
                    ),
                  ],
                ),
              ),
            ),

            // Versión + términos
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 110),
                child: Center(
                  child: Wrap(
                    alignment: WrapAlignment.center,
                    crossAxisAlignment: WrapCrossAlignment.center,
                    spacing: 8,
                    children: [
                      const Text('Versión 1.0.0',
                          style: TextStyle(color: AppTheme.textSecondary)),
                      const Text('•',
                          style: TextStyle(color: AppTheme.textSecondary)),
                      InkWell(
                        onTap: _showTerms,
                        borderRadius: BorderRadius.circular(4),
                        child: const Padding(
                          padding:
                          EdgeInsets.symmetric(horizontal: 4, vertical: 2),
                          child: Text('Términos y privacidad',
                              style: TextStyle(
                                  color: kBlue,
                                  fontWeight: FontWeight.w600)),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),

      // Botonera + bottom nav
      bottomNavigationBar: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            decoration: BoxDecoration(
              color: AppTheme.backgroundColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: .06),
                  blurRadius: 10,
                  offset: const Offset(0, -2),
                ),
              ],
            ),
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
            child: Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _signOut,
                    icon: const Icon(Icons.logout),
                    label: const Text('Cerrar sesión'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      foregroundColor: Colors.green.shade700,
                      side: BorderSide(color: Colors.green.shade600),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: _saving ? null : _savePrefs,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: kBlue,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: _saving
                        ? const SizedBox(
                      width: 20, height: 20,
                      child: CircularProgressIndicator(
                          strokeWidth: 2, color: Colors.white),
                    )
                        : const Text('Guardar cambios'),
                  ),
                ),
              ],
            ),
          ),
          _AulatapBottomNav(
            currentIndex: 3,
            onTap: (i) {
              switch (i) {
                case 0:
                  Navigator.pushReplacementNamed(context, AppRouter.home);
                  break;
                case 1:
                  Navigator.pushReplacementNamed(context, AppRouter.nfc);
                  break;
                case 2:
                  Navigator.pushReplacementNamed(context, AppRouter.history);
                  break;
                case 3:
                  break;
              }
            },
          ),
        ],
      ),
    );
  }
}

/// -------------------- Widgets reutilizables --------------------

class _HeaderWithBadge extends StatelessWidget {
  const _HeaderWithBadge();

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text('Ajustes',
            style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w800,
                color: AppTheme.textPrimary)),
        const SizedBox(width: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
          decoration: BoxDecoration(
            color: kMint,
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Text('Docente',
              style: TextStyle(
                  color: kMintDeep, fontWeight: FontWeight.w700, fontSize: 12)),
        ),
      ],
    );
  }
}

class _ProfileCard extends StatelessWidget {
  final String name;
  final String email;
  final VoidCallback onEdit;
  const _ProfileCard({required this.name, required this.email, required this.onEdit});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: kStroke),
      ),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 22,
            backgroundImage: AssetImage('assets/images/avatar_sample.jpg'),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(name,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        color: AppTheme.textPrimary)),
                const SizedBox(height: 2),
                Text(email,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                        fontSize: 12, color: AppTheme.textSecondary)),
              ],
            ),
          ),
          TextButton(
            onPressed: onEdit,
            style: TextButton.styleFrom(
              backgroundColor: const Color(0xFFF2F6FF),
              foregroundColor: kBlue,
              padding:
              const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20)),
            ),
            child: const Text('Editar',
                style: TextStyle(fontWeight: FontWeight.w700)),
          ),
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String text;
  const _SectionTitle(this.text);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 10),
      child: Text(
        text,
        style: const TextStyle(
          fontSize: 12,
          letterSpacing: .2,
          fontWeight: FontWeight.w700,
          color: AppTheme.textSecondary,
        ),
      ),
    );
  }
}

class _TileSwitch extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final bool value;
  final ValueChanged<bool> onChanged;

  const _TileSwitch({
    required this.icon,
    required this.title,
    this.subtitle,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding:
      const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: kStroke),
      ),
      child: Row(
        children: [
          _LeadingIcon(icon),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        color: AppTheme.textPrimary)),
                if (subtitle != null) ...[
                  const SizedBox(height: 2),
                  Text(subtitle!,
                      style: const TextStyle(
                          fontSize: 12, color: AppTheme.textSecondary)),
                ],
              ],
            ),
          ),
          Switch.adaptive(value: value, onChanged: onChanged),
        ],
      ),
    );
  }
}

class _TileArrow extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback onTap;

  const _TileArrow({
    required this.icon,
    required this.title,
    this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(16),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Container(
          padding:
          const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: kStroke),
          ),
          child: Row(
            children: [
              _LeadingIcon(icon),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title,
                        style: const TextStyle(
                            fontWeight: FontWeight.w700,
                            color: AppTheme.textPrimary)),
                    if (subtitle != null) ...[
                      const SizedBox(height: 2),
                      Text(subtitle!,
                          style: const TextStyle(
                              fontSize: 12, color: AppTheme.textSecondary)),
                    ],
                  ],
                ),
              ),
              const Icon(Icons.chevron_right,
                  color: AppTheme.textSecondary),
            ],
          ),
        ),
      ),
    );
  }
}

class _LeadingIcon extends StatelessWidget {
  final IconData icon;
  const _LeadingIcon(this.icon);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 34,
      height: 34,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: kStroke),
      ),
      child: Icon(icon, size: 18, color: AppTheme.textPrimary),
    );
  }
}

class _EditProfileDialog extends StatefulWidget {
  final String name;
  final String email;
  const _EditProfileDialog({required this.name, required this.email});

  @override
  State<_EditProfileDialog> createState() => _EditProfileDialogState();
}

class _EditProfileDialogState extends State<_EditProfileDialog> {
  late final TextEditingController _name =
  TextEditingController(text: widget.name);
  late final TextEditingController _email =
  TextEditingController(text: widget.email);
  final _form = GlobalKey<FormState>();

  @override
  void dispose() {
    _name.dispose();
    _email.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Editar perfil'),
      content: Form(
        key: _form,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextFormField(
              controller: _name,
              decoration: const InputDecoration(labelText: 'Nombre'),
              validator: (v) =>
              (v == null || v.trim().isEmpty) ? 'Requerido' : null,
            ),
            TextFormField(
              controller: _email,
              decoration: const InputDecoration(labelText: 'Correo'),
              keyboardType: TextInputType.emailAddress,
              validator: (v) {
                if (v == null || v.trim().isEmpty) return 'Requerido';
                if (!RegExp(r'^[^@]+@[^@]+\.[^@]+$').hasMatch(v.trim())) {
                  return 'Correo inválido';
                }
                return null;
              },
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar')),
        ElevatedButton(
          onPressed: () {
            if (_form.currentState?.validate() != true) return;
            Navigator.pop(
                context, {'name': _name.text, 'email': _email.text});
          },
          child: const Text('Guardar'),
        )
      ],
    );
  }
}

class _DummyPage extends StatelessWidget {
  final String title;
  const _DummyPage({required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: const Center(child: Text('Contenido en construcción')),
    );
  }
}

/// Bottom nav local (sin parámetro opcional activo para evitar warning)
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
                  padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: selected ? kBlue : Colors.transparent,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(it.icon, color: fg),
                      const SizedBox(height: 4),
                      Text(it.label,
                          style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: fg)),
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
