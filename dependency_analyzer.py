import urllib.request
import urllib.error
import json
import sys
from typing import List, Dict, Optional

class NuGetDependencyAnalyzer:
    """
    Анализатор зависимостей NuGet пакетов
    """
    
    # Базовый URL для NuGet API
    NUGET_API_BASE_URL = "https://api.nuget.org/v3-flatcontainer"
    
    def __init__(self):
        self.session = urllib.request.build_opener()
        self.session.addheaders = [('User-Agent', 'NuGet-Dependency-Analyzer/1.0')]
    
    def get_package_info(self, package_name: str, version: str) -> Optional[Dict]:
        """
        Получает информацию о пакете из NuGet API
        
        Args:
            package_name: Название пакета
            version: Версия пакета
            
        Returns:
            Словарь с информацией о пакете или None в случае ошибки
        """
        try:
            # Формируем URL для получения информации о пакете
            url = f"{self.NUGET_API_BASE_URL}/{package_name.lower()}/{version}/{package_name.lower()}.nuspec"
            
            print(f"Запрос к API: {url}")
            
            # Выполняем HTTP-запрос
            with self.session.open(url) as response:
                if response.status == 200:
                    # Читаем и декодируем XML ответ (NuGet использует nuspec формат)
                    content = response.read().decode('utf-8')
                    return self._parse_nuspec_content(content, package_name, version)
                else:
                    print(f"Ошибка: Пакет не найден (HTTP {response.status})")
                    return None
                    
        except urllib.error.HTTPError as e:
            print(f"HTTP ошибка: {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            print(f"URL ошибка: {e.reason}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {str(e)}")
            return None
    
    def _parse_nuspec_content(self, content: str, package_name: str, version: str) -> Dict:
        """
        Парсит содержимое nuspec файла и извлекает зависимости
        
        Args:
            content: XML содержимое nuspec файла
            package_name: Название пакета
            version: Версия пакета
            
        Returns:
            Словарь с информацией о пакете и его зависимостях
        """
        package_info = {
            'name': package_name,
            'version': version,
            'dependencies': []
        }
        
        try:
            # Упрощенный парсинг XML для извлечения зависимостей
            lines = content.split('\n')
            in_dependencies = False
            
            for line in lines:
                line = line.strip()
                
                # Ищем начало секции зависимостей
                if '<dependencies>' in line:
                    in_dependencies = True
                    continue
                
                # Ищем конец секции зависимостей
                if '</dependencies>' in line:
                    in_dependencies = False
                    continue
                
                # Парсим зависимости
                if in_dependencies and '<dependency' in line:
                    dependency = self._parse_dependency_line(line)
                    if dependency:
                        package_info['dependencies'].append(dependency)
                        
        except Exception as e:
            print(f"Ошибка при парсинге зависимостей: {str(e)}")
        
        return package_info
    
    def _parse_dependency_line(self, line: str) -> Optional[Dict]:
        """
        Парсит строку с информацией о зависимости
        
        Args:
            line: Строка XML с информацией о зависимости
            
        Returns:
            Словарь с информацией о зависимости или None в случае ошибки
        """
        try:
            # Извлекаем атрибуты из строки вида: <dependency id="Package.Name" version="1.0.0" />
            id_start = line.find('id="') + 4
            id_end = line.find('"', id_start)
            
            version_start = line.find('version="') + 9
            version_end = line.find('"', version_start)
            
            if id_start > 3 and id_end > id_start and version_start > 8 and version_end > version_start:
                package_id = line[id_start:id_end]
                package_version = line[version_start:version_end]
                
                return {
                    'id': package_id,
                    'version': package_version
                }
        except Exception as e:
            print(f"Ошибка при парсинге строки зависимости: {str(e)}")
        
        return None
    
    def get_direct_dependencies(self, package_name: str, version: str) -> List[Dict]:
        """
        Получает прямые зависимости указанного пакета
        
        Args:
            package_name: Название пакета
            version: Версия пакета
            
        Returns:
            Список прямых зависимостей
        """
        print(f"\nПолучение зависимостей для пакета: {package_name} версии {version}")
        print("=" * 50)
        
        package_info = self.get_package_info(package_name, version)
        
        if package_info and package_info['dependencies']:
            return package_info['dependencies']
        else:
            return []
    
    def display_dependencies(self, package_name: str, version: str, dependencies: List[Dict]):
        """
        Выводит зависимости на экран
        
        Args:
            package_name: Название пакета
            version: Версия пакета
            dependencies: Список зависимостей для отображения
        """
        print(f"\nРезультаты анализа пакета: {package_name} версии {version}")
        print("=" * 60)
        
        if not dependencies:
            print("Прямые зависимости не найдены.")
            return
        
        print("\nПрямые зависимости пакета:")
        print("-" * 40)
        
        for i, dep in enumerate(dependencies, 1):
            print(f"{i}. {dep['id']} версия {dep['version']}")
        
        print(f"\nИтого найдено прямых зависимостей: {len(dependencies)}")