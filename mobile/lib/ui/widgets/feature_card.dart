import 'package:flutter/material.dart';
import '../../core/app_theme.dart';

class FeatureCard extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color? color;
  final bool isTablet;

  const FeatureCard({
    super.key,
    required this.icon,
    required this.text,
    this.color,
    this.isTablet = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: isTablet ? 24 : 20,
        vertical: isTablet ? 16 : 14,
      ),
      decoration: BoxDecoration(
        color: color ?? AppTheme.secondaryColor,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Icon(
            icon,
            color: AppTheme.accentColor,
            size: isTablet ? 26 : 22,
          ),
          SizedBox(width: isTablet ? 14 : 12),
          Flexible(
            child: Text(
              text,
              style: TextStyle(
                fontSize: isTablet ? 17 : 15,
                fontWeight: FontWeight.w500,
                color: AppTheme.accentColor,
              ),
            ),
          ),
        ],
      ),
    );
  }
}