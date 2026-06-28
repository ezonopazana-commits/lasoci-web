import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { socio_id, dni } = await request.json();
    if (!socio_id || !dni) {
      return new Response(JSON.stringify({ ok: false, error: 'Faltan datos.' }), { status: 400 });
    }

    const supabase = createClient(
      import.meta.env.PUBLIC_SUPABASE_URL,
      import.meta.env.SUPABASE_SERVICE_ROLE_KEY
    );

    const { data: socio, error } = await supabase
      .from('socios')
      .select('dni, direccion, telefono, genero')
      .eq('id', socio_id)
      .single();

    if (error || !socio) {
      return new Response(JSON.stringify({ ok: false, error: 'Socio no encontrado.' }), { status: 404 });
    }

    const dniNormalizado = String(dni).trim().toUpperCase();
    if (!socio.dni || socio.dni.trim().toUpperCase() !== dniNormalizado) {
      return new Response(JSON.stringify({ ok: false, error: 'El DNI no coincide con la ficha seleccionada.' }), { status: 403 });
    }

    return new Response(JSON.stringify({
      ok: true,
      direccion: socio.direccion || null,
      telefono: socio.telefono || null,
      genero: socio.genero || null,
    }), { status: 200 });

  } catch (e: any) {
    console.error('verificar-socio error:', e);
    return new Response(JSON.stringify({ ok: false, error: e.message || 'Error interno' }), { status: 500 });
  }
};
