class MermaidGenerator:
    def __init__(self, dependency_parser: DependencyParser):
        self.parser = dependency_parser
    
    def generate_mermaid_graph(self, package_name: str, max_nodes: int = 20) -> str:
        """Сгенерировать Mermaid диаграмму для пакета"""
        package_info = self.parser.get_package_info(package_name)
        
        mermaid_code = ["graph TD"]
        
        # Добавляем центральный пакет
        mermaid_code.append(f"    {self._format_node_name(package_name)}[{package_name}]")
        
        # Добавляем прямые зависимости
        added_nodes = {package_name}
        
        for i, dep in enumerate(package_info['direct_dependencies'][:max_nodes//2]):
            dep_node = self._format_node_name(dep)
            mermaid_code.append(f"    {dep_node}[{dep}]")
            mermaid_code.append(f"    {self._format_node_name(package_name)} --> {dep_node}")
            added_nodes.add(dep)
        
        # Добавляем обратные зависимости
        for i, rev_dep in enumerate(package_info['reverse_dependencies'][:max_nodes//2]):
            rev_dep_node = self._format_node_name(rev_dep)
            if rev_dep not in added_nodes:
                mermaid_code.append(f"    {rev_dep_node}[{rev_dep}]")
                added_nodes.add(rev_dep)
            mermaid_code.append(f"    {rev_dep_node} --> {self._format_node_name(package_name)}")
        
        return '\n'.join(mermaid_code)
    
    def _format_node_name(self, name: str) -> str:
        """Форматировать имя узла для Mermaid"""
        # Заменяем недопустимые символы
        return name.replace('-', '_').replace('.', '_').replace(' ', '_')
    
    def save_mermaid_to_file(self, mermaid_code: str, filename: str):
        """Сохранить Mermaid код в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        print(f"Mermaid код сохранен в {filename}")