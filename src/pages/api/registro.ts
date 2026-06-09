import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    
    const supabase = createClient(
      import.meta.env.PUBLIC_SUPABASE_URL,
      import.meta.env.PUBLIC_SUPABASE_ANON_KEY
    );

    const { email, password, nombre, apellidos, dni, telefono, iban, vinculacion, titular_dni, idioma } = body;

    // 1. Crear usuario en auth
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { nombre, apellidos }
      }
    });

    if (authError) {
      return new Response(JSON.stringify({ ok: false, error: authError.message }), { status: 400 });
    }

    const userId = authData.user?.id;
    if (!userId) {
      return new Response(JSON.stringify({ ok: false, error: 'No se pudo crear el usuario' }), { status: 400 });
    }

    // 2. Insertar en tabla socios
    const { error: socioError } = await supabase.from('socios').insert({
      id: userId,
      email,
      nombre,
      apellidos,
      dni,
      telefono: telefono || null,
      iban: iban || null,
      vinculacion,
      titular_dni: titular_dni || null,
      idioma: idioma || 'es',
      activo: false,
      rol: 'asociado'
    });

    if (socioError) {
      return new Response(JSON.stringify({ ok: false, error: socioError.message }), { status: 400 });
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200 });
  } catch (e: any) {
    return new Response(JSON.stringify({ ok: false, error: e.message || 'Error interno' }), { status: 500 });
  }
};
