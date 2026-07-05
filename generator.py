import json
import os
from jinja2 import Environment, FileSystemLoader

def load_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate(schema_path, template_dir, out_path):
    schema = load_schema(schema_path)
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    tmpl = env.get_template('structs.jinja2')
    rendered = tmpl.render(types=schema.get('types', []))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    print('Generated', out_path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate serialization code from interface.json')
    parser.add_argument('--schema', default='interface.json')
    parser.add_argument('--templates', default='templates')
    parser.add_argument('--out', default='generated/messages.py')
    args = parser.parse_args()
    generate(args.schema, args.templates, args.out)
