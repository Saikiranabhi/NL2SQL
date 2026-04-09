import os

# Project structure
structure = {
    "project": [
        "main.py",
        "vanna_setup.py",
        "setup_database.py",
        "seed_memory.py",
        "requirements.txt",
        "README.md",
        "RESULTS.md",
        ".env",
        ".gitignore",
        "Dockerfile",
        ".dockerignore"
    ],
    "project/utils": [
        "__init__.py",
        "validator.py",
        "formatter.py",
        "charts.py"
    ]
}

def create_structure():
    for folder, files in structure.items():
        os.makedirs(folder, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(folder, file)
            
            # Create empty file if not exists
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    pass

    print("✅ Project structure created successfully!")

if __name__ == "__main__":
    create_structure()