import sys
import httpx

CLIENT_ID = "36998_qqoFcDBlYfuplZhXy6JsKeW8jsNFpn111uiJgmB4RsXrSrNn8G"
CLIENT_SECRET = "kgrfcb5CyvdbjpD742NuLURnxqJWoDFBvhQxQXhuFt8PL1HNdS"
REDIRECT_URI = "http://localhost"

def exchange_code(auth_code: str):
    # Limpiar el código si el usuario pegó la URL completa
    if "code=" in auth_code:
        auth_code = auth_code.split("code=")[1].split("&")[0]

    url = "https://openapi.ctrader.com/apps/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code.strip()
    }

    try:
        response = httpx.get(url, params=params, timeout=10.0)
        print("Status Code:", response.status_code)
        data = response.json()
        print("Response:", data)
        return data
    except Exception as e:
        print("Error en la solicitud:", e)
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        exchange_code(sys.argv[1])
    else:
        print("Uso: python exchange_ctrader_token.py <CODIGO_O_URL_DE_REDIRECCION>")
