"""
Autoprueba de login: prueba iniciar sesion con TODOS los usuarios
haciendo peticiones HTTP reales al servidor FastAPI.
"""
import urllib.request
import urllib.error
import json
import sys

API_BASE = "http://127.0.0.1:8000"

# Lista de usuarios a probar (nombre/correo/documento, contrasena)
TEST_USERS = [
    ("nelson",          "1234"),
    ("maria",           "1234"),
    ("Juan Perez",      "1234"),
    ("Maria Lopez",     "1234"),
    ("Carlos Ruiz",     "1234"),
    ("wilson",          "1234"),
    ("Alberto Sarmiento","1234"),
    ("mathew",          "1234"),
    ("aaa",             "1234"),   # antes fallaba
    ("Marcos",          "1234"),   # antes fallaba
]


def post_json(url, payload):
    body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read()).get('detail', str(e))
        except Exception:
            detail = str(e)
        return e.code, {"detail": detail}
    except Exception as ex:
        return None, {"detail": str(ex)}


def main():
    print("=" * 70)
    print("  AUTOPRUEBA DE LOGIN - TODOS LOS USUARIOS")
    print("=" * 70)

    # Verificar que el servidor esta corriendo
    try:
        with urllib.request.urlopen(f"{API_BASE}/docs", timeout=5) as r:
            pass
        print(f"\n  Servidor FastAPI: ACTIVO en {API_BASE}\n")
    except Exception as e:
        print(f"\n  [ERROR] El servidor no esta corriendo en {API_BASE}")
        print(f"  Inicia el servidor con: python -m uvicorn app.main:app --reload")
        print(f"  Error: {e}")
        sys.exit(1)

    ok_count = 0
    fail_count = 0
    results = []

    for username, password in TEST_USERS:
        status, resp = post_json(f"{API_BASE}/auth/login", {
            "username": username,
            "password": password
        })

        if status == 200 and "access_token" in resp:
            rol = resp.get("user", {}).get("rol", "?")
            nombre = resp.get("user", {}).get("nombre", username)
            print(f"  [ OK ] {nombre:<22} | rol: {rol:<12} | token: {resp['access_token'][:20]}...")
            ok_count += 1
            results.append((username, "OK", rol))
        else:
            detail = resp.get("detail", "Error desconocido") if isinstance(resp, dict) else str(resp)
            print(f"  [FAIL] {username:<22} | HTTP {status} | {detail}")
            fail_count += 1
            results.append((username, f"FAIL({status})", detail))

    print(f"\n{'='*70}")
    print(f"  RESULTADO: {ok_count} OK / {fail_count} FALLIDOS de {len(TEST_USERS)} usuarios")
    print(f"{'='*70}")

    if fail_count == 0:
        print("\n  Todos los usuarios pueden iniciar sesion correctamente!")
    else:
        print("\n  Algunos usuarios fallaron. Revisa los errores arriba.")

    return fail_count


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
