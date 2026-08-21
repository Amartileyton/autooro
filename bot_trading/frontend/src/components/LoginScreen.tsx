import React, { useEffect, useRef, useState } from 'react';

declare global {
  interface Window {
    google?: any;
  }
}

interface LoginScreenProps {
  apiBaseUrl: string;
  clientId: string;
  onLoginSuccess: (token: string, user: any) => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({
  apiBaseUrl,
  clientId,
  onLoginSuccess
}) => {
  const googleBtnRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [gsiReady, setGsiReady] = useState<boolean>(false);

  useEffect(() => {
    let checkInterval: any = null;

    const initGoogleAuth = () => {
      if (window.google?.accounts?.id && googleBtnRef.current) {
        try {
          window.google.accounts.id.initialize({
            client_id: clientId,
            callback: handleGoogleCredentialResponse,
            auto_select: false,
            cancel_on_tap_outside: true,
          });

          // Renderizar botón oficial personalizado
          window.google.accounts.id.renderButton(googleBtnRef.current, {
            theme: 'filled_black',
            size: 'large',
            shape: 'rectangular',
            text: 'signin_with',
            logo_alignment: 'left',
            width: 320,
          });

          setGsiReady(true);
          if (checkInterval) clearInterval(checkInterval);
        } catch (e) {
          console.error('Error inicializando Google Identity Services:', e);
        }
      }
    };

    // Reintentar si el script de Google tarda unos ms en cargar
    initGoogleAuth();
    if (!window.google?.accounts?.id) {
      checkInterval = setInterval(initGoogleAuth, 300);
    }

    return () => {
      if (checkInterval) clearInterval(checkInterval);
    };
  }, [clientId]);

  const handleGoogleCredentialResponse = async (response: any) => {
    if (!response.credential) {
      setErrorMsg('No se recibió credencial válida de Google.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);

    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/auth/google-login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ credential: response.credential }),
      });

      const data = await res.json();

      if (res.ok && data.status === 'success') {
        localStorage.setItem('goldex_auth_token', data.access_token);
        localStorage.setItem('goldex_auth_user', JSON.stringify(data.user));
        onLoginSuccess(data.access_token, data.user);
      } else {
        const detail = data.detail || 'Error de autenticación.';
        setErrorMsg(detail);
      }
    } catch (err: any) {
      console.error('Error al verificar sesión en backend:', err);
      setErrorMsg('No se pudo conectar con el servidor de autenticación.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0d0e12] overflow-hidden">
      {/* Grid de fondo y resplandor sutil */}
      <div className="absolute inset-0 chart-grid opacity-30 pointer-events-none" />
      <div className="absolute w-[600px] h-[600px] rounded-full bg-amber-500/5 blur-[120px] pointer-events-none" />

      <div className="relative w-full max-w-md p-8 mx-4 rounded-2xl bg-[#14151b]/90 border border-[#2b2d38] shadow-2xl backdrop-blur-xl flex flex-col items-center text-center">
        {/* Cabecera / Logo */}
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-400/20 to-amber-600/5 border border-amber-500/30 flex items-center justify-center mb-5 shadow-lg shadow-amber-500/10">
          <span className="material-symbols-outlined text-amber-400 text-3xl">shield_lock</span>
        </div>

        <div className="flex items-center gap-2 mb-1">
          <span className="text-xl font-bold tracking-tight text-white font-mono">GOLD-EX</span>
          <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono font-semibold">
            CORE-01
          </span>
        </div>

        <p className="text-xs text-[#8e909e] mb-6 font-mono">
          Terminal Autónomo XAUUSD • Acceso Restringido
        </p>

        {/* Badge de seguridad */}
        <div className="w-full bg-[#1b1d26] border border-[#262833] rounded-lg p-3 mb-6 flex items-start gap-3 text-left">
          <span className="material-symbols-outlined text-emerald-400 text-lg shrink-0 mt-0.5">verified_user</span>
          <div>
            <div className="text-[11px] font-bold text-white font-mono uppercase tracking-wider">
              Seguridad Google OAuth 2.0
            </div>
            <div className="text-[11px] text-[#8e909e] mt-0.5 leading-relaxed">
              Solo las cuentas autorizadas en la lista blanca pueden acceder a la telemetría y ejecución.
            </div>
          </div>
        </div>

        {/* Mensaje de Error */}
        {errorMsg && (
          <div className="w-full bg-red-500/10 border border-red-500/30 rounded-lg p-3 mb-5 flex items-start gap-2.5 text-left animate-fadeIn">
            <span className="material-symbols-outlined text-red-400 text-lg shrink-0">error</span>
            <div className="text-xs text-red-300 font-sans leading-relaxed">{errorMsg}</div>
          </div>
        )}

        {/* Botón de Google */}
        <div className="w-full flex flex-col items-center justify-center min-h-[44px]">
          {loading ? (
            <div className="flex items-center gap-3 py-2 text-xs text-amber-400 font-mono">
              <div className="w-4 h-4 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
              Validando credenciales con Google...
            </div>
          ) : (
            <div ref={googleBtnRef} className="flex justify-center w-full" />
          )}

          {!gsiReady && !loading && (
            <div className="text-[11px] text-[#6b6d7a] font-mono mt-2">
              Cargando servicio de autenticación...
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 pt-4 border-t border-[#22242e] w-full flex items-center justify-between text-[10px] text-[#6b6d7a] font-mono">
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            Zero-Trust Gateway
          </span>
          <span>v1.0.0</span>
        </div>
      </div>
    </div>
  );
};
