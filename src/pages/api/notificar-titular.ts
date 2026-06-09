import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const { beneficiario_id } = body;

    const supabase = createClient(
      import.meta.env.PUBLIC_SUPABASE_URL,
      import.meta.env.SUPABASE_SERVICE_ROLE_KEY
    );

    // Obtener datos del beneficiario
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

    // Obtener datos del titular
    const { data: titular } = await supabase
      .from('socios')
      .select('nombre, apellidos, email, iban, telefono')
      .eq('dni', beneficiario.titular_dni)
      .single();

    // Enviar email vía Resend — siempre a ezonopazana@gmail.com
    const resendRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${import.meta.env.RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: 'La Soci <onboarding@resend.dev>',
        to: ['ezonopazana@gmail.com'],
        subject: `Solicitud autorización domiciliación - ${beneficiario.nombre} ${beneficiario.apellidos}`,
        html: `
          <h2>Solicitud de autorización de domiciliación bancaria</h2>
          
          <h3>📋 BENEFICIARIO</h3>
          <ul>
            <li><strong>Nombre:</strong> ${beneficiario.nombre} ${beneficiario.apellidos}</li>
            <li><strong>DNI:</strong> ${beneficiario.dni}</li>
            <li><strong>Email:</strong> ${beneficiario.email}</li>
            <li><strong>IBAN:</strong> ${beneficiario.iban || 'No registrado'}</li>
            <li><strong>Tipo IBAN:</strong> ${beneficiario.iban_tipo || '-'}</li>
          </ul>

          <h3>👤 TITULAR VINCULADO</h3>
          <ul>
            <li><strong>Nombre:</strong> ${titular?.nombre || '-'} ${titular?.apellidos || ''}</li>
            <li><strong>Email:</strong> ${titular?.email || '-'}</li>
            <li><strong>Teléfono:</strong> ${titular?.telefono || '-'}</li>
            <li><strong>IBAN:</strong> ${titular?.iban || '-'}</li>
          </ul>

          <p>Por favor, contacta con el titular para solicitar la autorización de domiciliación bancaria para el beneficiario indicado.</p>
          <p><em>Email generado automáticamente desde el panel de administración de La Soci.</em></p>
        `,
      }),
    });

    const resendData = await resendRes.json();

    if (!resendRes.ok) {
      console.error('Resend error:', JSON.stringify(resendData));
      return new Response(
        JSON.stringify({ ok: false, error: `Error Resend: ${resendData.message || JSON.stringify(resendData)}` }),
        { status: 500 }
      );
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200 });

  } catch (err: any) {
    console.error('notificar-titular error:', err);
    return new Response(JSON.stringify({ ok: false, error: err.message }), { status: 500 });
  }
};
