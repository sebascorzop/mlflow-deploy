# 🚀 MLflow CI/CD Pipeline

Pipeline automatizado de Machine Learning con entrenamiento, validación y registro de modelos usando MLflow y GitHub Actions.

## 📋 Descripción

Este proyecto implementa un pipeline completo de CI/CD para Machine Learning que:

1. **Entrena** un modelo de regresión lineal con el dataset Diabetes
2. **Registra** el modelo y métricas en MLflow
3. **Valida** que el modelo cumple criterios de calidad (MSE < 5000)
4. **Almacena** el modelo validado como artefacto de GitHub Actions

## 🏗️ Estructura del Proyecto

```
mlflow-deploy/
├── src/
│   ├── train.py              # Script de entrenamiento
│   └── validate.py           # Script de validación
├── .github/
│   └── workflows/
│       └── mlflow-ci.yml     # Workflow de GitHub Actions
├── requirements.txt          # Dependencias Python
├── Makefile                  # Comandos del pipeline
├── .gitignore
└── README.md
```

## 🔧 Requisitos

- Python 3.9+
- pip
- make (opcional, pero recomendado)

## 📦 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/mlflow-deploy.git
cd mlflow-deploy
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
make install
# O directamente:
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar pipeline completo

```bash
make all
```

Este comando ejecuta:
1. `make train` - Entrena el modelo
2. `make validate` - Valida el modelo

### Comandos individuales

```bash
# Solo entrenar
make train

# Solo validar (requiere modelo entrenado)
make validate

# Limpiar archivos generados
make clean
```

## 📊 Scripts Principales

### `src/train.py`

Entrena un modelo de regresión lineal con el dataset Diabetes:

- Carga datos usando `sklearn.datasets.load_diabetes`
- Split 80/20 (train/test)
- Entrena LinearRegression
- Registra en MLflow:
  - Métricas: MSE, n_features, n_samples
  - Parámetros: model_type, test_size, random_state
  - Modelo: guardado en MLflow y como `model.pkl`

**Salida:**
- `model.pkl` - Modelo serializado con joblib
- `mlruns/` - Logs de MLflow

### `src/validate.py`

Valida el modelo entrenado:

- Carga `model.pkl`
- Carga mismo dataset de prueba
- Calcula MSE
- Verifica que MSE ≤ 5000.0
- Exit code 0 si pasa, 1 si falla

## 🤖 GitHub Actions

El workflow se ejecuta automáticamente en cada push a `main` o PR.

### Pasos del workflow:

1. **Setup** - Clona repo, configura Python 3.9
2. **Install** - Instala dependencias
3. **Train** - Ejecuta entrenamiento
4. **Validate** - Valida el modelo
5. **Artifact Upload** - Sube modelo y logs

### Artefactos generados:

- `modelo-validado` - Archivo model.pkl (30 días)
- `mlflow-logs` - Logs completos de MLflow (7 días)

### Ver resultados:

1. Ve a la pestaña "Actions" en GitHub
2. Click en el workflow más reciente
3. Revisa los logs de cada paso
4. Descarga artefactos si el pipeline fue exitoso

## 📈 MLflow UI (Local)

Para ver los experimentos registrados localmente:

```bash
mlflow ui
```

Abre http://localhost:5000 en tu navegador.

Verás:
- Experimentos
- Runs con métricas
- Modelos registrados
- Parámetros
- Artefactos

## 🎯 Criterios de Validación

El modelo debe cumplir:

| Métrica | Umbral | Descripción |
|---------|--------|-------------|
| MSE | ≤ 5000.0 | Error cuadrático medio en test set |

Si el modelo NO cumple:
- El pipeline se detiene con exit code 1
- No se genera artefacto de modelo validado
- GitHub Actions marca el workflow como fallido

## 🔍 Troubleshooting

### Error: "No module named mlflow"

```bash
pip install -r requirements.txt
```

### Error: "model.pkl not found"

Ejecuta primero:
```bash
make train
```

### Error: "MSE excede umbral"

El modelo no cumple calidad. Opciones:
- Aumentar el umbral en `src/validate.py` (línea 13)
- Mejorar el modelo en `src/train.py`

### MLflow tracking error

Verifica que existe el directorio:
```bash
mkdir -p mlruns
```

## 📝 Modificaciones Comunes

### Cambiar el umbral de MSE

Edita `src/validate.py`:
```python
MSE_THRESHOLD = 5000.0  # Cambia este valor
```

### Usar otro modelo

Edita `src/train.py`:
```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)
```

### Cambiar dataset

Edita ambos scripts:
```python
from sklearn.datasets import load_boston  # u otro

X, y = load_boston(return_X_y=True)
```

## 🧪 Testing

```bash
# Test rápido (solo entrenamiento)
make test

# Pipeline completo
make all

# Limpiar y ejecutar desde cero
make clean && make all
```

## 📚 Recursos

- [MLflow Documentation](https://www.mlflow.org/docs/latest/index.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)

## 👤 Autor

Sebastian Corzo Penha  
Universidad EAN - Maestría en Ciencia de Datos

## 📄 Licencia

Este proyecto es para fines educativos.

## 🎓 Contexto Académico

Proyecto desarrollado como parte del curso de MLOps, demostrando:
- Integración continua (CI) para ML
- Registro de modelos con MLflow
- Validación automatizada
- Pipelines reproducibles
- Gestión de artefactos
