CREATE DATABASE SISTEMA_VENTA_PYTHON;
GO

USE SISTEMA_VENTA_PYTHON;
GO

CREATE TABLE USUARIO (
    IdUsuario INT PRIMARY KEY IDENTITY,
    Documento VARCHAR(50),
    NombreCompleto VARCHAR(50),
    Clave VARCHAR(50),
    Estado BIT,
    FechaRegistro DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE CATEGORIA (
    IdCategoria INT PRIMARY KEY IDENTITY,
    Descripcion VARCHAR(50),
    Estado BIT,
    FechaRegistro DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE PRODUCTO (
    IdProducto INT PRIMARY KEY IDENTITY,
    Codigo VARCHAR(50),
    Nombre VARCHAR(50),
    Descripcion VARCHAR(50),
    IdCategoria INT,
    Precio DECIMAL(10,2) DEFAULT 0,
    Stock INT NOT NULL DEFAULT 0,
    Estado BIT,
    FechaRegistro DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdCategoria) REFERENCES CATEGORIA(IdCategoria)
);
GO

CREATE TABLE VENTA (
    IdVenta INT PRIMARY KEY IDENTITY,
    MontoPago DECIMAL(10,2) DEFAULT 0,
    MontoCambio DECIMAL(10,2) DEFAULT 0,
    MontoTotal DECIMAL(10,2),
    FechaRegistro DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE DETALLE_VENTA (
    IdDetalleVenta INT PRIMARY KEY IDENTITY,
    IdVenta INT,
    IdProducto INT,
    PrecioVenta DECIMAL(10,2) DEFAULT 0,
    Cantidad INT,
    SubTotal DECIMAL(10,2),
    FechaRegistro DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdVenta) REFERENCES VENTA(IdVenta),
    FOREIGN KEY (IdProducto) REFERENCES PRODUCTO(IdProducto)
);
GO
