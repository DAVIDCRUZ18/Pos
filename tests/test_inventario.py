import pytest
import os
import sqlite3
from app.db.database import crear_tablas, get_db
from app.logic.inventario_logic import InventarioLogic

# Configurar una base de datos de prueba temporal
TEST_DB = "test_pos.db"

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    # Cambiar el nombre de la base de datos en el módulo database para los tests
    monkeypatch.setattr("app.db.database.DATABASE_NAME", TEST_DB)
    
    # Crear las tablas en la BD de prueba
    crear_tablas()
    
    yield
    
    # Limpiar después de los tests
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_crear_y_obtener_producto():
    # 1. Crear producto
    InventarioLogic.crear_producto(
        codigo="12345",
        nombre="Producto Test",
        categoria="Test",
        precio=100.0,
        costo=50.0,
        stock=10,
        min_stock=5,
        proveedor="Proveedor Test"
    )
    
    # 2. Obtener productos
    productos = InventarioLogic.obtener_productos()
    
    # 3. Validar
    assert len(productos) == 1
    assert productos[0]['nombre'] == "Producto Test"
    assert productos[0]['codigo_barras'] == "12345"
    assert productos[0]['precio'] == 100.0

def test_ajustar_stock():
    # Crear producto inicial
    InventarioLogic.crear_producto("001", "Item", "Cat", 10, 5, 20, 5, "Prov")
    producto = InventarioLogic.obtener_producto_por_codigo("001")
    
    # Ajustar stock (salida)
    InventarioLogic.ajustar_stock(producto['id'], 5, tipo='salida')
    
    # Verificar
    actualizado = InventarioLogic.obtener_producto_por_id(producto['id'])
    assert actualizado['stock'] == 15

def test_ajustar_stock_insuficiente():
    InventarioLogic.crear_producto("002", "Item2", "Cat", 10, 5, 5, 2, "Prov")
    producto = InventarioLogic.obtener_producto_por_codigo("002")
    
    # Intentar sacar más de lo que hay
    with pytest.raises(ValueError, match="Stock insuficiente"):
        InventarioLogic.ajustar_stock(producto['id'], 10, tipo='salida')
