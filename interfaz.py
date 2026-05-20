import math
import os

try:
    import numexpr as ne
    HAS_NUMEXPR = True
except ImportError:
    HAS_NUMEXPR = False


def make_func(expr):
    """Compila una expresión matemática a una función f(x)."""
    expr_clean = expr.replace("^", "**")

    if HAS_NUMEXPR:
        def f(x):
            try:
                return float(
                    ne.evaluate(
                        expr_clean,
                        local_dict={
                            "x": x, "e": math.e, "pi": math.pi,
                            "sin": math.sin, "cos": math.cos, "tan": math.tan,
                            "log": math.log, "ln": math.log, "exp": math.exp,
                            "sqrt": math.sqrt, "abs": abs,
                        },
                    )
                )
            except Exception as exc:
                raise ValueError(f"Error evaluando '{expr_clean}' en x={x}: {exc}")
        return f
    else:
        allowed_globals = {
            "__builtins__": {},
            "math": math,
            "abs": abs,
            "e": math.e,
            "pi": math.pi,
        }
        def f(x):
            try:
                return float(eval(expr_clean, allowed_globals, {"x": x}))
            except Exception as exc:
                raise ValueError(f"Error evaluando '{expr_clean}' en x={x}: {exc}")
        return f


def test_func(f, x0):
    """Verifica que f(x0) retorne un número válido."""
    v = f(x0)
    if v is None or math.isnan(v) or math.isinf(v):
        raise ValueError("La función no devuelve un valor numérico válido en x=1.")
    return v


# ─────────────────────────── MÉTODOS ─────────────────────────────

def fib_search(f, a, b, n):
    """Búsqueda de Fibonacci."""
    fib = [1, 1]
    for i in range(2, n + 1):
        fib.append(fib[-1] + fib[-2])
    L = b - a
    x1 = a + (fib[n - 2] / fib[n]) * L
    x2 = a + (fib[n - 1] / fib[n]) * L
    f1, f2 = f(x1), f(x2)
    for k in range(1, n):
        if f1 > f2:
            a = x1; x1 = x2; f1 = f2
            x2 = a + (fib[n - k - 1] / fib[n - k]) * (b - a)
            if k < n - 1:
                f2 = f(x2)
        else:
            b = x2; x2 = x1; f2 = f1
            x1 = a + (fib[n - k - 2] / fib[n - k]) * (b - a)
            if k < n - 1:
                f1 = f(x1)
    return (a + b) / 2


def golden_search(f, a, b, tol=1e-5):
    """Sección Dorada."""
    phi       = (1 + math.sqrt(5)) / 2
    resphi    = 2 - phi
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1, f2 = f(x1), f(x2)
    while abs(b - a) > tol:
        if f1 < f2:
            b = x2; x2 = x1; f2 = f1
            x1 = a + resphi * (b - a); f1 = f(x1)
        else:
            a = x1; x1 = x2; f1 = f2
            x2 = b - resphi * (b - a); f2 = f(x2)
    return (a + b) / 2


def quadratic_interp(f, x1, x2, x3, tol=1e-5, max_iter=100):
    """Interpolación Cuadrática."""
    for _ in range(max_iter):
        f1, f2, f3 = f(x1), f(x2), f(x3)
        num = (x2**2 - x3**2) * f1 + (x3**2 - x1**2) * f2 + (x1**2 - x2**2) * f3
        den = (x2 - x3) * f1 + (x3 - x1) * f2 + (x1 - x2) * f3
        if abs(den) < 1e-14:
            break
        x4 = 0.5 * num / den
        if abs(x4 - x2) < tol:
            return x4
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
    """Búsqueda por Extrapolación (fase de acotamiento)."""
    if f(x0 - delta) >= f(x0) >= f(x0 + delta):
        step = delta
    elif f(x0 - delta) <= f(x0) <= f(x0 + delta):
        step = -delta
    else:
        return x0 - delta, x0 + delta

    x_k      = x0
    x_k_next = x0 + step
    k        = 0

    while f(x_k_next) < f(x_k):
        k       += 1
        x_k_prev  = x_k
        x_k       = x_k_next
        x_k_next  = x_k + step * (2 ** k)

    if step > 0:
        return x_k_prev, x_k_next
    else:
        return x_k_next, x_k_prev


# ─────────────────────────── INTERFAZ ─────────────────────────────

RESET = "\033[0m"
BOLD  = "\033[1m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
RED   = "\033[91m"
GRAY  = "\033[90m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(f"""
{CYAN}{BOLD}
 ╔══════════════════════════════════════════╗
 ║     MÉTODOS DE OPTIMIZACIÓN UNIDIMENSIONAL  ║
 ║          (Búsqueda sin Derivadas)             ║
 ╚══════════════════════════════════════════╝
{RESET}""")


def read_float(msg):
    while True:
        try:
            return float(input(f"  {YELLOW}→{RESET} {msg}").strip())
        except ValueError:
            print(f"  {RED}✗ Valor numérico inválido. Intenta de nuevo.{RESET}")


def read_int(msg, min_val=1):
    while True:
        try:
            val = int(input(f"  {YELLOW}→{RESET} {msg}").strip())
            if val < min_val:
                print(f"  {RED}✗ Debe ser ≥ {min_val}.{RESET}")
                continue
            return val
        except ValueError:
            print(f"  {RED}✗ Entero inválido. Intenta de nuevo.{RESET}")


def read_equation():
    """Lee y compila la función objetivo."""
    print(f"\n{GREEN}{BOLD}━━ INGRESO DE FUNCIÓN ━━{RESET}")
    print(f"  Expresión en variable {GREEN}x{RESET}.")
    print(f"  Funciones: sin, cos, tan, log, ln, exp, sqrt, abs")
    print(f"  Constantes: pi, e")
    print(f"  Ejemplos:  x**2 - 4*x + 4     x**3 + 3*x**2     exp(-x**2)")

    while True:
        expr = input(f"\n  {YELLOW}f(x) = {RESET}").strip()
        if not expr:
            print(f"  {RED}✗ La expresión no puede estar vacía.{RESET}")
            continue
        try:
            f = make_func(expr)
            test_func(f, 1.0)
            print(f"  {GREEN}✓ Función validada correctamente{RESET}")
            return f, expr
        except Exception as exc:
            print(f"  {RED}✗ {exc}{RESET}")


def menu_method():
    print(f"""
{GREEN}{BOLD}━━ SELECCIONA UN MÉTODO ━━{RESET}
  {CYAN}1.{RESET}  Búsqueda de Fibonacci
  {CYAN}2.{RESET}  Sección Dorada
  {CYAN}3.{RESET}  Interpolación Cuadrática
  {CYAN}4.{RESET}  Búsqueda por Extrapolación
""")
    while True:
        choice = input(f"  {YELLOW}→ Opción [1-4]: {RESET}").strip()
        if choice in ("1", "2", "3", "4"):
            return int(choice)
        print(f"  {RED}✗ Opción inválida.{RESET}")


def collect_params(method, _f_unused):
    if method == 4:
        delta = read_float("Valor de delta, paso inicial, ej: 0.1: ")
        return {"delta": delta}
    return {}


def run_method(method, f, a, b, params):
    names = {
        1: "Búsqueda de Fibonacci",
        2: "Sección Dorada",
        3: "Interpolación Cuadrática",
        4: "Búsqueda por Extrapolación",
    }
    name = names[method]
    print(f"\n  {CYAN}⏳ Ejecutando {name}...{RESET}")

    try:
        if method == 1:
            n = read_int("Número de evaluaciones n  (recomendado 10–30): ", min_val=2)
            result = fib_search(f, a, b, n)

        elif method == 2:
            tol = read_float("Tolerancia, ej: 1e-5: ")
            result = golden_search(f, a, b, tol=tol)

        elif method == 3:
            print(f"\n  {GRAY}Se requieren tres puntos x1 < x2 < x3 en [{a}, {b}].{RESET}")
            print(f"  {GRAY}x1 toma el valor a={a} y x2 el punto medio por defecto.{RESET}")
            while True:
                x3_raw = input(f"  {YELLOW}→{RESET} Tercer punto x3 (en [{a}, {b}]): ").strip()
                x3     = float(x3_raw)
                mid    = (a + b) / 2.0
                if x3 <= mid:
                    print(f"  {RED}✗ x3 ({x3}) debe ser mayor que el punto medio ({mid:.4f}).{RESET}")
                    continue
                if x3 >= b:
                    print(f"  {RED}✗ x3 ({x3}) debe ser menor que b ({b}).{RESET}")
                    continue
                break
            result = quadratic_interp(f, a, (a + b) / 2, x3)

        elif method == 4:
            x0 = a
            result = extrapolation_search(f, x0, delta=params.get("delta", 0.1))
            if isinstance(result, tuple):
                print(f"  {GREEN}✓ Intervalo acotado: [{result[0]:.6f}, {result[1]:.6f}]{RESET}")
                print(f"  {GREEN}  (El mínimo se encuentra dentro de este intervalo){RESET}")
                return result

        if not isinstance(result, tuple):
            f_val = f(result)
            print(f"\n  {GREEN}{BOLD}✓ Resultado:{RESET}")
            print(f"    x*    = {result:.6f}")
            print(f"    f(x*)  = {f_val:.6f}")
        return result

    except Exception as exc:
        print(f"  {RED}✗ Error: {exc}{RESET}")
        return None


def continue_prompt():
    print(f"\n{GRAY}{'─'*46}{RESET}")
    while True:
        ans = input(f"  {YELLOW}¿Ejecutar otro método con la misma función? [s/n]: {RESET}").strip().lower()
        if ans in ("s", "n"):
            return ans == "s"
        print(f"  {RED}✗ Responde 's' o 'n'.{RESET}")


def main():
    while True:
        clear()
        banner()

        # ── 1. Ecuación ──────────────────────────────────────────
        f, expr = read_equation()

        # ── 2. Intervalo ─────────────────────────────────────────
        print(f"\n{GREEN}{BOLD}━━ INTERVALO DE BÚSQUEDA ━━{RESET}")
        a = read_float("Extremo izquierdo  a: ")
        b = read_float("Extremo derecho   b: ")
        while b <= a:
            print(f"  {RED}✗ b debe ser mayor que a.{RESET}")
            b = read_float("Extremo derecho   b: ")

        # ── 3. Selección de método ───────────────────────────────
        while True:
            clear()
            banner()
            print(f"  {BOLD}f(x) = {expr}{RESET}")
            print(f"  Intervalo:  [{a}, {b}]")
            print(f"\n{GRAY}{'─'*46}{RESET}")

            method   = menu_method()
            params   = collect_params(method, f)

            clear()
            banner()
            print(f"  {BOLD}f(x) = {expr}{RESET}")
            print(f"  Intervalo:  [{a}, {b}]")
            run_method(method, f, a, b, params)

            if not continue_prompt():
                break

        print(f"\n  {GREEN}{BOLD}¡Hasta luego!{RESET}\n")
        ans_final = input(f"  {YELLOW}¿Analizar otra función? [s/n]: {RESET}").strip().lower()
        if ans_final != "s":
            break
    clear()
    print(f"\n{GREEN}{BOLD}Programa finalizado. ¡Hasta luego!{RESET}\n")


if __name__ == "__main__":
    main()
