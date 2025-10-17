#!/usr/bin/env python3
"""
i18n (Internationalization) Demo

This example demonstrates how to use the i18n system in CodeViewX.
"""

from codeviewx import get_i18n, t, set_locale, detect_ui_language


def demo_auto_detection():
    """Demonstrate automatic language detection"""
    print("=" * 60)
    print("1. Auto Language Detection")
    print("=" * 60)
    
    ui_lang = detect_ui_language()
    print(f"Detected system language: {ui_lang}")
    print()


def demo_english():
    """Demonstrate English messages"""
    print("=" * 60)
    print("2. English Messages")
    print("=" * 60)
    
    set_locale('en')
    print(t('starting'))
    print(t('working_dir') + ': /path/to/project')
    print(t('generated_files', count=5))
    print(t('analyzing_structure'))
    print(t('completed'))
    print()


def demo_chinese():
    """Demonstrate Chinese messages"""
    print("=" * 60)
    print("3. Chinese Messages")
    print("=" * 60)
    
    set_locale('zh')
    print(t('starting'))
    print(t('working_dir') + ': /path/to/project')
    print(t('generated_files', count=5))
    print(t('analyzing_structure'))
    print(t('completed'))
    print()


def demo_dynamic_switching():
    """Demonstrate dynamic language switching"""
    print("=" * 60)
    print("4. Dynamic Language Switching")
    print("=" * 60)
    
    i18n = get_i18n()
    
    for lang in ['en', 'zh', 'en']:
        i18n.set_locale(lang)
        print(f"\nLanguage: {lang}")
        print(f"  {t('cli_description')}")
        print(f"  {t('completed')}")
    print()


def demo_error_messages():
    """Demonstrate error messages"""
    print("=" * 60)
    print("5. Error Messages")
    print("=" * 60)
    
    set_locale('en')
    print("English:")
    print(f"  {t('error_file_not_found', filename='test.md')}")
    print(f"  {t('error_template_variable', variable='working_directory')}")
    
    print()
    
    set_locale('zh')
    print("Chinese:")
    print(f"  {t('error_file_not_found', filename='test.md')}")
    print(f"  {t('error_template_variable', variable='working_directory')}")
    print()


def demo_cli_messages():
    """Demonstrate CLI messages"""
    print("=" * 60)
    print("6. CLI Messages")
    print("=" * 60)
    
    set_locale('en')
    print("English:")
    print(f"  {t('cli_starting_server')}")
    print(f"  {t('cli_server_address')}")
    print(f"  {t('cli_server_stop')}")
    
    print()
    
    set_locale('zh')
    print("Chinese:")
    print(f"  {t('cli_starting_server')}")
    print(f"  {t('cli_server_address')}")
    print(f"  {t('cli_server_stop')}")
    print()


def main():
    """
    Main demo function
    """
    print("\n" + "=" * 60)
    print("CodeViewX i18n System Demo")
    print("=" * 60)
    print()
    
    demo_auto_detection()
    demo_english()
    demo_chinese()
    demo_dynamic_switching()
    demo_error_messages()
    demo_cli_messages()
    
    print("=" * 60)
    print("✓ Demo completed!")
    print("=" * 60)
    print()
    
    print("Available locales:", get_i18n().available_locales())
    print("Current locale:", get_i18n().get_locale())
    print()


if __name__ == "__main__":
    main()

