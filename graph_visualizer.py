import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List
import os

class GraphVisualizer:
    def __init__(self, dependency_parser: DependencyParser):
        self.parser = dependency_parser
    
    def create_networkx_graph(self, package_name: str, max_depth: int = 2) -> nx.DiGraph:
        """Создать граф NetworkX для визуализации"""
        G = nx.DiGraph()
        
        def add_dependencies(pkg: str, depth: int = 0):
            if depth > max_depth:
                return
            
            G.add_node(pkg)
            
            deps = self.parser.dependencies.get(pkg, [])
            for dep in deps:
                G.add_node(dep)
                G.add_edge(pkg, dep)
                add_dependencies(dep, depth + 1)
        
        add_dependencies(package_name)
        return G
    
    def visualize_package_dependencies(self, package_name: str, output_file: str = None):
        """Визуализировать зависимости пакета"""
        G = self.create_networkx_graph(package_name)
        
        plt.figure(figsize=(12, 8))
        
        # Используем spring layout для лучшего расположения узлов
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Рисуем граф
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=2000, alpha=0.7)
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        plt.title(f'Граф зависимостей для пакета: {package_name}', fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Граф сохранен в {output_file}")
        
        plt.show()
    
    def create_comparison_visualization(self, package_name: str, our_graph: nx.DiGraph, 
                                      official_graph: nx.DiGraph, output_file: str):
        """Создать сравнительную визуализацию"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        # Наш граф
        pos1 = nx.spring_layout(our_graph, k=1, iterations=50)
        nx.draw_networkx_nodes(our_graph, pos1, node_color='lightblue', 
                              node_size=1500, alpha=0.7, ax=ax1)
        nx.draw_networkx_edges(our_graph, pos1, edge_color='blue', 
                              arrows=True, arrowsize=15, alpha=0.6, ax=ax1)
        nx.draw_networkx_labels(our_graph, pos1, font_size=6, font_weight='bold', ax=ax1)
        ax1.set_title('Наша визуализация', fontsize=12)
        ax1.axis('off')
        
        # Официальный граф
        pos2 = nx.spring_layout(official_graph, k=1, iterations=50)
        nx.draw_networkx_nodes(official_graph, pos2, node_color='lightgreen', 
                              node_size=1500, alpha=0.7, ax=ax2)
        nx.draw_networkx_edges(official_graph, pos2, edge_color='green', 
                              arrows=True, arrowsize=15, alpha=0.6, ax=ax2)
        nx.draw_networkx_labels(official_graph, pos2, font_size=6, font_weight='bold', ax=ax2)
        ax2.set_title('Официальная визуализация (pipdeptree)', fontsize=12)
        ax2.axis('off')
        
        plt.suptitle(f'Сравнение визуализаций для пакета: {package_name}', fontsize=16)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()