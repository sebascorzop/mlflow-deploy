#!/bin/bash
# Script de prueba local del pipeline completo

echo "╔════════════════════════════════════════════╗"
echo "║   PRUEBA LOCAL DEL PIPELINE ML + MLFLOW   ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# 1. Verificar Python
echo "1️⃣  Verificando Python..."
python --version
print_status $? "Python encontrado"
echo ""

# 2. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "2️⃣  Creando entorno virtual..."
    python -m venv venv
    print_status $? "Entorno virtual creado"
else
    echo "2️⃣  Entorno virtual ya existe"
fi
echo ""

# 3. Activar entorno virtual
echo "3️⃣  Activando entorno virtual..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
print_status $? "Entorno activado"
echo ""

# 4. Instalar dependencias
echo "4️⃣  Instalando dependencias..."
make install
print_status $? "Dependencias instaladas"
echo ""

# 5. Limpiar archivos previos
echo "5️⃣  Limpiando archivos previos..."
make clean
print_status $? "Limpieza completada"
echo ""

# 6. Entrenar modelo
echo "6️⃣  Entrenando modelo..."
make train
TRAIN_EXIT=$?
print_status $TRAIN_EXIT "Entrenamiento completado"
echo ""

# 7. Validar modelo
if [ $TRAIN_EXIT -eq 0 ]; then
    echo "7️⃣  Validando modelo..."
    make validate
    VALIDATE_EXIT=$?
    print_status $VALIDATE_EXIT "Validación completada"
    echo ""
else
    echo -e "${RED}❌ No se puede validar: el entrenamiento falló${NC}"
    exit 1
fi

# 8. Verificar archivos generados
echo "8️⃣  Verificando archivos generados..."
if [ -f "model.pkl" ]; then
    echo -e "${GREEN}   ✅ model.pkl${NC}"
    ls -lh model.pkl
else
    echo -e "${RED}   ❌ model.pkl no encontrado${NC}"
fi

if [ -d "mlruns" ]; then
    echo -e "${GREEN}   ✅ mlruns/${NC}"
    echo "   Experimentos registrados:"
    ls -la mlruns/
else
    echo -e "${RED}   ❌ mlruns/ no encontrado${NC}"
fi
echo ""

# 9. Resumen
echo "╔════════════════════════════════════════════╗"
echo "║           RESUMEN DEL PIPELINE             ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "📊 Estado del Pipeline:"
if [ $VALIDATE_EXIT -eq 0 ]; then
    echo -e "${GREEN}   ✅ EXITOSO - Modelo validado y listo${NC}"
    echo ""
    echo "📁 Archivos generados:"
    echo "   - model.pkl (modelo serializado)"
    echo "   - mlruns/ (logs de MLflow)"
    echo ""
    echo "🚀 Próximos pasos:"
    echo "   1. Ver experimentos: mlflow ui"
    echo "   2. Abrir http://localhost:5000"
    echo "   3. Commit y push al repositorio"
else
    echo -e "${RED}   ❌ FALLIDO - El modelo no pasó validación${NC}"
fi
echo ""
echo "════════════════════════════════════════════"
