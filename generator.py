import json
import os
import sys
from jinja2 import Environment, FileSystemLoader, TemplateError

# Obsługiwane typy danych i ich rozmiary w bajtach
SUPPORTED_TYPES = {
    'uint32': 4,
    'int32': 4,
    'int64': 8,
    'uint64': 8,
    'float': 4,
    'double': 8,
    'bool': 1,
    'string': -1,  # zmienna długość
    'bytes': -1,   # zmienna długość
}

def validate_schema(schema):
    """Waliduj strukturę schematu JSON.
    
    Args:
        schema (dict): Schemat z 'types' i definicjami struktur
        
    Raises:
        ValueError: jeśli schemat jest nieprawidłowy
    """
    if not isinstance(schema, dict):
        raise ValueError("Schemat musi być słownikiem (dict)")
    
    if 'types' not in schema:
        raise ValueError("Schemat musi zawierać klucz 'types' (lista typów)")
    
    if not isinstance(schema['types'], list):
        raise ValueError("'types' musi być listą")
    
    if len(schema['types']) == 0:
        raise ValueError("'types' nie może być pusta")
    
    for i, type_def in enumerate(schema['types']):
        validate_type_definition(type_def, i)

def validate_type_definition(type_def, index):
    """Waliduj definicję einzelnego typu.
    
    Args:
        type_def (dict): Definicja typu
        index (int): Indeks typu w liście
        
    Raises:
        ValueError: jeśli typ jest nieprawidłowy
    """
    if not isinstance(type_def, dict):
        raise ValueError(f"Type #{index}: musi być słownikiem")
    
    if 'name' not in type_def:
        raise ValueError(f"Type #{index}: brak wymaganego klucza 'name'")
    
    name = type_def['name']
    
    if not isinstance(name, str) or not name:
        raise ValueError(f"Type #{index}: 'name' musi być niepustym stringiem")
    
    if not name[0].isupper():
        raise ValueError(f"Type '{name}': nazwa musi zaczynać się wielką literą")
    
    if 'fields' not in type_def:
        raise ValueError(f"Type '{name}': brak wymaganego klucza 'fields'")
    
    if not isinstance(type_def['fields'], list):
        raise ValueError(f"Type '{name}': 'fields' musi być listą")
    
    if len(type_def['fields']) == 0:
        raise ValueError(f"Type '{name}': 'fields' nie może być pusta")
    
    for j, field in enumerate(type_def['fields']):
        validate_field(field, name, j)

def validate_field(field, type_name, field_index):
    """Waliduj definicję pola.
    
    Args:
        field (dict): Definicja pola
        type_name (str): Nazwa rodzica (typu)
        field_index (int): Indeks pola w strukturze
        
    Raises:
        ValueError: jeśli pole jest nieprawidłowe
    """
    if not isinstance(field, dict):
        raise ValueError(f"Type '{type_name}', field #{field_index}: musi być słownikiem")
    
    if 'name' not in field:
        raise ValueError(f"Type '{type_name}', field #{field_index}: brak 'name'")
    
    if 'type' not in field:
        raise ValueError(f"Type '{type_name}', field #{field_index}: brak 'type'")
    
    field_name = field['name']
    field_type = field['type']
    
    if not isinstance(field_name, str) or not field_name:
        raise ValueError(f"Type '{type_name}', field #{field_index}: 'name' musi być stringiem")
    
    if not isinstance(field_type, str) or not field_type:
        raise ValueError(f"Type '{type_name}', field '{field_name}': 'type' musi być stringiem")
    
    # Sprawdź czy typ jest obsługiwany (może być base type lub array)
    base_type = field_type.rstrip('[]')
    is_array = field_type.endswith('[]')
    
    if base_type not in SUPPORTED_TYPES:
        raise ValueError(
            f"Type '{type_name}', field '{field_name}': nieznany typ '{base_type}'. "
            f"Obsługiwane typy: {', '.join(SUPPORTED_TYPES.keys())}"
        )

def load_schema(path):
    """Załaduj i zwaliduj schemat JSON.
    
    Args:
        path (str): Ścieżka do interface.json
        
    Returns:
        dict: Zwalidowany schemat
        
    Raises:
        FileNotFoundError: jeśli plik nie istnieje
        json.JSONDecodeError: jeśli JSON jest nieprawidłowy
        ValueError: jeśli schemat nie przechodzi walidacji
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Plik schematu nie istnieje: {path}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Błąd parsowania JSON: {e}")
    
    validate_schema(schema)
    return schema

def generate(schema_path, template_dir, out_path):
    """Wygeneruj moduł serializacji z schematu.
    
    Args:
        schema_path (str): Ścieżka do interface.json
        template_dir (str): Ścieżka do katalogu szablonów
        out_path (str): Ścieżka do wyjściowego pliku .py
        
    Raises:
        Verschiedene błędy jeśli schemat, szablony lub proces generacji się nie powiedzie
    """
    try:
        schema = load_schema(schema_path)
        print(f"✓ Schemat wczytany: {len(schema['types'])} typów")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"✗ Błąd schematu: {e}", file=sys.stderr)
        raise
    
    try:
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        tmpl = env.get_template('structs.jinja2')
        print(f"✓ Szablon załadowany: {template_dir}/structs.jinja2")
    except Exception as e:
        print(f"✗ Błąd szablonu: {e}", file=sys.stderr)
        raise
    
    try:
        rendered = tmpl.render(types=schema.get('types', []))
        print(f"✓ Kod wygenerowany ({len(rendered)} znaków)")
    except TemplateError as e:
        print(f"✗ Błąd renderowania szablonu: {e}", file=sys.stderr)
        raise
    
    try:
        os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"✓ Zapisano: {out_path}")
    except IOError as e:
        print(f"✗ Błąd zapisu: {e}", file=sys.stderr)
        raise

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Generator serializacji/deserializacji z interface.json'
    )
    parser.add_argument('--schema', default='interface.json',
                       help='Ścieżka do interface.json (default: interface.json)')
    parser.add_argument('--templates', default='templates',
                       help='Ścieżka do katalogu szablonów (default: templates)')
    parser.add_argument('--out', default='generated/messages.py',
                       help='Ścieżka do wyjściowego pliku (default: generated/messages.py)')
    args = parser.parse_args()
    
    try:
        generate(args.schema, args.templates, args.out)
        print("✓ Sukces!")
        sys.exit(0)
    except Exception as e:
        sys.exit(1)
