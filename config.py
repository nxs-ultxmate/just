import xml.etree.ElementTree as ET
from typing import Optional
from exceptions import XMLConfigError, InvalidParameterError, MissingParameterError

class PackageAnalyzerConfig:
    """Класс для работы с конфигурацией анализатора пакетов"""
    
    def __init__(self, config_path: str = "config.xml"):
        self.config_path = config_path
        self.package_name: Optional[str] = None
        self.repository_url: Optional[str] = None
        self.test_mode: bool = False
        self.package_version: Optional[str] = None
        self.output_filename: str = "dependency_graph.png"
        self.max_depth: int = 3
        self.filter_substring: Optional[str] = None
        
    def load_config(self) -> None:
        """Загружает конфигурацию из XML файла"""
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            
            # Обязательные параметры
            self.package_name = self._get_required_parameter(root, 'package_name')
            self.repository_url = self._get_required_parameter(root, 'repository_url')
            
            # Опциональные параметры с значениями по умолчанию
            self.test_mode = self._get_optional_bool(root, 'test_mode', False)
            self.package_version = self._get_optional_parameter(root, 'package_version')
            self.output_filename = self._get_optional_parameter(root, 'output_filename', 'dependency_graph.png')
            self.max_depth = self._get_optional_int(root, 'max_depth', 3)
            self.filter_substring = self._get_optional_parameter(root, 'filter_substring')
            
            self._validate_parameters()
            
        except ET.ParseError as e:
            raise XMLConfigError(f"Ошибка парсинга XML файла: {e}")
        except FileNotFoundError:
            raise XMLConfigError(f"Конфигурационный файл не найден: {self.config_path}")
    
    def _get_required_parameter(self, root: ET.Element, param_name: str) -> str:
        """Получает обязательный параметр из XML"""
        element = root.find(param_name)
        if element is None or element.text is None or not element.text.strip():
            raise MissingParameterError(f"Обязательный параметр '{param_name}' отсутствует или пустой")
        return element.text.strip()
    
    def _get_optional_parameter(self, root: ET.Element, param_name: str, default: Optional[str] = None) -> Optional[str]:
        """Получает опциональный параметр из XML"""
        element = root.find(param_name)
        if element is not None and element.text is not None and element.text.strip():
            return element.text.strip()
        return default
    
    def _get_optional_bool(self, root: ET.Element, param_name: str, default: bool) -> bool:
        """Получает булевый параметр из XML"""
        element = root.find(param_name)
        if element is not None and element.text is not None:
            text = element.text.strip().lower()
            if text in ('true', '1', 'yes'):
                return True
            elif text in ('false', '0', 'no'):
                return False
        return default
    
    def _get_optional_int(self, root: ET.Element, param_name: str, default: int) -> int:
        """Получает целочисленный параметр из XML"""
        element = root.find(param_name)
        if element is not None and element.text is not None:
            try:
                return int(element.text.strip())
            except ValueError:
                raise InvalidParameterError(f"Параметр '{param_name}' должен быть целым числом")
        return default
    
    def _validate_parameters(self) -> None:
        """Валидирует параметры конфигурации"""
        if self.max_depth < 1:
            raise InvalidParameterError("Максимальная глубина анализа должна быть положительным числом")
        
        if self.output_filename and not self.output_filename.endswith(('.png', '.jpg', '.jpeg', '.svg')):
            raise InvalidParameterError("Имя файла изображения должно иметь расширение (.png, .jpg, .jpeg, .svg)")
    
    def display_config(self) -> None:
        """Выводит конфигурацию в формате ключ-значение"""
        config_items = [
            ("Имя анализируемого пакета", self.package_name),
            ("URL-адрес репозитория", self.repository_url),
            ("Режим работы с тестовым репозиторием", "Включен" if self.test_mode else "Отключен"),
            ("Версия пакета", self.package_version or "Не указана"),
            ("Имя файла с изображением графа", self.output_filename),
            ("Максимальная глубина анализа", self.max_depth),
            ("Подстрока для фильтрации пакетов", self.filter_substring or "Не указана")
        ]
        
        print("=" * 50)
        print("Конфигурация анализатора пакетов")
        print("=" * 50)
        for key, value in config_items:
            print(f"{key}: {value}")
        print("=" * 50)