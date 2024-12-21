from pathlib import Path

# Укажите полный путь к файлу
public_key_path = Path("/certs/jwt-private.pem")

# Проверка существования файла
if public_key_path.exists():
    print("Файл найден.")
    # Открытие файла в режиме чтения
    with public_key_path.open("r") as f:
        content = f.read()
        print("Содержимое файла:")
        print(content)
else:
    print("Файл не найден.")
