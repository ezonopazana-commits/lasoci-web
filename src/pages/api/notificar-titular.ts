import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  const { beneficiario_id } = body;

  const supabase = createClient(
    import.meta.env.PUBLIC_SUPABASE_URL,
    import.meta.env.SUPABASE_SERVICE_ROLE_KEY
  );

  const { data: beneficiario, error: errBenef } = await supabase
    .from('socios')
    .select('nombre, apellidos, dni, email, iban, iban_tipo, titular_dni')
    .eq('id', beneficiario_id)
    .single();

  if (errBenef || !beneficiario) {
    return new Response(JSON.stringify({ ok: false, error: 'Beneficiario no encontrado' }), { status: 404 });
  }

  if (!beneficiario.titular_dni) {
    return new Response(JSON.stringify({ ok: false, error: 'Este beneficiario no tiene titular vinculado' }), { status: 400 });
  }

  const { data: titular } = await supabase
    .from('socios')
    .select('nombre, apellidos, email, iban, telefono')
    .eq('dni', beneficiario.titular_dni)
    .single();

  // Obtener email del admin
  const { data: admins } = await supabase
    .from('socios')
    .select('email, nombre, apellidos')
    .eq('rol', 'admin')
    .limit(1);

  const adminEmail = admins?.[0]?.email;
  if (!adminEmail) {
    return new Response(JSON.stringify({ ok: false, error: 'No se encontró email de administrador' }), { status: 400 });
  }

  const resendKey = import.meta.env.RESEND_API_KEY;

  const emailHtml = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: #1e3a5f; padding: 24px; border-radius: 12px 12px 0 0;">
        <h1 style="color: white; margin: 0; font-size: 24px;">
          <span style="color: #f97316;">la</span>Soci — Notificación Admin
        </h1>
      </div>
      <div style="background: #f9fafb; padding: 32px; border-radius: 0 0 12px 12px; border: 1px solid #e5e7eb;">
        <h2 style="color: #1e3a5f; margin-top: 0;">Solicitud de autorización de domiciliación</h2>
        <p style="color: #374151;">El siguiente beneficiario ha solicitado usar el IBAN de su titular para la domiciliación de su cuota.</p>

        <div style="background: white; border: 1px solid #fde68a; border-radius: 8px; padding: 20px; margin: 20px 0;">
          <h3 style="color: #92400e; margin-top: 0; font-size: 15px;">👨‍👩‍👧 Beneficiario</h3>
          <p style="margin: 4px 0; color: #374151;"><strong>Nombre:</strong> ${beneficiario.nombre} ${beneficiario.apellidos}</p>
          <p style="margin: 4px 0; color: #374151;"><strong>DNI:</strong> ${beneficiario.dni}</p>
          <p style="margin: 4px 0; color: #374151;"><strong>Email:</strong> ${beneficiario.email}</p>
          <p style="margin: 4px 0; color: #374151;"><strong>Tipo IBAN solicitado:</strong> ${beneficiario.iban_tipo === 'titular' ? 'IBAN del titular' : 'IBAN propio'}</p>
        </div>

        <div style="background: white; border: 1px solid #bfdbfe; border-radius: 8px; padding: 20px; margin: 20px 0;">
          <h3 style="color: #1e40af; margin-top: 0; font-size: 15px;">👔 Titular vinculado</h3>
          <p style="margin: 4px 0; color: #374151;"><strong>Nombre:</strong> ${titular?.nombre || '—'} ${titular?.apellidos || ''}</p>
          <p style="margin: 4px 0; color: #374151;"><strong>Email:</strong> ${titular?.email || 'Sin email registrado'}</p>
          <p style="margin: 4px 0; color: #374151;"><strong>Teléfono:</strong> ${titular?.telefono || 'Sin teléfono registrado'}</p>
          <p style="margin: 4px 0; color: #374151;"><strong>IBAN:</strong> ${titular?.iban ? titular.iban.match(/.{1,4}/g)?.join(' ') : 'Sin IBAN registrado'}</p>
        </div>

        <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 16px; margin: 20px 0;">
          <p style="color: #9a3412; margin: 0; font-size: 14px;">
            <strong>⚠️ Acción requerida:</strong> Contacta con el titular para verificar que autoriza el uso de su cuenta para la domiciliación del beneficiario. Una vez confirmado, aprueba al beneficiario desde el panel de administración.
          </p>
        </div>

        <p style="color: #6b7280; font-size: 13px;">Este email ha sido generado automáticamente desde el panel de administración de la Soci.</p>
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;" />
        <p style="color: #9ca3af; font-size: 12px; margin: 0;">Associació del Personal de CaixaBank — la Soci</p>
      </div>
    </div>
  `;

  const resendRes = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${resendKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: 'la Soci <onboarding@resend.dev>',
      to: ['ezonopazana@gmail.com'],
      subject: `⚠️ Solicitud autorización IBAN — ${beneficiario.nombre} ${beneficiario.apellidos}`,
      html: emailHtml
    })
  });

  if (!resendRes.ok) {
    const err = await resendRes.json();
    return new Response(JSON.stringify({ ok: false, error: err.message || 'Error al enviar email' }), { status: 500 });
  }

  return new Response(JSON.stringify({ 
    ok: true, 
    admin_email: adminEmail,
    titular_nombre: titular ? titular.nombre + ' ' + titular.apellidos : 'No encontrado'
  }), { status: 200 });
};
