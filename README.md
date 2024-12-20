# water_FreshDB

Este proyecto es un sistema de gestión de distribución de productos para una empresa de agua potable. Permite gestionar pedidos, productos, clientes, proveedores, conductores y rutas de distribución. La base de datos está diseñada para optimizar la administración de los componentes, productos y las órdenes.

### Características
- Agregar nuevos productos, componentes y proveedores.
- Ver productos y componentes asociados.
- Realizar pedidos y asociar productos a esos pedidos.
- Gestionar la información de los clientes y conductores.
- Obtener relaciones entre productos, componentes y proveedores utilizando INNER JOIN.

## Uso

### Para utilizar este proyecto, sigue estos pasos:

1. Clona el repositorio a tu máquina local utilizando el siguiente comando:

## Copiar código
```
git clone https://github.com/J0sephT/water_FreshDB.git
```


2. Abre el proyecto en tu editor de código preferido.

3. Configura el motor de base de datos (no incluido en este repositorio) para la comunicación con la base de datos, asegúrate de tener las rutas correctas.

4. Abre tu terminal y navega al directorio de tu proyecto.

5. Ejecuta la API de Flask:

```
python run.py
```


6. Abre Postman o cualquier herramienta similar para realizar peticiones a las rutas de la API.

## Tecnologías Utilizadas
- Python
- Flask
- SQLAlchemy
- Marshmallow
- MySQL

### Dependencias

Para instalar las dependencias necesarias, puedes utilizar el siguiente comando:
```
pip install -r requirements.txt
```


## Esquema de base de datos

La base de datos contiene las siguientes tablas principales:

### Tabla: Driver (Conductor)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Driver_ID    | INT       | PRIMARY KEY       |
| Name         | VARCHAR   | NOT NULL          |
| Phone        | VARCHAR   | NOT NULL          |
| Email        | VARCHAR   | NOT NULL          |
| ID_Number    | VARCHAR   | NOT NULL          |

### Tabla: Customer (Cliente)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Customer_ID  | INT       | PRIMARY KEY       |
| Name         | VARCHAR   | NOT NULL          |
| Address      | VARCHAR   | NOT NULL          |
| Phone        | VARCHAR   | NOT NULL          |
| Email        | VARCHAR   | NOT NULL          |

### Tabla: Product (Producto)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Product_ID   | INT       | PRIMARY KEY       |
| Product_Name | VARCHAR   | NOT NULL          |
| Description  | TEXT      | NOT NULL          |
| Price        | DECIMAL   | NOT NULL          |
| Stock        | INT       | NOT NULL          |

### Tabla: Component (Componente)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Component_ID | INT       | PRIMARY KEY       |
| Component_Name | VARCHAR | NOT NULL          |
| Description  | TEXT      |                   |

### Tabla: Supplier (Proveedor)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Supplier_ID  | INT       | PRIMARY KEY       |
| Supplier_Name| VARCHAR   | NOT NULL          |
| Phone        | VARCHAR   |                   |
| Email        | VARCHAR   |                   |

### Tabla: Order (Pedido)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Order_ID     | INT       | PRIMARY KEY       |
| Date         | DATE      | NOT NULL          |
| Status       | VARCHAR   | NOT NULL          |
| Customer_ID  | INT       | FOREIGN KEY       |
| Driver_ID    | INT       | FOREIGN KEY       |

### Tabla: OrderProduct (Producto en Pedido)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Order_Product_ID | INT    | PRIMARY KEY       |
| Order_ID     | INT       | FOREIGN KEY       |
| Product_ID   | INT       | FOREIGN KEY       |
| Quantity     | INT       | NOT NULL          |

### Tabla: ProductComponent (Componente de Producto)
| Campo        | Tipo      | Restricciones     |
|--------------|-----------|-------------------|
| Product_Component_ID | INT | PRIMARY KEY       |
| Product_ID   | INT       | FOREIGN KEY       |
| Component_ID | INT       | FOREIGN KEY       |
| Quantity     | INT       | NOT NULL          |

## Cómo hacer consultas INNER JOIN

Para realizar consultas INNER JOIN entre las tablas, puedes utilizar las siguientes rutas de la API:

- **Obtener los pedidos con detalles de productos asociados:**

```
GET /orders_with_details
```

- **Obtener los productos asociados a un pedido específico:**

```
GET /order_products_with_details
```

- **Obtener los componentes asociados a un producto específico:**
```
GET /product/{product_id}/components
```

## Ejemplo de Consultas con INNER JOIN

- Obtener los pedidos junto con los detalles de los productos asociados:

```bash
GET http://127.0.0.1:5000/orders_with_details


