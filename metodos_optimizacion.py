import math

def fibonacci_search(f, a, b, n):
    """
    Método de búsqueda de Fibonacci para encontrar el mínimo de una función f(x) en el intervalo [a, b].
    n es el número de evaluaciones de la función.
    """
    # Generar secuencia de Fibonacci
    fib = [1, 1]
    for i in range(2, n + 1):
        fib.append(fib[-1] + fib[-2])
    
    L = b - a
    
    x1 = a + (fib[n-2] / fib[n]) * L
    x2 = a + (fib[n-1] / fib[n]) * L
    
    f1 = f(x1)
    f2 = f(x2)
    
    for k in range(1, n):
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (fib[n-k-1] / fib[n-k]) * (b - a)
            if k < n - 1: # Para evitar evaluar fuera del rango en la última iteración
                f2 = f(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (fib[n-k-2] / fib[n-k]) * (b - a)
            if k < n - 1:
                f1 = f(x1)
                
    return (a + b) / 2

def golden_section_search(f, a, b, tol=1e-5):
    """
    Método de la Sección Dorada para encontrar el mínimo de una función f(x) en el intervalo [a, b].
    """
    phi = (1 + math.sqrt(5)) / 2
    resphi = 2 - phi
    
    # Puntos iniciales
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    
    f1 = f(x1)
    f2 = f(x2)
    
    while abs(b - a) > tol:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = f(x2)
            
    return (a + b) / 2

def quadratic_interpolation(f, x1, x2, x3, tol=1e-5, max_iter=100):
    """
    Método de Interpolación Cuadrática para encontrar el mínimo de una función f(x).
    Requiere tres puntos iniciales x1 < x2 < x3 tales que f(x1) > f(x2) y f(x3) > f(x2).
    """
    for _ in range(max_iter):
        f1, f2, f3 = f(x1), f(x2), f(x3)
        
        # Calcular el punto mínimo del polinomio cuadrático
        num = (x2**2 - x3**2)*f1 + (x3**2 - x1**2)*f2 + (x1**2 - x2**2)*f3
        den = (x2 - x3)*f1 + (x3 - x1)*f2 + (x1 - x2)*f3
        
        if den == 0:
            break
            
        x4 = 0.5 * num / den
        
        if abs(x4 - x2) < tol:
            return x4
            
        # Actualizar los puntos
        if x4 > x2:
            if f(x4) > f2:
                x3 = x4
            else:
                x1, x2 = x2, x4
        else:
            if f(x4) > f2:
                x1 = x4
            else:
                x3, x2 = x2, x4
                
    return x2

def extrapolation_search(f, x0, delta=0.1):
    """
    Método de Extrapolación (Fase de acotamiento) para encontrar un intervalo [a, b] 
    que contiene el mínimo de la función f(x), partiendo de un punto x0.
    """
    k = 0
    
    # Determinar la dirección de búsqueda
    if f(x0 - delta) >= f(x0) >= f(x0 + delta):
        # La función decrece hacia la derecha
        step = delta
    elif f(x0 - delta) <= f(x0) <= f(x0 + delta):
        # La función decrece hacia la izquierda
        step = -delta
    else:
        # El mínimo está ya acotado
        return x0 - delta, x0 + delta
        
    x_k = x0
    x_k_next = x0 + step * (2**k)
    
    while f(x_k_next) < f(x_k):
        k += 1
        x_k_prev = x_k
        x_k = x_k_next
        x_k_next = x_k + step * (2**k)
        
    if step > 0:
        return x_k_prev, x_k_next
    else:
        return x_k_next, x_k_prev

# === Ejemplo de uso ===
if __name__ == "__main__":
    # Función de ejemplo: f(x) = x^2 - 4x + 4 (Mínimo en x = 2)
    def funcion_objetivo(x):
        return x**2 - 4*x + 4
        
    print("=== Minimización de f(x) = x^2 - 4x + 4 (Mínimo real en x = 2) ===")
    
    # 1. Extrapolación para encontrar un intervalo inicial
    print("\n1. Método de Extrapolación:")
    a_ext, b_ext = extrapolation_search(funcion_objetivo, x0=0, delta=0.5)
    print(f"Intervalo acotado encontrado: [{a_ext:.4f}, {b_ext:.4f}]")
    
    # 2. Fibonacci (Usando el intervalo encontrado o uno predefinido)
    print("\n2. Método de Fibonacci:")
    min_fib = fibonacci_search(funcion_objetivo, a=0, b=5, n=20)
    print(f"Mínimo encontrado: {min_fib:.4f}")
    
    # 3. Sección Dorada
    print("\n3. Método de la Sección Dorada:")
    min_dorada = golden_section_search(funcion_objetivo, a=0, b=5, tol=1e-5)
    print(f"Mínimo encontrado: {min_dorada:.4f}")
    
    # 4. Interpolación Cuadrática
    print("\n4. Método de Interpolación Cuadrática:")
    min_interp = quadratic_interpolation(funcion_objetivo, x1=0, x2=1.5, x3=5)
    print(f"Mínimo encontrado: {min_interp:.4f}")
