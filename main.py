#!/usr/bin/env python3
"""
Основной модуль для анализа зависимостей NuGet пакетов
"""

from dependency_analyzer import NuGetDependencyAnalyzer

def analyze_packages():
    """
    Анализирует предопределенные пакеты и выводит их зависимости
    """
    # Список пакетов для анализа (пакет, версия)
    packages_to_analyze = [
        ("Newtonsoft.Json", "13.0.1"),
        ("Microsoft.EntityFrameworkCore", "7.0.0"),
        ("Serilog", "2.12.0"),
        ("AutoMapper", "12.0.1"),
        ("FluentValidation", "11.5.0")
    ]
    
    print("=== Анализатор зависимостей NuGet пакетов ===")
    print("Этап 2: Сбор данных о зависимостях")
    print("\nАнализ предопределенных пакетов...")
    print("=" * 70)
    
    # Создаем экземпляр анализатора
    analyzer = NuGetDependencyAnalyzer()
    
    total_packages = len(packages_to_analyze)
    processed_packages = 0
    
    for package_name, version in packages_to_analyze:
        try:
            print(f"\n\nАнализ пакета {processed_packages + 1}/{total_packages}")
            print("-" * 50)
            
            # Получаем прямые зависимости
            dependencies = analyzer.get_direct_dependencies(package_name, version)
            
            # Выводим результат на экран
            analyzer.display_dependencies(package_name, version, dependencies)
            
            processed_packages += 1
            
            # Небольшая пауза между запросами чтобы не перегружать API
            import time
            time.sleep(1)
            
        except Exception as e:
            print(f"\nОшибка при анализе пакета {package_name}: {str(e)}")
            processed_packages += 1
            continue
    
    print("\n" + "=" * 70)
    print(f"Анализ завершен! Обработано пакетов: {processed_packages}/{total_packages}")

def main():
    """
    Основная функция приложения
    """
    try:
        analyze_packages()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла критическая ошибка: {str(e)}")

if __name__ == "__main__":
    main()