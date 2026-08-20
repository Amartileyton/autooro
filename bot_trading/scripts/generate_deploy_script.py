import base64
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

with open("bot_session.session", "rb") as f:
    session_b64 = base64.b64encode(f.read()).decode("utf-8")

with open(".env", "r", encoding="utf-8") as f:
    env_content = f.read()

script_content = f"""#!/bin/bash
set -e

echo "=================================================="
echo "🚀 DESPLEGANDO MOTOR DE TRADING GOLD-EX EN GCP"
echo "=================================================="

# 1. Instalar dependencias del sistema y Docker
echo "📦 1/4 Instalando Docker, Docker Compose y Git..."
sudo apt-get update -qq
sudo apt-get install -y -qq docker.io docker-compose git curl

sudo systemctl enable --now docker

# 2. Clonar el repositorio
echo "📥 2/4 Descargando código del repositorio GitHub..."
mkdir -p ~/app
cd ~/app
if [ -d "autooro" ]; then
    cd autooro
    git pull origin main
else
    git clone https://github.com/Amartileyton/autooro.git
    cd autooro
fi

cd bot_trading

# 3. Configurar .env y restaurar sesión pre-autenticada de Telethon
echo "🔑 3/4 Configurando credenciales y sesión autenticada..."
cat << 'EOF' > .env
{env_content}
EOF

# Desempaquetar sesión binaria de Telethon
echo "{session_b64}" | base64 -d > bot_session.session
chmod 600 bot_session.session

# 4. Construir y levantar contenedores Docker en segundo plano
echo "🐳 4/4 Construyendo y levantando contenedores en segundo plano..."
sudo docker-compose down --remove-orphans || true
sudo docker-compose up -d --build

echo ""
echo "=================================================="
echo "✅ ¡DESPLIEGUE COMPLETADO CON ÉXITO!"
echo "=================================================="
echo "📊 Dashboard Obsidian Terminal: http://34.175.69.118:4321"
echo "⚙️ Backend API Swagger Docs:   http://34.175.69.118:8000/docs"
echo "🤖 Telegram Admin Bot:         Activo y conectado a tu cuenta"
echo "=================================================="
echo ""
sudo docker ps
"""

with open("deploy_to_gcp.sh", "w", encoding="utf-8") as f:
    f.write(script_content)

print("✅ Archivo 'deploy_to_gcp.sh' generado con éxito.")
