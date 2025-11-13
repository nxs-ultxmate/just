import sys
from config import PackageAnalyzerConfig
from exceptions import ConfigurationError

def main():
    """Основная функция CLI приложения"""
    try:
        # Загрузка конфигурации
        config = PackageAnalyzerConfig()
        config.load_config()
        
        # Вывод конфигурации (требование этапа 1)
        config.display_config()
        
        # Здесь в будущих этапах будет основная логика анализа
        print("\nКонфигурация успешно загружена. Готов к анализу зависимостей!")
        
    except ConfigurationError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()