import os

folders = ['data', 'pipelines', 'models', 'src', 'steps']
for folder in folders:
    os.makedirs(folder, exist_ok=True)