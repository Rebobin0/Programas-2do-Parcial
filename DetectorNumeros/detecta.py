import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path

class DetectorNumeros:    
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
        
        self._cargar_patrones()
        print("Patrones cargados correctamente (tablas de frecuencias)\n")
    

    def _cargar_patrones(self):
        for digito in range(10):
            ruta = os.path.join(self.ruta_patrones, f"num{digito}.xlsx")
            
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"Patrón no encontrado: {ruta}")
            
            try:
                df = pd.read_excel(ruta, sheet_name=0, header=None)
                matriz = df.values.astype(np.float64)
                
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
                
                print(f"  Patrón {digito}: Cargado: "
                      f"(min={self.estadisticas_patrones[digito]['min']:.2f}, "
                      f"max={self.estadisticas_patrones[digito]['max']:.2f})")
                
            except Exception as e:
                raise Exception(f"Error cargando patrón {digito}: {str(e)}")


    def _cargar_entrada(self, nombre_archivo):
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
            return matriz
            
        except Exception as e:
            raise Exception(f"Error cargando entrada: {str(e)}")
    

    def _normalizar_entrada(self, matriz_entrada):
        # Calcular rango combinado de todos los patrones
        min_global = min(stats['min'] for stats in self.estadisticas_patrones.values())
        max_global = max(stats['max'] for stats in self.estadisticas_patrones.values())
        
        # Normalizar entrada del rango [0, 1] al rango de patrones
        rango_patrones = max_global - min_global
        matriz_normalizada = matriz_entrada * rango_patrones + min_global
        
        return matriz_normalizada
    

    def _distancia_euclidiana(self, matriz1, matriz2):
        diferencia = matriz1 - matriz2
        distancia = np.sqrt(np.sum(diferencia ** 2))
        return distancia
    
    def _mostrar_debug(self, entrada_original, entrada_normalizada, 
                       distancias, numero_detectado):

        print("="*70)
        print("DEBUG: ANÁLISIS DE ENTRADA Y COMPARACIÓN")
        print("="*70)
        
        # Estadísticas de entrada original
        print("\n[ENTRADA ORIGINAL] (valores 0-1)")
        print(f"  Min: {np.min(entrada_original):.4f}")
        print(f"  Max: {np.max(entrada_original):.4f}")
        print(f"  Media: {np.mean(entrada_original):.4f}")
        print(f"  Desv. Est.: {np.std(entrada_original):.4f}")
        
        # Estadísticas de entrada normalizada
        print("\n[ENTRADA NORMALIZADA] (al rango de patrones)")
        print(f"  Min: {np.min(entrada_normalizada):.4f}")
        print(f"  Max: {np.max(entrada_normalizada):.4f}")
        print(f"  Media: {np.mean(entrada_normalizada):.4f}")
        print(f"  Desv. Est.: {np.std(entrada_normalizada):.4f}")
        
        # Estadísticas del patrón ganador
        numero_ganador = numero_detectado
        stats_ganador = self.estadisticas_patrones[numero_ganador]
        print(f"\n[PATRÓN {numero_ganador} - GANADOR] (referencia)")
        print(f"  Min: {stats_ganador['min']:.4f}")
        print(f"  Max: {stats_ganador['max']:.4f}")
        print(f"  Media: {stats_ganador['media']:.4f}")
        print(f"  Desv. Est.: {stats_ganador['std']:.4f}")
        
        # Tabla de distancias
        print("\n[DISTANCIAS A TODOS LOS DÍGITOS]")
        print(f"{'Dígito':<8} {'Distancia':<15} {'Estado':<15}")
        print("-" * 40)
        
        for digito in sorted(distancias.keys()):
            estado = "← GANADOR" if digito == numero_ganador else ""
            print(f"{digito:<8} {distancias[digito]:<15.6f} {estado:<15}")
        
    
    def reconocer_numero(self, nombre_archivo, mostrar_debug=True):        
        # Cargar entrada
        entrada_original = self._cargar_entrada(nombre_archivo)
        
        # Normalizar
        entrada_normalizada = self._normalizar_entrada(entrada_original)
        
        # Calcular distancias)
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
    
    def mostrar_resultado(self, resultado):
        print("="*70)
        print("RESULTADO FINAL")
        print("="*70)
        print(f"\nEl número ingresado es: {resultado['palabra'].upper()}")
        print(f"\nDetalles:")
        print(f"  • Número detectado: {resultado['numero']}")
        print(f"  • Distancia mínima: {resultado['distancia']:.6f}")
        print(f"  • Confianza: {resultado['confianza']*100:.2f}%")


def main():    
    try:
        # Inicializar detector
        detector = DetectorNumeros()
        
        # Archivo de entrada
        nombre_archivo = "7.xlsx"
        
        # Procesar archivo
        resultado = detector.reconocer_numero(
            nombre_archivo, 
            mostrar_debug=True
        )
        # Mostrar resultado
        detector.mostrar_resultado(resultado)
            
    except FileNotFoundError as e:
        print(f"\n[ERROR CRÍTICO] {str(e)}")
        print("Verifica que la carpeta 'patrones' exista con los archivos num0.xlsx a num9.xlsx")
    except ValueError as e:
        print(f"\n[ERROR] {str(e)}")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")


if __name__ == "__main__":
    main()