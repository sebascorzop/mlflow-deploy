"""
Script de validación de modelo
Carga el modelo entrenado y valida que cumple con el umbral de calidad
"""

import os
import sys
import joblib
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Umbral de MSE para considerar el modelo válido
MSE_THRESHOLD = 5000.0

def main():
    print("=" * 60)
    print("VALIDACIÓN DEL MODELO")
    print("=" * 60)
    
    workspace_dir = os.getcwd()
    model_path = os.path.join(workspace_dir, "model.pkl")
    
    # Verificar que existe el modelo
    print(f"\n🔍 Buscando modelo en: {model_path}")
    if not os.path.exists(model_path):
        print(f"❌ ERROR: No se encontró el archivo model.pkl")
        print(f"   Asegúrate de ejecutar 'make train' primero")
        return 1
    
    # Cargar modelo
    print("📥 Cargando modelo...")
    try:
        model = joblib.load(model_path)
        print(f"   ✅ Modelo cargado correctamente")
        print(f"   - Tipo: {type(model).__name__}")
        print(f"   - Features esperadas: {model.n_features_in_}")
    except Exception as e:
        print(f"❌ ERROR al cargar el modelo: {e}")
        return 1
    
    # Cargar datos de prueba (mismo split que en entrenamiento)
    print("\n📥 Cargando dataset de prueba...")
    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   - Muestras de prueba: {X_test.shape[0]}")
    print(f"   - Features: {X_test.shape[1]}")
    
    # Validar dimensiones
    if X_test.shape[1] != model.n_features_in_:
        print(f"❌ ERROR: Dimensiones no coinciden")
        print(f"   - Modelo espera: {model.n_features_in_} features")
        print(f"   - Dataset tiene: {X_test.shape[1]} features")
        return 1
    
    # Hacer predicciones
    print("\n🔮 Realizando predicciones...")
    try:
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"   ✅ Predicciones completadas")
    except Exception as e:
        print(f"❌ ERROR durante predicción: {e}")
        return 1
    
    # Validar contra umbral
    print("\n" + "=" * 60)
    print("RESULTADO DE LA VALIDACIÓN")
    print("=" * 60)
    print(f"📊 MSE obtenido: {mse:.4f}")
    print(f"🎯 MSE umbral:   {MSE_THRESHOLD:.4f}")
    print("=" * 60)
    
    if mse <= MSE_THRESHOLD:
        print("✅ VALIDACIÓN EXITOSA")
        print("   El modelo cumple con los criterios de calidad")
        print("   El pipeline puede continuar")
        print("=" * 60)
        return 0
    else:
        print("❌ VALIDACIÓN FALLIDA")
        print(f"   El MSE ({mse:.4f}) supera el umbral ({MSE_THRESHOLD:.4f})")
        print("   El modelo no cumple con los criterios de calidad")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
