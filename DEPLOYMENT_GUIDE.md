# 🚀 Guía Rápida de Deployment

## 📦 Archivos del Proyecto

El proyecto completo está en la carpeta `mlflow-deploy/` con esta estructura:

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
├── .gitignore                # Archivos a ignorar en Git
├── README.md                 # Documentación completa
└── test_pipeline.sh          # Script de prueba local
```

## 🏁 Pasos para Desplegar

### 1. Crear Repositorio en GitHub

```bash
# En GitHub, crear nuevo repositorio llamado "mlflow-deploy"
# NO inicializar con README
```

### 2. Subir Código al Repositorio

```bash
cd mlflow-deploy

# Inicializar Git
git init
git add .
git commit -m "Initial commit: MLflow CI/CD pipeline"

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/mlflow-deploy.git
git branch -M main
git push -u origin main
```

### 3. Verificar GitHub Actions

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Deberías ver el workflow "CI/CD para ML con MLflow" ejecutándose
4. Espera a que complete (todos los pasos en verde ✅)

### 4. Descargar Artifacts

Si el pipeline fue exitoso:
1. En la página del workflow, scroll hasta "Artifacts"
2. Descargar:
   - `modelo-validado` (model.pkl)
   - `mlflow-logs` (carpeta mlruns/)

## 🧪 Prueba Local

Antes de hacer push, prueba localmente:

```bash
cd mlflow-deploy

# Dar permisos al script
chmod +x test_pipeline.sh

# Ejecutar prueba completa
./test_pipeline.sh
```

Este script:
- ✅ Crea entorno virtual
- ✅ Instala dependencias
- ✅ Limpia archivos previos
- ✅ Ejecuta entrenamiento
- ✅ Valida modelo
- ✅ Verifica archivos generados
- ✅ Muestra resumen

## 📊 Ver Experimentos en MLflow

Después de ejecutar localmente:

```bash
mlflow ui
```

Abre http://localhost:5000 para ver:
- Experimentos registrados
- Métricas (MSE, n_features, etc.)
- Parámetros del modelo
- Artifacts guardados

## 🔧 Comandos Útiles

```bash
# Instalar dependencias
make install

# Entrenar modelo
make train

# Validar modelo
make validate

# Pipeline completo
make all

# Limpiar archivos generados
make clean
```

## ⚠️ Troubleshooting

### Error: "No module named 'mlflow'"
```bash
pip install -r requirements.txt
```

### Error: "model.pkl not found"
```bash
# Ejecutar primero:
make train
```

### Error en GitHub Actions
1. Revisar logs del workflow
2. Verificar que requirements.txt está incluido
3. Verificar que la estructura de carpetas es correcta

### Modelo no pasa validación (MSE > 5000)
El modelo entrenado con LinearRegression en el dataset Diabetes
debería tener un MSE alrededor de 2900, por debajo del umbral de 5000.

Si falla:
- Verificar que el dataset se carga correctamente
- Revisar el random_state (debe ser 42 en ambos scripts)
- Ajustar el umbral en `src/validate.py` si es necesario

## 📝 Modificaciones Comunes

### Cambiar el dataset

Edita `src/train.py` y `src/validate.py`:

```python
# En lugar de:
from sklearn.datasets import load_diabetes
X, y = load_diabetes(return_X_y=True)

# Usa:
from sklearn.datasets import load_boston  # u otro
X, y = load_boston(return_X_y=True)
```

### Cambiar el modelo

Edita `src/train.py`:

```python
# En lugar de:
from sklearn.linear_model import LinearRegression
model = LinearRegression()

# Usa:
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
```

### Ajustar umbral de validación

Edita `src/validate.py`, línea 13:

```python
MSE_THRESHOLD = 5000.0  # Cambia este valor
```

## 🎯 Checklist de Entrega

- [ ] Código subido a GitHub
- [ ] Workflow ejecutado exitosamente
- [ ] Artifacts generados y descargados
- [ ] MLflow UI funciona localmente
- [ ] README.md completo
- [ ] Documento Word con capturas
- [ ] 5 capturas de pantalla:
  - [ ] Workflow exitoso en GitHub
  - [ ] Logs de entrenamiento
  - [ ] Logs de validación
  - [ ] Artifacts descargados
  - [ ] MLflow UI con experimentos

## 📚 Recursos Adicionales

- **MLflow Docs**: https://www.mlflow.org/docs/latest/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Scikit-learn**: https://scikit-learn.org/

## 👤 Contacto

Sebastian Corzo Penha  
Universidad EAN - Maestría en Ciencia de Datos

---
**Nota**: Este proyecto está listo para usar. Solo necesitas:
1. Crear repo en GitHub
2. Push del código
3. Ver el workflow ejecutarse automáticamente
