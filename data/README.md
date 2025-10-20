# NYC-TLC-Trip-Record-Data-Analysis
This is an attempt to recover data from NYC TLC Trip Record Data using SPARK to Ingest, Transform and Export this data to a lakehouse (Snowflake) in order to keep this tables on the cloud (roughly 15 gb of data) to then use SQL by connecting vscode to Snowflake and answer 20 simple questions about the data.

# Arquitectura

                    +--------------------+
                    |   Usuario / Dev    |
                    |  (JupyterLab UI)   |
                    +---------+----------+
                              |
                              | PySpark / notebooks
                              v
+----------------+     +----------------------+     +---------------------------+
|  Datos origen  | --> |   Spark (ETL / ELT)  | --> |  Snowflake (COMPUTE_WH)   |
|  (GREEN/YELLOW)|     |  - lectura desde SF  |     |  - BRONZE.ENRICHED_TRIPS  |
+----------------+     |  - limpieza, uniones |     |  - analítica: ANALYTICS   |
                       |  - enriquecimiento   |     |    .OBT_TRIPS (CREATE AS) |
                       |  - agregaciones / AQ |     +---------------------------+
                       |  - escribir resultados|
                       +----------------------+
                                                     
# Tabla de la Arquitectura

| Componente                          |                                                                                                                                                         Rol / Qué hace | Tecnologías / Notas                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------ |
| Usuario / Dev                       |                                                                                                       Orquestar y desarrollar análisis, lanzar DDL/ETL desde notebooks | JupyterLab (en Docker), Python, PySpark                                              |
| Spark (notebook)                    | Ejecuta ETL: unifica `GREEN_TRIPS` + `YELLOW_TRIPS`, timezone, enrich con `TAXI_ZONES`, calcula `TRIP_DURATION_MIN`, `AVG_SPEED_MPH`, `TIP_PCT` y persiste a Snowflake | PySpark, spark-snowflake connector (o `snowflake-connector-python` para DDL directo) |
| Snowflake — RAW (COMPUTE_WH.BRONZE) |                                                                                             Almacena la capa raw/bronze `ENRICHED_TRIPS` (fuente única para analítica) | Snowflake (warehouse, schema BRONZE)                                                 |
| Snowflake — ANALYTICS               |                                                         Capa analítica: tabla `ANALYTICS.OBT_TRIPS` creada con SQL (CTE / CREATE TABLE AS) para consultas y dashboards | Snowflake (schema ANALYTICS), optimizar con clustering por YEAR, MONTH               |
| Export / UX                         |                                                                                                                            Exportar resultados (Excel) y bajar al host | pandas, openpyxl, Jupyter FileLink / docker cp / volumenes Docker                    |


# Matriz de cobertura mes a mes — Yellow y Green (2015–2025) [x] Tarea completada 100%

**Contexto**: Cargados todos los meses 2015–2025 (Parquet) de Yellow y Green. Esta tabla muestra la cobertura mes a mes por servicio. ✓ = mes cargado (cover), X = mes no cargado.

**Nota**: Todos los meses fueron subidos.

## Leyenda

* ✓ : Mes con datos cargados
* X : Mes sin datos

---

## Matriz — Servicio: YELLOW

|  Año | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
| ---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 2015 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2016 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2017 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2018 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2019 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2020 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2021 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2022 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2023 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2024 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2025 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  X  |  X  |  X  |  X  |

---

## Matriz — Servicio: GREEN

|  Año | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
| ---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 2015 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2016 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2017 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2018 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2019 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2020 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2021 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2022 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2023 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2024 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |
| 2025 |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  ✓  |  X  |  X  |  X  |  X  |

---

## Pasos para docker compose

| Elemento                            | Explicación breve                                                                                                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **image: jupyter/pyspark-notebook** | Usa la imagen oficial de Jupyter con Spark y Python ya preinstalados. Ideal para análisis con PySpark.                                                                |
| **container_name: pyspark-vscode**  | Nombre fijo del contenedor (así lo puedes referir con comandos como `docker exec -it pyspark-vscode bash`).                                                           |
| **ports: "8888:8888"**              | Expone el puerto 8888 del contenedor al 8888 de tu máquina local → permite acceder a Jupyter desde el navegador en `http://localhost:8888`.                           |
| **volumes: .:/home/jovyan/work**    | Monta la carpeta actual (`.`) de tu host dentro del contenedor en `/home/jovyan/work`. Todo lo que guardes ahí se sincroniza automáticamente con tu máquina.          |
| **environment:**                    | Variables de entorno.                                                                                                                                                 |
| **PYSPARK_SUBMIT_ARGS**             | Configura PySpark para incluir los conectores necesarios para trabajar con **Snowflake** (`spark-snowflake` y `snowflake-jdbc`) cuando se inicializa la sesión Spark. |



## Variables de ambiente

Las usamos para conectarnos a Snowflake, las variables son las siguientes:

SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WH=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_ROLE=
SNOWFLAKE_URL=""


## Diseño raw y OBT

| Etapa               | Descripción                                                                                                                        | Ejemplo en tu caso                                                                                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **RAW / BRONZE**    | Capa **de ingesta cruda**: los datos se cargan tal como vienen del origen (TLC, CSV, API, etc.), con mínima transformación.        | `BRONZE.ENRICHED_TRIPS` contiene viajes con datos originales, timestamps, montos, zonas, etc.                                                                                                                                              |
| **OBT / ANALYTICS** | Capa **analítica o refinada**: se derivan métricas y columnas útiles para análisis de negocio o dashboards. Es una tabla *curada*. | `ANALYTICS.OBT_TRIPS` se crea a partir de `ENRICHED_TRIPS`, añadiendo variables como: <br>• `TRIP_DURATION_MIN` → duración del viaje (minutos)<br>• `AVG_SPEED_MPH` → velocidad promedio (millas/h)<br>• `TIP_PCT` → porcentaje de propina |


## Validaciones

### 1. Nulos por columna

Evalúa la **presencia de valores faltantes** en campos críticos:

* `PICKUP_DATETIME`
* `DROPOFF_DATETIME`
* `TRIP_DISTANCE`
* `FARE_AMOUNT`
* `TOTAL_AMOUNT`
* `PASSENGER_COUNT`
* `PULOCATIONID`
* `DOLOCATIONID`
* `INGEST_RUN_ID`

**Objetivo:** detectar fallas de ingesta, transformaciones incompletas o columnas mal pobladas.

---

### 2. Rangos numéricos

Verifica la **coherencia y plausibilidad** de los valores numéricos:

* `TRIP_DISTANCE`: sin valores negativos ni mayores a **100 millas**.
* `FARE_AMOUNT`: no negativo y menor a **1000 USD**.
* `PASSENGER_COUNT`: entre **1 y 10**.
* `TRIP_DURATION_MIN`: entre **1 y 180 minutos**.
* `AVG_SPEED_MPH`: menor a **100 mph**.

**Objetivo:** identificar outliers o errores de cálculo en las métricas del viaje.

---

### 3. Coherencia temporal

Comprueba la **lógica temporal** de los registros:

* `DROPOFF_DATETIME` no debe ser anterior a `PICKUP_DATETIME`.
* Ninguna fecha debe estar en el futuro.
* Se evalúan los rangos mínimos y máximos de fechas para auditar cobertura temporal.
* Verifica consistencia entre los campos `YEAR` y `MONTH` frente a las fechas reales.

**Objetivo:** detectar inconsistencias temporales y validar la integridad cronológica.

---

### 4. Conteos mensuales por tipo de servicio

Genera **estadísticas agregadas** por año, mes y tipo de servicio (`SERVICE_TYPE`):

* Total de viajes (`COUNT(*)`)
* Total de pasajeros (`SUM(PASSENGER_COUNT)`)
* Promedio de distancia, tarifa y duración
* Ingreso total (`SUM(TOTAL_AMOUNT)`)

**Objetivo:** controlar volumen y consistencia frente a reportes externos o históricos.

---

### 5. Validación de zonas

Evalúa la integridad de los **IDs y nombres de zonas** de pickup y dropoff:

* Conteo de zonas únicas (`PULOCATIONID`, `DOLOCATIONID`)
* Detección de nulos en `PICKUP_ZONE`, `DROPOFF_ZONE`, `BOROUGH`
* Identificación de las zonas más comunes de origen y destino

**Objetivo:** verificar correcta unión con la tabla de referencia `TAXI_ZONES`.

---

### 6. Validación de pagos

Agrupa y resume los viajes por tipo de pago (`PAYMENT_TYPE`):

* Número total de viajes por método
* Promedio de tarifa (`FARE_AMOUNT`)
* Promedio de propina (`TIP_AMOUNT`) y porcentaje (`TIP_PCT`)
* Ingreso total por tipo de pago

**Objetivo:** detectar anomalías en registros financieros o categorización de métodos de pago.

---

### 7. Resumen por tipo de servicio

Consolida estadísticas globales por `SERVICE_TYPE`:

* Total de viajes
* Cantidad de `VENDORID` únicos
* Promedio de distancia, duración y pasajeros
* Ingreso total agregado

**Objetivo:** comparar el rendimiento y la consistencia de las fuentes **Yellow** y **Green** dentro del pipeline analítico.

---

