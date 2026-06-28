import type { APIRoute } from 'astro';
import { env } from 'cloudflare:workers';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { socios, tipo, importe, descripcion } = await request.json();
    if (!Array.isArray(socios) || !tipo || importe === undefined || !descripcion) {
      return new Response(JSON.stringify({ ok: false, error: 'Faltan datos.' }), { status: 400 });
    }

    const destinatarios = socios.filter((s: any) => s?.email);

    const resultados = await Promise.allSettled(destinatarios.map((s: any) =>
      fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: 'la Soci <noreply@lasoci.pages.dev>',
          to: [s.email],
          subject: tipo === 'cargo' ? `la Soci — Cargo por ${descripcion}` : `la Soci — Abono subvención: ${descripcion}`,
          html: `<div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;padding:24px;">
            <div style="background:#1e3a8a;color:white;padding:20px 24px;border-radius:12px 12px 0 0;">
              <span style="font-size:20px;font-weight:bold;color:#fb923c;">la</span>
              <span style="font-size:20px;font-weight:bold;">Soci</span>
            </div>
            <div style="background:white;border:1px solid #e5e7eb;padding:24px;border-radius:0 0 12px 12px;">
              <p style="color:#374151;">Hola <strong>${s.nombre || ''}</strong>,</p>
              <p style="color:#374151;">Te informamos de la siguiente operación en tu cuenta:</p>
              <div style="background:${tipo === 'cargo' ? '#fef2f2' : '#f0fdf4'};border:1px solid ${tipo === 'cargo' ? '#fecaca' : '#bbf7d0'};border-radius:8px;padding:16px;margin:16px 0;text-align:center;">
                <p style="font-size:24px;font-weight:bold;color:${tipo === 'cargo' ? '#dc2626' : '#16a34a'};margin:0;">${tipo === 'cargo' ? '−' : '+'}${Number(importe).toFixed(2)} €</p>
                <p style="color:#6b7280;margin:4px 0 0;">${tipo === 'cargo' ? '💳 Cargo' : '💰 Abono subvención'}</p>
              </div>
              <p style="color:#374151;"><strong>Concepto:</strong> ${descripcion}</p>
              <p style="color:#9ca3af;font-size:12px;margin-top:24px;">Este es un mensaje automático de la Soci. Por favor no respondas a este email.</p>
            </div>
          </div>`,
        }),
      })
    ));

    const enviados = resultados.filter(r => r.status === 'fulfilled').length;
    const fallidos = resultados.length - enviados;

    return new Response(JSON.stringify({ ok: true, enviados, fallidos }), { status: 200 });
  } catch (e: any) {
    console.error('cobros-notificar error:', e);
    return new Response(JSON.stringify({ ok: false, error: e.message || 'Error interno' }), { status: 500 });
  }
};
