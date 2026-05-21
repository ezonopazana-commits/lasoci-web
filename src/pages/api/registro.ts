import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  
  const supabase = createClient(
    import.meta.env.PUBLIC_SUPABASE_URL,
    import.meta.env.SUPABASE_SERVICE_ROLE_KEY
  );

  const { id, email, nombre, apellidos, dni, telefono, iban, vinculacion, titular_dni } = body;

  const { error } = await supabase.from('socios').insert({
    id, email, nombre, apellidos, dni,
    telefono: telefono || null,
    iban: iban || null,
    vinculacion,
    titular_dni: titular_dni || null,
    activo: false,
    rol: 'asociado'
  });

  if (error) {
    return new Response(JSON.stringify({ ok: false, error: error.message }), { status: 400 });
  }

  return new Response(JSON.stringify({ ok: true }), { status: 200 });
};
