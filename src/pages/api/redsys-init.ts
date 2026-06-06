// Endpoint para iniciar pago Redsys
// Pendiente de credenciales (Ds_MerchantCode, Ds_Terminal, clave secreta)
// Documentación: https://pagosonline.redsys.es/

export const prerender = false;

export async function POST({ request }: { request: Request }) {
  const body = await request.json();
  const { eventoId, socioId, importe, concepto } = body;

  // TODO: cuando se disponga de credenciales Redsys
  // 1. Generar Ds_Merchant_Parameters (JSON base64)
  // 2. Firmar con HMAC-SHA256 con clave secreta
  // 3. Redirigir a https://sis.redsys.es/sis/realizarPago

  const REDSYS_CONFIG = {
    merchantCode:  import.meta.env.REDSYS_MERCHANT_CODE || 'PENDIENTE',
    terminal:      import.meta.env.REDSYS_TERMINAL || '001',
    secretKey:     import.meta.env.REDSYS_SECRET_KEY || 'PENDIENTE',
    url:           'https://sis.redsys.es/sis/realizarPago', // producción
    urlTest:       'https://sis-t.redsys.es:25443/sis/realizarPago', // pruebas
  };

  if (REDSYS_CONFIG.merchantCode === 'PENDIENTE') {
    return new Response(JSON.stringify({
      error: 'Redsys no configurado. Añade REDSYS_MERCHANT_CODE, REDSYS_TERMINAL y REDSYS_SECRET_KEY en las variables de entorno.',
      pending: true
    }), { status: 503, headers: { 'Content-Type': 'application/json' } });
  }

  // Implementar cuando se tengan las credenciales
  return new Response(JSON.stringify({ ok: true }), {
    headers: { 'Content-Type': 'application/json' }
  });
}
