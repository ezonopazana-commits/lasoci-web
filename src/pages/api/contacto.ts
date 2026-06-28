import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { env } from 'cloudflare:workers';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { nombre, apellidos, email, telefono, asunto, mensaje } = await request.json();

    if (!nombre || !apellidos || !email || !asunto || !mensaje) {
      return new Response(JSON.stringify({ ok: false, error: 'Faltan campos obligatorios.' }), { status: 400 });
    }

    const supabase = createClient(
      import.meta.env.PUBLIC_SUPABASE_URL,
      import.meta.env.PUBLIC_SUPABASE_ANON_KEY
    );

    const { error: dbError } = await supabase.from('contactos').insert({
      nombre, apellidos, email, telefono: telefono || null, asunto, mensaje,
    });
    if (dbError) {
      return new Response(JSON.stringify({ ok: false, error: 'Error al guardar el mensaje.' }), { status: 500 });
    }

    try {
      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: 'La Soci <noreply@lasoci.org>',
          to: ['info@lasoci.org'],
          subject: `Contacto web: ${asunto}`,
          html: `<h2>Nuevo mensaje de contacto</h2>
            <p><strong>Nombre:</strong> ${nombre} ${apellidos}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Teléfono:</strong> ${telefono || '—'}</p>
            <p><strong>Asunto:</strong> ${asunto}</p>
            <hr/>
            <p>${String(mensaje).replace(/\n/g, '<br>')}</p>`,
        }),
      });
    } catch (e) {
      console.error('Email error (contacto):', e);
      // El mensaje ya quedó guardado en BD aunque el email falle.
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200 });
  } catch (e: any) {
    console.error('contacto error:', e);
    return new Response(JSON.stringify({ ok: false, error: e.message || 'Error interno' }), { status: 500 });
  }
};
