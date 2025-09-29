import sys
import yaml

def validate_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"YAML validation successful: {file_path}")
        return 0
    except yaml.YAMLError as exc:
        print(f"YAML validation error in {file_path}:")
        print(exc)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_yaml.py <file.yaml>")
        sys.exit(1)
    sys.exit(validate_yaml(sys.argv[1]))
