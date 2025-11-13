import subprocess
import json
import networkx as nx
from typing import Dict, List

class ComparisonTool:
    def __init__(self, dependency_parser):
        self.parser = dependency_parser
    
    def get_official_dependencies(self, package_name: str) -> Dict:
        """Получить зависимости через официальные инструменты (pipdeptree)"""
        try:
            result = subprocess.run(
                ['pipdeptree', '-p', package_name, '--json'],
                capture_output=True, text=True, check=True
            )
            
            data = json.loads(result.stdout)
            return self._parse_pipdeptree_output(data, package_name)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("pipdeptree не установлен. Установите: pip install pipdeptree")
            return {}
    
    def _parse_pipdeptree_output(self, data: List, package_name: str) -> Dict:
        """Парсить вывод pipdeptree"""
        dependencies = {}
        
        for item in data:
            if item['package']['key'].lower() == package_name.lower():
                dependencies['package'] = package_name
                dependencies['dependencies'] = []
                
                for dep in item.get('dependencies', []):
                    dep_name = dep['key'].split('[')[0]  # Убираем extras
                    dependencies['dependencies'].append(dep_name)
                
                break
        
        return dependencies
    
    def create_official_graph(self, package_name: str) -> nx.DiGraph:
        """Создать граф из официальных данных"""
        G = nx.DiGraph()
        official_data = self.get_official_dependencies(package_name)
        
        if not official_data:
            return G
        
        G.add_node(package_name)
        
        for dep in official_data.get('dependencies', []):
            G.add_node(dep)
            G.add_edge(package_name, dep)
        
        return G
    
    def compare_graphs(self, our_graph: nx.DiGraph, official_graph: nx.DiGraph) -> Dict:
        """Сравнить два графа"""
        our_nodes = set(our_graph.nodes())
        official_nodes = set(official_graph.nodes())
        
        our_edges = set(our_graph.edges())
        official_edges = set(official_graph.edges())
        
        return {
            'common_nodes': our_nodes & official_nodes,
            'our_unique_nodes': our_nodes - official_nodes,
            'official_unique_nodes': official_nodes - our_nodes,
            'common_edges': our_edges & official_edges,
            'our_unique_edges': our_edges - official_edges,
            'official_unique_edges': official_edges - our_edges,
            'our_node_count': len(our_nodes),
            'official_node_count': len(official_nodes),
            'our_edge_count': len(our_edges),
            'official_edge_count': len(official_edges)
        }
    
    def print_comparison_report(self, comparison_result: Dict, package_name: str):
        """Напечатать отчет о сравнении"""
        print(f"\n{'='*60}")
        print(f"ОТЧЕТ СРАВНЕНИЯ ДЛЯ ПАКЕТА: {package_name}")
        print(f"{'='*60}")
        
        print(f"\nСТАТИСТИКА УЗЛОВ:")
        print(f"Общие узлы: {len(comparison_result['common_nodes'])}")
        print(f"Уникальные узлы в нашей визуализации: {len(comparison_result['our_unique_nodes'])}")
        print(f"Уникальные узлы в официальной визуализации: {len(comparison_result['official_unique_nodes'])}")
        
        print(f"\nСТАТИСТИКА РЕБЕР:")
        print(f"Общие ребра: {len(comparison_result['common_edges'])}")
        print(f"Уникальные ребра в нашей визуализации: {len(comparison_result['our_unique_edges'])}")
        print(f"Уникальные ребра в официальной визуализации: {len(comparison_result['official_unique_edges'])}")
        
        if comparison_result['our_unique_nodes']:
            print(f"\nУНИКАЛЬНЫЕ УЗЛЫ В НАШЕЙ ВИЗУАЛИЗАЦИИ:")
            for node in sorted(comparison_result['our_unique_nodes']):
                print(f"  - {node}")
        
        if comparison_result['official_unique_nodes']:
            print(f"\nУНИКАЛЬНЫЕ УЗЛЫ В ОФИЦИАЛЬНОЙ ВИЗУАЛИЗАЦИИ:")
            for node in sorted(comparison_result['official_unique_nodes']):
                print(f"  - {node}")
        
        print(f"\nОБЪЯСНЕНИЕ РАСХОЖДЕНИЙ:")
        self._explain_differences(comparison_result)

    def _explain_differences(self, comparison_result: Dict):
        """Объяснить расхождения в результатах"""
        reasons = []
        
        if comparison_result['our_unique_nodes']:
            reasons.append(
                "• Наш инструмент может включать транзитивные зависимости или зависимости окружения"
            )
        
        if comparison_result['official_unique_nodes']:
            reasons.append(
                "• pipdeptree показывает только прямые зависимости, указанные в метаданных пакета"
            )
        
        if len(comparison_result['our_node_count']) > len(comparison_result['official_node_count']):
            reasons.append(
                "• Наш анализ может быть более глубоким и включать непрямые зависимости"
            )
        
        if not reasons:
            reasons.append("• Расхождений не обнаружено, результаты идентичны")
        
        for reason in reasons:
            print(f"  {reason}")