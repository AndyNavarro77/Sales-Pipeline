-- ============================================================
-- Sales Pipeline — Database Schema
-- Author: Andrés Navarro
-- GitHub: https://github.com/AndyNavarro77/Sales-Pipeline
-- ============================================================

-- Create and select database
CREATE DATABASE IF NOT EXISTS sales_pipeline
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sales_pipeline;

-- ============================================================
-- TABLE: ventas
-- Main transactions table. New records are appended on each
-- pipeline run (append mode).
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    fecha           DATETIME            NOT NULL,
    producto        VARCHAR(100)        NOT NULL,
    categoria       VARCHAR(100)        NOT NULL,
    cantidad        INT                 NOT NULL,
    precio_unitario DECIMAL(10, 2)      NOT NULL,
    canal           VARCHAR(50)         NOT NULL,
    vendedor        VARCHAR(100)        NOT NULL,
    cliente_id      INT                 NOT NULL,
    revenue         DECIMAL(10, 2)      NOT NULL,
    created_at      TIMESTAMP           DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: ventas_por_dia
-- Daily revenue aggregation. Replaced on each pipeline run.
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_por_dia (
    fecha           DATE                NOT NULL,
    revenue         DECIMAL(12, 2)      NOT NULL,
    PRIMARY KEY (fecha)
);

-- ============================================================
-- TABLE: ventas_por_producto
-- Revenue aggregation by product. Replaced on each run.
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_por_producto (
    producto        VARCHAR(100)        NOT NULL,
    revenue         DECIMAL(12, 2)      NOT NULL,
    PRIMARY KEY (producto)
);

-- ============================================================
-- TABLE: ventas_por_vendedor
-- Revenue aggregation by sales rep. Replaced on each run.
-- Used by the alert engine to detect underperforming reps.
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_por_vendedor (
    vendedor        VARCHAR(100)        NOT NULL,
    revenue         DECIMAL(12, 2)      NOT NULL,
    PRIMARY KEY (vendedor)
);

-- ============================================================
-- TABLE: ventas_por_canal
-- Revenue aggregation by sales channel. Replaced on each run.
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_por_canal (
    canal           VARCHAR(50)         NOT NULL,
    revenue         DECIMAL(12, 2)      NOT NULL,
    PRIMARY KEY (canal)
);

-- ============================================================
-- USEFUL QUERIES
-- ============================================================

-- Top 5 products by revenue
-- SELECT producto, revenue
-- FROM ventas_por_producto
-- ORDER BY revenue DESC
-- LIMIT 5;

-- Underperforming reps (below 50% of average)
-- SELECT vendedor, revenue
-- FROM ventas_por_vendedor
-- WHERE revenue < (SELECT AVG(revenue) * 0.5 FROM ventas_por_vendedor);

-- Daily revenue trend (last 30 days)
-- SELECT fecha, revenue
-- FROM ventas_por_dia
-- ORDER BY fecha DESC
-- LIMIT 30;

-- Channel distribution
-- SELECT canal, revenue,
--        ROUND(revenue / SUM(revenue) OVER() * 100, 2) AS pct
-- FROM ventas_por_canal;