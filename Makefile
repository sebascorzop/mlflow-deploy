.PHONY: install train validate clean test all

# Instalar dependencias
install:
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt
	@echo "✅ Dependencias instaladas"

# Entrenar modelo
train:
	@echo "🚀 Iniciando entrenamiento..."
	python src/train.py

# Validar modelo
validate:
	@echo "🔍 Iniciando validación..."
	python src/validate.py

# Limpiar archivos generados
clean:
	@echo "🧹 Limpiando archivos generados..."
	rm -rf model.pkl
	rm -rf mlruns/
	rm -rf __pycache__
	rm -rf src/__pycache__
	@echo "✅ Limpieza completada"

# Ejecutar pipeline completo
all: train validate
	@echo "✅ Pipeline completo ejecutado"

# Test rápido (sin validación)
test: train
	@echo "✅ Test de entrenamiento completado"
