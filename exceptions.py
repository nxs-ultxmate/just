class ConfigurationError(Exception):
    """Базовое исключение для ошибок конфигурации"""
    pass

class XMLConfigError(ConfigurationError):
    """Ошибка парсинга XML конфигурации"""
    pass

class InvalidParameterError(ConfigurationError):
    """Некорректное значение параметра"""
    pass

class MissingParameterError(ConfigurationError):
    """Отсутствует обязательный параметр"""
    pass