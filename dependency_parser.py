import subprocess
import json
import sys
from typing import Dict, List, Set, Tuple
import pkg_resources

class DependencyParser:
    def __init__(self):
        self.dependencies = {}
        self.reverse_dependencies = {}
    
    def get_installed_packages(self) -> List[str]:
        """Получить список установленных пакетов"""
        return [pkg.key for pkg in pkg_resources.working_set]
    
    def get_package_dependencies(self, package_name: str) -> List[str]:
        """Получить зависимости для конкретного пакета"""
        try:
            # Используем pip show для получения информации о пакете
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', package_name],
                capture_output=True, text=True, check=True
            )
            
            dependencies = []
            for line in result.stdout.split('\n'):
                if line.startswith('Requires:'):
                    deps = line.split(':', 1)[1].strip()
                    if deps:
                        dependencies = [dep.strip().lower() for dep in deps.split(',')]
                    break
            
            return dependencies
        except subprocess.CalledProcessError:
            return []
    
    def build_dependency_graph(self, max_depth: int = 3) -> Dict[str, List[str]]:
        """Построить граф зависимостей для всех пакетов"""
        packages = self.get_installed_packages()
        self.dependencies = {}
        
        for package in packages:
            self._get_dependencies_recursive(package, set(), max_depth)
        
        self._build_reverse_dependencies()
        return self.dependencies
    
    def _get_dependencies_recursive(self, package: str, visited: Set[str], max_depth: int, current_depth: int = 0):
        """Рекурсивно получить зависимости пакета"""
        if current_depth > max_depth or package in visited:
            return
        
        visited.add(package)
        
        if package not in self.dependencies:
            deps = self.get_package_dependencies(package)
            self.dependencies[package] = deps
            
            for dep in deps:
                if dep not in visited:
                    self._get_dependencies_recursive(dep, visited, max_depth, current_depth + 1)
    
    def _build_reverse_dependencies(self):
        """Построить обратные зависимости (какие пакеты зависят от данного)"""
        self.reverse_dependencies = {}
        
        for package, deps in self.dependencies.items():
            for dep in deps:
                if dep not in self.reverse_dependencies:
                    self.reverse_dependencies[dep] = []
                self.reverse_dependencies[dep].append(package)
    
    def get_package_info(self, package_name: str) -> Dict:
        """Получить полную информацию о пакете и его зависимостях"""
        direct_deps = self.dependencies.get(package_name, [])
        reverse_deps = self.reverse_dependencies.get(package_name, [])
        
        return {
            'package': package_name,
            'direct_dependencies': direct_deps,
            'reverse_dependencies': reverse_deps,
            'dependency_count': len(direct_deps),
            'dependent_count': len(reverse_deps)
        }