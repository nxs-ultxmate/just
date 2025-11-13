import os
from dependency_parser import DependencyParser
from mermaid_generator import MermaidGenerator
from graph_visualizer import GraphVisualizer
from comparison_tool import ComparisonTool

def ensure_directory(directory: str):
    """Создать директорию если не существует"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    print("🚀 Запуск визуализатора графа зависимостей")
    
    # Создаем необходимые директории
    ensure_directory('examples')
    ensure_directory('mermaid_files')
    
    # Инициализируем компоненты
    parser = DependencyParser()
    mermaid_gen = MermaidGenerator(parser)
    visualizer = GraphVisualizer(parser)
    comparer = ComparisonTool(parser)
    
    print("📦 Анализ установленных пакетов...")
    parser.build_dependency_graph()
    
    # Выбираем пакеты для демонстрации
    demo_packages = ['requests', 'numpy', 'matplotlib']
    
    print(f"\n🎯 Демонстрационные пакеты: {', '.join(demo_packages)}")
    
    for i, package in enumerate(demo_packages, 1):
        print(f"\n{'='*50}")
        print(f"ПАКЕТ {i}: {package}")
        print(f"{'='*50}")
        
        # Генерируем Mermaid диаграмму
        mermaid_code = mermaid_gen.generate_mermaid_graph(package)
        mermaid_file = f"mermaid_files/{package}_dependencies.mmd"
        mermaid_gen.save_mermaid_to_file(mermaid_code, mermaid_file)
        
        print(f"📊 Mermaid диаграмма создана: {mermaid_file}")
        
        # Создаем визуализацию
        png_file = f"examples/example{i}.png"
        visualizer.visualize_package_dependencies(package, png_file)
        
        # Сравниваем с официальными инструментами
        print(f"\n🔍 Сравнение с официальными инструментами...")
        
        our_graph = visualizer.create_networkx_graph(package)
        official_graph = comparer.create_official_graph(package)
        
        if official_graph.number_of_nodes() > 0:
            comparison_result = comparer.compare_graphs(our_graph, official_graph)
            comparer.print_comparison_report(comparison_result, package)
            
            # Создаем сравнительную визуализацию
            comparison_file = f"examples/comparison_{package}.png"
            visualizer.create_comparison_visualization(
                package, our_graph, official_graph, comparison_file
            )
        else:
            print("⚠️  Официальные данные недоступны для сравнения")
    
    print(f"\n✅ Визуализация завершена!")
    print(f"📁 Результаты сохранены в папках 'examples' и 'mermaid_files'")
    
    # Сохраняем сводный отчет
    save_summary_report(demo_packages)

def save_summary_report(packages: list):
    """Сохранить сводный отчет"""
    with open('visualization_report.md', 'w', encoding='utf-8') as f:
        f.write("# Отчет по визуализации графа зависимостей\n\n")
        f.write("## Демонстрационные пакеты:\n")
        for i, pkg in enumerate(packages, 1):
            f.write(f"{i}. **{pkg}**\n")
        
        f.write("\n## Созданные файлы:\n")
        f.write("- PNG изображения графов в папке `examples/`\n")
        f.write("- Mermaid диаграммы в папке `mermaid_files/`\n")
        f.write("- Сравнительные визуализации в папке `examples/`\n")
        f.write("- Этот отчет в файле `visualization_report.md`\n")
        
        f.write("\n## Инструкция по использованию Mermaid диаграмм:\n")
        f.write("1. Скопируйте содержимое .mmd файлов\n")
        f.write("2. Вставьте в поддерживаемый редактор Mermaid (GitHub, Mermaid Live Editor)\n")
        f.write("3. Получите визуальное представление графа\n")

if __name__ == "__main__":
    main()