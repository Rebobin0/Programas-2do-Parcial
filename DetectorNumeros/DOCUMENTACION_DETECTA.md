# Documentación Técnica: detecta.py
## Sistema de Reconocimiento de Dígitos con Distancia Euclidiana

---

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Fundamentos Teóricos: Distancia Euclidiana](#fundamentos-teóricos-distancia-euclidiana)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Análisis Detallado del Código](#análisis-detallado-del-código)
5. [Flujo de Ejecución](#flujo-de-ejecución)
6. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Introducción

El programa **detecta.py** es un sistema de reconocimiento de dígitos manuscritos que utiliza el método de **distancia euclidiana** para clasificar números. El sistema compara una matriz de entrada (28×28 píxeles) contra patrones predefinidos de los dígitos 0-9 y determina cuál es el número representado.

### Características principales:
- ✅ Reconocimiento de dígitos del 0 al 9
- ✅ Entrada desde archivos Excel (.xlsx) con matrices 28×28
- ✅ Clasificación basada en distancia euclidiana
- ✅ Normalización automática de datos
- ✅ Cálculo de confianza de predicción
- ✅ Salida en lenguaje natural (ej: "siete")

---

## Fundamentos Teóricos: Distancia Euclidiana

### ¿Qué es la Distancia Euclidiana?

La **distancia euclidiana** es una medida de la "diferencia" o "similitud" entre dos puntos en un espacio multidimensional. Es la extensión del teorema de Pitágoras a múltiples dimensiones.

### Fórmula Matemática

Para dos puntos **A** y **B** en un espacio n-dimensional:

```
d(A, B) = √[(a₁ - b₁)² + (a₂ - b₂)² + ... + (aₙ - bₙ)²]
```

O de forma más compacta:

```
d(A, B) = √[Σᵢ₌₁ⁿ (aᵢ - bᵢ)²]
```

### Ejemplo Visual en 2D

Imagina dos puntos en un plano:
- Punto A = (1, 2)
- Punto B = (4, 6)

```
d = √[(4-1)² + (6-2)²]
d = √[3² + 4²]
d = √[9 + 16]
d = √25
d = 5
```

### Aplicación en Reconocimiento de Imágenes

En nuestro caso, cada matriz 28×28 es un "punto" en un espacio de **784 dimensiones** (28 × 28 = 784 píxeles).

#### Ejemplo con matrices pequeñas (3×3):

**Matriz de entrada:**
```
[1, 1, 0]
[1, 0, 0]
[1, 1, 0]
```

**Patrón del número "1":**
```
[1, 1, 0]
[0, 1, 0]
[1, 1, 0]
```

**Cálculo de la distancia:**

1. **Restar elemento por elemento:**
```
Diferencia = Entrada - Patrón

[1-1,  1-1,  0-0]   =   [0,  0,  0]
[1-0,  0-1,  0-0]       [1, -1,  0]
[1-1,  1-1,  0-0]       [0,  0,  0]
```

2. **Elevar al cuadrado cada diferencia:**
```
[0²,   0²,  0²]   =   [0, 0, 0]
[1²,  (-1)², 0²]       [1, 1, 0]
[0²,   0²,  0²]        [0, 0, 0]
```

3. **Sumar todos los elementos:**
```
Suma = 0 + 0 + 0 + 1 + 1 + 0 + 0 + 0 + 0 = 2
```

4. **Calcular la raíz cuadrada:**
```
Distancia = √2 ≈ 1.414
```

**Interpretación:** 
- **Distancia pequeña** → Las matrices son muy parecidas
- **Distancia grande** → Las matrices son muy diferentes

El algoritmo compara la entrada contra TODOS los patrones (0-9) y elige el que tenga la **distancia más pequeña**.

---

## Arquitectura del Sistema

### Estructura de Carpetas

```
DetectorNumeros/
│
├── detecta.py          # Programa principal
├── patrones/           # Carpeta con patrones de referencia
│   ├── num0.xlsx       # Patrón del número 0
│   ├── num1.xlsx       # Patrón del número 1
│   ├── ...
│   └── num9.xlsx       # Patrón del número 9
│
└── input/              # Carpeta con archivos a reconocer
    ├── 7.xlsx          # Ejemplo de entrada
    └── ...
```

### Formato de Archivos

Cada archivo Excel contiene una matriz de 28×28:
- **Valores:** 0 (fondo) y 1 (trazo del número)
- **Dimensión:** Exactamente 28 filas × 28 columnas (784 celdas)

---

## Análisis Detallado del Código

### Clase DetectorNumeros

Esta es la clase principal que encapsula toda la funcionalidad del sistema.

---

### 1. Inicialización (`__init__`)

```python
def __init__(self, ruta_patrones=None):
    # Si no se proporciona ruta, usar la carpeta del script
    if ruta_patrones is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_patrones = os.path.join(script_dir, "patrones")
    
    self.ruta_patrones = ruta_patrones
    self.script_dir = os.path.dirname(os.path.abspath(__file__))
    self.patrones = {}
    self.estadisticas_patrones = {}
    self.numeros_palabras = {
        0: "cero", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro",
        5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve"
    }
    
    print("[INICIALIZANDO] Cargando patrones de dígitos...")
    self._cargar_patrones()
    print("[✓] Patrones cargados correctamente\n")
```

**¿Qué hace este método?**

1. **Determina la ruta de patrones:** Si no se proporciona, usa la subcarpeta `patrones/` en el directorio del script.

2. **Inicializa estructuras de datos:**
   - `self.patrones = {}` → Diccionario que almacenará las matrices 28×28 de cada dígito
   - `self.estadisticas_patrones = {}` → Diccionario con estadísticas (min, max, media, desviación estándar) de cada patrón
   - `self.numeros_palabras = {...}` → Mapeo de números a sus nombres en español

3. **Carga los patrones:** Llama a `_cargar_patrones()` para leer los 10 archivos Excel.

---

### 2. Carga de Patrones (`_cargar_patrones`)

```python
def _cargar_patrones(self):
    """Carga los 10 archivos de patrones (num0.xlsx a num9.xlsx)."""
    for digito in range(10):
        ruta = os.path.join(self.ruta_patrones, f"num{digito}.xlsx")
        
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Patrón no encontrado: {ruta}")
        
        try:
            # Leer el archivo Excel sin headers
            df = pd.read_excel(ruta, sheet_name=0, header=None)
            matriz = df.values.astype(np.float64)
            
            # Validar dimensiones
            if matriz.shape != (28, 28):
                raise ValueError(
                    f"Patrón {digito}: Dimensión incorrecta {matriz.shape}, "
                    f"esperaba (28, 28)"
                )
            
            self.patrones[digito] = matriz
            
            # Calcular estadísticas
            self.estadisticas_patrones[digito] = {
                'min': np.min(matriz),
                'max': np.max(matriz),
                'media': np.mean(matriz),
                'std': np.std(matriz)
            }
            
            print(f"  Patrón {digito}: Cargado ✓ "
                  f"(min={self.estadisticas_patrones[digito]['min']:.2f}, "
                  f"max={self.estadisticas_patrones[digito]['max']:.2f})")
            
        except Exception as e:
            raise Exception(f"Error cargando patrón {digito}: {str(e)}")
```

**Proceso paso a paso:**

1. **Iteración sobre dígitos:** Para cada número del 0 al 9:
   - Construye la ruta del archivo: `patrones/num0.xlsx`, `patrones/num1.xlsx`, etc.

2. **Verificación de existencia:** Comprueba que el archivo exista, si no, lanza error.

3. **Lectura del Excel:**
   - `pd.read_excel(ruta, sheet_name=0, header=None)` → Lee la primera hoja sin considerar encabezados
   - `df.values.astype(np.float64)` → Convierte el DataFrame a un array NumPy de tipo float64

4. **Validación de dimensiones:** Verifica que la matriz sea exactamente 28×28.

5. **Almacenamiento:**
   - `self.patrones[digito] = matriz` → Guarda la matriz en el diccionario

6. **Cálculo de estadísticas:**
   - **min:** Valor mínimo en la matriz (generalmente 0)
   - **max:** Valor máximo en la matriz (generalmente 1)
   - **media:** Promedio de todos los píxeles
   - **std:** Desviación estándar (mide la variabilidad)

7. **Feedback:** Imprime confirmación de carga.

---

### 3. Carga de Entrada (`_cargar_entrada`)

```python
def _cargar_entrada(self, nombre_archivo):
    """
    Carga la matriz de entrada desde un archivo Excel en la carpeta input.
    """
    ruta = os.path.join(self.script_dir, "input", nombre_archivo)
    
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo de entrada no encontrado: {ruta}")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(ruta, sheet_name=0, header=None)
        matriz = df.values.astype(np.float64)
        
        # Validar dimensiones
        if matriz.shape != (28, 28):
            raise ValueError(
                f"Dimensión incorrecta: {matriz.shape}, esperaba (28, 28)"
            )
        
        print(f"[✓] Entrada cargada desde: {ruta}")
        print(f"[✓] Dimensión validada: {matriz.shape}\n")
        
        return matriz
        
    except Exception as e:
        raise Exception(f"Error cargando entrada: {str(e)}")
```

**Funcionamiento:**

1. **Construcción de ruta:** Combina el directorio del script con `input/` y el nombre del archivo.
   - Ejemplo: `input/7.xlsx`

2. **Lectura y validación:** Similar a la carga de patrones, lee el Excel y valida que sea 28×28.

3. **Retorno:** Devuelve la matriz NumPy con los datos.

---

### 4. Normalización (`_normalizar_entrada`)

```python
def _normalizar_entrada(self, matriz_entrada):
    """
    Normaliza la matriz de entrada (0-1) al rango de los patrones.
    """
    # Calcular rango combinado de todos los patrones
    min_global = min(stats['min'] for stats in self.estadisticas_patrones.values())
    max_global = max(stats['max'] for stats in self.estadisticas_patrones.values())
    
    # Normalizar entrada del rango [0, 1] al rango de patrones
    rango_patrones = max_global - min_global
    matriz_normalizada = matriz_entrada * rango_patrones + min_global
    
    return matriz_normalizada
```

**¿Por qué es necesaria la normalización?**

Los patrones de referencia y la entrada pueden tener rangos de valores diferentes. La normalización asegura que estén en la misma escala para una comparación justa.

**Proceso:**

1. **Calcular rango global de patrones:**
   - `min_global` = Valor mínimo entre TODOS los patrones
   - `max_global` = Valor máximo entre TODOS los patrones

2. **Transformación lineal:**
   ```
   matriz_normalizada = matriz_entrada × (max_global - min_global) + min_global
   ```

**Ejemplo numérico:**

Si los patrones tienen valores en el rango [0.0, 1.0] y la entrada también está en [0, 1]:
- `min_global = 0.0`
- `max_global = 1.0`
- `rango_patrones = 1.0 - 0.0 = 1.0`
- `matriz_normalizada = entrada × 1.0 + 0.0 = entrada` (sin cambios)

---

### 5. Cálculo de Distancia Euclidiana (`_distancia_euclidiana`)

**¡Este es el corazón del algoritmo!**

```python
def _distancia_euclidiana(self, matriz1, matriz2):
    """
    Calcula la distancia euclidiana entre dos matrices.
    """
    diferencia = matriz1 - matriz2
    distancia = np.sqrt(np.sum(diferencia ** 2))
    return distancia
```

**Desglose matemático:**

1. **Resta elemento por elemento:**
   ```python
   diferencia = matriz1 - matriz2
   ```
   Esto crea una nueva matriz donde cada celda contiene la diferencia entre las matrices correspondientes.
   
   **Ejemplo visual (matrices 3×3):**
   ```
   Entrada:     Patrón:      Diferencia:
   [1, 1, 0]    [1, 1, 0]    [0,  0,  0]
   [1, 0, 1] -  [0, 1, 0] =  [1, -1,  1]
   [1, 1, 0]    [1, 1, 0]    [0,  0,  0]
   ```

2. **Elevar al cuadrado:**
   ```python
   diferencia ** 2
   ```
   Eleva cada elemento de la matriz al cuadrado. Esto elimina los signos negativos y enfatiza las diferencias grandes.
   
   ```
   [0,  0,  0]²  =  [0, 0, 0]
   [1, -1,  1]      [1, 1, 1]
   [0,  0,  0]      [0, 0, 0]
   ```

3. **Sumar todos los elementos:**
   ```python
   np.sum(diferencia ** 2)
   ```
   Suma todos los 784 elementos (para matrices 28×28) en un solo número.
   
   ```
   Suma = 0 + 0 + 0 + 1 + 1 + 1 + 0 + 0 + 0 = 3
   ```

4. **Raíz cuadrada:**
   ```python
   np.sqrt(...)
   ```
   Calcula la raíz cuadrada del resultado.
   
   ```
   Distancia = √3 ≈ 1.732
   ```

**Esto implementa exactamente la fórmula:**
```
d = √[Σ (matriz1[i,j] - matriz2[i,j])²]
```

---

### 6. Reconocimiento del Número (`reconocer_numero`)

Este es el método principal que orquesta todo el proceso de reconocimiento.

```python
def reconocer_numero(self, nombre_archivo, mostrar_debug=True):
    """
    Reconoce el número en una matriz de entrada.
    """
    print(f"\n[PROCESANDO] Archivo: {nombre_archivo}")
    print("-" * 70)
    
    # Cargar entrada
    entrada_original = self._cargar_entrada(nombre_archivo)
    
    # Normalizar
    entrada_normalizada = self._normalizar_entrada(entrada_original)
    
    # Calcular distancias
    print("[CALCULANDO] Distancias a todos los patrones...")
    distancias = {}
    for digito in range(10):
        distancias[digito] = self._distancia_euclidiana(
            entrada_normalizada, 
            self.patrones[digito]
        )
    
    # Encontrar número con menor distancia
    numero_detectado = min(distancias, key=distancias.get)
    distancia_minima = distancias[numero_detectado]
    
    # Calcular confianza (inversa de la distancia normalizada)
    distancia_maxima = max(distancias.values())
    distancia_minima_relativa = distancia_minima / distancia_maxima if distancia_maxima > 0 else 0
    confianza = 1 - distancia_minima_relativa
    
    print(f"[✓] Procesamiento completado\n")
    
    # Mostrar debug si se solicita
    if mostrar_debug:
        self._mostrar_debug(entrada_original, entrada_normalizada, 
                           distancias, numero_detectado)
    
    # Preparar resultado
    resultado = {
        'numero': numero_detectado,
        'palabra': self.numeros_palabras[numero_detectado],
        'distancia': distancia_minima,
        'confianza': confianza
    }
    
    return resultado
```

**Proceso detallado:**

#### Paso 1: Cargar la entrada
```python
entrada_original = self._cargar_entrada(nombre_archivo)
```
Lee el archivo Excel de la carpeta `input/` y obtiene la matriz 28×28.

#### Paso 2: Normalizar
```python
entrada_normalizada = self._normalizar_entrada(entrada_original)
```
Ajusta el rango de valores para que coincida con el de los patrones.

#### Paso 3: Calcular distancias a TODOS los patrones
```python
distancias = {}
for digito in range(10):
    distancias[digito] = self._distancia_euclidiana(
        entrada_normalizada, 
        self.patrones[digito]
    )
```

**Ejemplo de resultado:**
```python
distancias = {
    0: 125.43,
    1: 98.76,
    2: 142.89,
    3: 110.25,
    4: 105.67,
    5: 118.92,
    6: 132.45,
    7: 23.14,  # ← Distancia más pequeña!
    8: 127.88,
    9: 115.33
}
```

#### Paso 4: Encontrar el número con menor distancia
```python
numero_detectado = min(distancias, key=distancias.get)
distancia_minima = distancias[numero_detectado]
```

- `min(distancias, key=distancias.get)` → Encuentra la clave (dígito) con el valor (distancia) más pequeño
- En el ejemplo anterior: `numero_detectado = 7` (distancia 23.14)

#### Paso 5: Calcular confianza
```python
distancia_maxima = max(distancias.values())
distancia_minima_relativa = distancia_minima / distancia_maxima
confianza = 1 - distancia_minima_relativa
```

**¿Qué es la confianza?**

Es una medida de qué tan seguro está el sistema de su predicción:
- **Confianza alta (cerca de 1.0 o 100%):** La entrada es muy similar al patrón detectado
- **Confianza baja (cerca de 0.0):** La entrada es ambigua o diferente de todos los patrones

**Ejemplo de cálculo:**
```
distancia_minima = 23.14 (dígito 7)
distancia_maxima = 142.89 (dígito 2)

distancia_minima_relativa = 23.14 / 142.89 ≈ 0.162
confianza = 1 - 0.162 = 0.838 ≈ 83.8%
```

#### Paso 6: Retornar resultado
```python
resultado = {
    'numero': 7,
    'palabra': 'siete',
    'distancia': 23.14,
    'confianza': 0.838
}
```

---

### 7. Mostrar Resultado (`mostrar_resultado`)

```python
def mostrar_resultado(self, resultado):
    """
    Muestra el resultado final en lenguaje natural.
    """
    print("="*70)
    print("RESULTADO FINAL")
    print("="*70)
    print(f"\nEl número ingresado es: {resultado['palabra'].upper()}")
    print(f"\nDetalles:")
    print(f"  • Número detectado: {resultado['numero']}")
    print(f"  • Distancia mínima: {resultado['distancia']:.6f}")
    print(f"  • Confianza: {resultado['confianza']*100:.2f}%")
    print("\n" + "="*70 + "\n")
```

**Salida ejemplo:**
```
======================================================================
RESULTADO FINAL
======================================================================

El número ingresado es: SIETE

Detalles:
  • Número detectado: 7
  • Distancia mínima: 23.140000
  • Confianza: 83.80%

======================================================================
```

---

## Flujo de Ejecución

### Diagrama de Flujo Completo

```
INICIO
  │
  ├─→ [1] Inicializar DetectorNumeros
  │      │
  │      └─→ Cargar 10 patrones (num0.xlsx a num9.xlsx)
  │           └─→ Calcular estadísticas de cada patrón
  │
  ├─→ [2] Cargar archivo de entrada (ej: 7.xlsx)
  │      └─→ Validar dimensiones 28×28
  │
  ├─→ [3] Normalizar entrada al rango de patrones
  │
  ├─→ [4] Calcular distancia euclidiana con CADA patrón
  │      │
  │      ├─→ Distancia con patrón 0
  │      ├─→ Distancia con patrón 1
  │      ├─→ Distancia con patrón 2
  │      ├─→ ...
  │      └─→ Distancia con patrón 9
  │
  ├─→ [5] Encontrar patrón con MENOR distancia
  │      └─→ Ese es el número detectado
  │
  ├─→ [6] Calcular confianza de la predicción
  │
  ├─→ [7] Mostrar resultado en lenguaje natural
  │
FIN
```

### Secuencia de Operaciones con Datos Reales

**Supongamos que queremos reconocer un "7" del archivo `7.xlsx`:**

1. **Carga de entrada:**
   ```
   Matriz 28×28 leída desde input/7.xlsx
   Valores: mayormente 0s con algunos 1s formando la figura del 7
   ```

2. **Normalización:**
   ```
   Ya que entrada y patrones están en [0, 1], 
   la matriz permanece sin cambios
   ```

3. **Cálculo de distancias:**
   ```
   Vs patrón 0: d = 145.23
   Vs patrón 1: d = 98.45
   Vs patrón 2: d = 156.78
   Vs patrón 3: d = 132.90
   Vs patrón 4: d = 118.34
   Vs patrón 5: d = 141.67
   Vs patrón 6: d = 152.11
   Vs patrón 7: d = 18.92  ← MÍNIMA
   Vs patrón 8: d = 135.44
   Vs patrón 9: d = 127.89
   ```

4. **Selección:**
   ```
   Número detectado = 7 (menor distancia: 18.92)
   ```

5. **Confianza:**
   ```
   Confianza = 1 - (18.92 / 156.78) = 1 - 0.121 = 0.879 = 87.9%
   ```

6. **Salida:**
   ```
   "El número ingresado es: SIETE"
   ```

---

## Ejemplos Prácticos

### Ejemplo 1: Reconocimiento Perfecto

**Entrada:** Matriz idéntica al patrón del número 5

**Resultado de distancias:**
```
Dígito 0: 142.56
Dígito 1: 128.34
Dígito 2: 155.78
Dígito 3: 138.92
Dígito 4: 125.67
Dígito 5: 0.00      ← Distancia = 0 (¡coincidencia perfecta!)
Dígito 6: 148.23
Dígito 7: 132.45
Dígito 8: 151.89
Dígito 9: 135.12
```

**Salida:**
```
El número ingresado es: CINCO
Confianza: 100.00%
```

---

### Ejemplo 2: Reconocimiento con Ruido

**Entrada:** Número 3 con algunos píxeles extra (ruido)

**Resultado de distancias:**
```
Dígito 0: 152.34
Dígito 1: 145.67
Dígito 2: 138.92
Dígito 3: 28.45    ← Mínima (pero no cero)
Dígito 4: 142.78
Dígito 5: 147.23
Dígito 6: 155.89
Dígito 7: 149.34
Dígito 8: 136.12
Dígito 9: 141.56
```

**Salida:**
```
El número ingresado es: TRES
Confianza: 81.70%
```

La confianza es menor que 100% debido al ruido, pero aún detecta correctamente.

---

### Ejemplo 3: Entrada Ambigua

**Entrada:** Número que parece tanto 6 como 8

**Resultado de distancias:**
```
Dígito 0: 156.78
Dígito 1: 162.34
Dígito 2: 149.92
Dígito 3: 158.45
Dígito 4: 152.67
Dígito 5: 147.89
Dígito 6: 45.23    ← Mínima
Dígito 7: 165.34
Dígito 8: 48.12    ← Muy cercana!
Dígito 9: 151.56
```

**Salida:**
```
El número ingresado es: SEIS
Confianza: 72.60%
```

La confianza más baja indica ambigüedad: el sistema detecta "6" pero no está muy seguro.

---

## Ventajas y Limitaciones del Método

### ✅ Ventajas

1. **Simplicidad:** Fácil de entender e implementar
2. **Sin entrenamiento:** No requiere algoritmos de machine learning complejos
3. **Interpretable:** Se puede visualizar por qué se tomó una decisión
4. **Rápido:** Cálculo directo sin optimización iterativa

### ⚠️ Limitaciones

1. **Sensible a rotación:** Si el número está rotado, la distancia aumenta mucho
2. **Sensible a escala:** Números más grandes o pequeños afectan el reconocimiento
3. **Requiere alineación:** Los números deben estar centrados en la matriz
4. **No aprende:** No mejora con más datos, siempre usa los mismos patrones fijos

---

## Conceptos Clave para Recordar

### 1. ¿Cómo funciona la distancia euclidiana?
Mide qué tan "diferentes" son dos matrices calculando:
- La diferencia entre cada par de píxeles
- Elevando al cuadrado esas diferencias
- Sumando todo
- Sacando la raíz cuadrada

### 2. ¿Cómo detecta el número?
Compara la entrada contra TODOS los patrones (0-9) y elige el que tenga la **menor distancia** (más parecido).

### 3. ¿Qué es la confianza?
Un porcentaje que indica qué tan seguro está el sistema:
- **Alta confianza:** La entrada es muy similar al patrón detectado
- **Baja confianza:** Puede haber ambigüedad o errores

### 4. ¿Por qué normalizar?
Para que entrada y patrones estén en la misma escala y la comparación sea justa.

---

## Conclusión

El sistema **detecta.py** implementa un clasificador de dígitos manuscritos basado en **reconocimiento por similitud**. En lugar de "aprender" patrones como lo haría una red neuronal, simplemente **compara** la entrada contra ejemplos de referencia usando la **distancia euclidiana** como medida de similitud.

Es un enfoque clásico, simple pero efectivo para problemas donde:
- Tienes buenos patrones de referencia
- Las entradas están bien alineadas y normalizadas
- No hay variaciones extremas (rotación, escala, etc.)

Para casos más complejos, se recomendarían técnicas de machine learning como redes neuronales convolucionales (CNN), pero este método es excelente para comprender los fundamentos del reconocimiento de patrones.

---

**Autores:** Emiliano Rebolledo Navarrete, Azareth Trejo Alvarez, Emilio Abel Zuñiga Cruz   
**Fecha:** Diciembre 2025  
**Curso:** Inteligencia Artificial - 7mo Semestre - Instituto Tecnológico de Celaya
