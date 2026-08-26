import os
import tarfile
import io
import base64

def exclude_filter(tarinfo):
    name = tarinfo.name
    if any(x in name for x in ['node_modules', '.venv', 'venv', '__pycache__', '.pytest_cache', '.astro', 'dist', '.git', '.sqlite', '.db']):
        return None
    return tarinfo

bio = io.BytesIO()
with tarfile.open(fileobj=bio, mode='w:gz') as tar:
    tar.add('bot_trading', arcname='bot_trading', filter=exclude_filter)

bio.seek(0)
b64_data = base64.b64encode(bio.read()).decode('utf-8')

installer = f'''#!/bin/bash
set -e
echo "=================================================="
echo "🚀 ACTUALIZANDO MOTOR GOLD-EX EN LA VM (PRODUCCIÓN)"
echo "=================================================="

mkdir -p ~/app/autooro
cd ~/app/autooro

echo "📦 1/2 Desempaquetando archivos del proyecto..."
echo "{b64_data}" | base64 -d | tar -xzf -

cd bot_trading

echo "🐳 2/2 Reconstruyendo y levantando contenedores Docker..."
sudo docker compose down --remove-orphans || true
sudo docker compose up -d --build

echo ""
echo "=================================================="
echo "✅ ¡DESPLIEGUE COMPLETADO CON ÉXITO EN LA VM!"
echo "=================================================="
echo "📊 Dashboard Terminal: http://34.175.69.118:4321"
echo "⚙️ API Backend Docs:  http://34.175.69.118:8000/docs"
'''

with open('deploy_standalone.sh', 'w', encoding='utf-8', newline='\n') as f:
    f.write(installer)

print(f"Standalone installer generated: {len(installer)} bytes")
