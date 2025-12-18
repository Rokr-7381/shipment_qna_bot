import os


def update_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if not os.path.exists(env_path):
        print(f"No .env found at {env_path}")
        return

    updates = {
        "AZURE_SEARCH_CONTAINER_FIELD": "metadata",
        "AZURE_SEARCH_CONSIGNEE_FIELD": "consignee_code",
        "AZURE_SEARCH_CONSIGNEE_IS_COLLECTION": "false",
    }

    new_lines = []
    keys_updated = set()

    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue

        valid = False
        parts = stripped.split("=", 1)
        if len(parts) == 2:
            key, val = parts
            key = key.strip()
            if key in updates:
                new_str = f"{key}={updates[key]}\n"
                new_lines.append(new_str)
                keys_updated.add(key)
                valid = True

        if not valid:
            new_lines.append(line)

    # Append missing
    for k, v in updates.items():
        if k not in keys_updated:
            new_lines.append(f"{k}={v}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("Updated .env successfully.")
    for k, v in updates.items():
        print(f"Set {k}={v}")


if __name__ == "__main__":
    update_env()
