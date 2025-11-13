#!/usr/bin/env python3
"""
Демонстрация работы анализатора пакетов
"""

import os
import tempfile
from config import PackageAnalyzerConfig
from exceptions import ConfigurationError

def demonstrate_working_config():
    """Демонстрация работы с корректной конфигурацией"""
    print("=== Демонстрация работы с корректной конфигурацией ===")
    
    config = PackageAnalyzerConfig("config.xml")
    try:
        config.load_config()
        config.display_config()
        print("✅ Конфигурация успешно загружена!")
    except ConfigurationError as e:
        print(f"❌ Ошибка: {e}")

def demonstrate_error_handling():
    """Демонстрация обработки ошибок"""
    print("\n=== Демонстрация обработки ошибок ===")
    
    # Создаем временный файл с ошибками
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write("""<?xml version="1.0"?>
<configuration>
    <package_name></package_name>
    <repository_url>https://example.com/repo</repository_url>
    <max_depth>invalid</max_depth>
</configuration>""")
        temp_config_path = f.name
    
    try:
        config = PackageAnalyzerConfig(temp_config_path)
        config.load_config()
    except ConfigurationError as e:
        print(f"✅ Ошибка корректно обработана: {e}")
    finally:
        os.unlink(temp_config_path)

if __name__ == "__main__":
    demonstrate_working_config()
    demonstrate_error_handling()