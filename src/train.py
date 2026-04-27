"""
Script de entrenamiento de modelo con MLflow
Entrena un modelo de regresión lineal con el dataset Diabetes
y lo registra en MLflow y como archivo .pkl
"""

import os
import sys
import joblib
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def main():
    print("=" * 60)
    print("ENTRENAMIENTO DEL MODELO")
    print("=" * 60)
    
    # Configuración de MLflow
    workspace_dir = os.getcwd()
    mlruns_dir = os.path.join(workspace_dir, "mlruns")
    tracking_uri = f"file://{os.path.abspath(mlruns_dir)}"
    
    print(f"📁 Directorio de trabajo: {workspace_dir}")
    print(f"📊 MLflow tracking URI: {tracking_uri}")
    
    # Crear directorio mlruns si no existe
    os.makedirs(mlruns_dir, exist_ok=True)
    
    # Configurar MLflow
    mlflow.set_tracking_uri(tracking_uri)
    experiment_name = "CI-CD-Lab2"
    
    # Crear o obtener experimento
    try:
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"✅ Experimento '{experiment_name}' creado")
    except mlflow.exceptions.MlflowException:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        experiment_id = experiment.experiment_id
        print(f"✅ Usando experimento existente '{experiment_name}'")
    
    # Cargar datos
    print("\n📥 Cargando dataset Diabetes...")
    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   - Muestras de entrenamiento: {X_train.shape[0]}")
    print(f"   - Muestras de prueba: {X_test.shape[0]}")
    print(f"   - Features: {X_train.shape[1]}")
    
    # Entrenar modelo
    print("\n🤖 Entrenando modelo de regresión lineal...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluar modelo
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"📊 MSE en test: {mse:.4f}")
    
    # Registrar en MLflow
    print("\n📝 Registrando en MLflow...")
    with mlflow.start_run(experiment_id=experiment_id) as run:
        # Log de métricas
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("n_features", X_train.shape[1])
        mlflow.log_metric("n_samples_train", X_train.shape[0])
        mlflow.log_metric("n_samples_test", X_test.shape[0])
        
        # Log de parámetros
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        
        # Log del modelo en MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
        )
        
        print(f"   ✅ Run ID: {run.info.run_id}")
        print(f"   ✅ Artifact URI: {run.info.artifact_uri}")
    
    # Guardar modelo como .pkl para validación
    model_path = os.path.join(workspace_dir, "model.pkl")
    print(f"\n💾 Guardando modelo en: {model_path}")
    joblib.dump(model, model_path)
    
    print("\n" + "=" * 60)
    print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print(f"📊 MSE: {mse:.4f}")
    print(f"📁 Modelo guardado: model.pkl")
    print(f"📁 MLflow logs: mlruns/")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
