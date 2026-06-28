import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { generarDocumentoCandidatura } from '../../lib/docx-candidatura';

const BUCKET = 'postulaciones-rector-docs';

function base64ToUint8Array(base64: string): Uint8Array {
  const clean = base64.includes(',') ? base64.split(',')[1] : base64;
  const binStr = atob(clean);
  const bytes = new Uint8Array(binStr.length);
  for (let i = 0; i < binStr.length; i++) bytes[i] = binStr.charCodeAt(i);
  return bytes;
}

function uint8ToBase64(bytes: Uint8Array): string {
  let binStr = '';
  for (let i = 0; i < bytes.length; i++) binStr += String.fromCharCode(bytes[i]);
  return btoa(binStr);
}

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const {
      socio_id, territorio_id, nombre_completo, dni, direccion,
      motivacion, genero, telefono_contacto,
      tipo_presentacion, // 'fisica' | 'email'
      firma_base64, dni_anverso_base64, dni_reverso_base64,
    } = body;

    if (!socio_id || !territorio_id || !nombre_completo || !dni || !direccion || !motivacion || !genero || !tipo_presentacion) {
      return new Response(JSON.stringify({ ok: false, error: 'Faltan datos obligatorios.' }), { status: 400 });
    }
    if (tipo_presentacion === 'email' && (!firma_base64 || !dni_anverso_base64 || !dni_reverso_base64)) {
      return new Response(JSON.stringify({ ok: false, error: 'Para la vía email se requiere firma y DNI (anverso y reverso).' }), { status: 400 });
    }

    const supabase = createClient(
      import.meta.env.PUBLIC_SUPABASE_URL,
      import.meta.env.SUPABASE_SERVICE_ROLE_KEY
    );

    // 1. Comprobar periodo electoral activo y ventana de candidaturas
    const { data: periodo } = await supabase
      .from('periodo_electoral')
      .select('activo, fecha_inicio_candidaturas, fecha_fin_candidaturas, descripcion')
      .eq('activo', true)
      .maybeSingle();

    if (!periodo) {
      return new Response(JSON.stringify({ ok: false, error: 'No hay un proceso electoral activo en este momento.' }), { status: 400 });
    }
    const hoy = new Date().toISOString().slice(0, 10);
    if (periodo.fecha_inicio_candidaturas && hoy < periodo.fecha_inicio_candidaturas) {
      return new Response(JSON.stringify({ ok: false, error: 'El plazo de presentación de candidaturas todavía no ha comenzado.' }), { status: 400 });
    }
    if (periodo.fecha_fin_candidaturas && hoy > periodo.fecha_fin_candidaturas) {
      return new Response(JSON.stringify({ ok: false, error: 'El plazo de presentación de candidaturas ya ha finalizado.' }), { status: 400 });
    }

    // 2. Territorio + CCAA (para el documento, desde BD, no desde el cliente)
    const { data: territorio, error: errTerr } = await supabase
      .from('territorios')
      .select('nombre, ccaa:ccaa_id(nombre)')
      .eq('id', territorio_id)
      .single();
    if (errTerr || !territorio) {
      return new Response(JSON.stringify({ ok: false, error: 'Territorio no válido.' }), { status: 400 });
    }
    const ccaaNombre = (territorio as any).ccaa?.nombre || '';

    // 2b. Verificación de identidad: el DNI introducido debe coincidir con el real de esa ficha
    const { data: socioReal, error: errSocioReal } = await supabase
      .from('socios').select('dni, genero').eq('id', socio_id).single();
    if (errSocioReal || !socioReal) {
      return new Response(JSON.stringify({ ok: false, error: 'Socio no encontrado.' }), { status: 404 });
    }
    const dniNormalizado = String(dni).trim().toUpperCase();
    if (!socioReal.dni || socioReal.dni.trim().toUpperCase() !== dniNormalizado) {
      return new Response(JSON.stringify({ ok: false, error: 'El DNI no coincide con la ficha seleccionada. Verifica tu identidad.' }), { status: 403 });
    }
    const dniVerificado = socioReal.dni;

    // 3. Si el socio no tenía género guardado, lo fijamos ahora
    if (!socioReal.genero) {
      await supabase.from('socios').update({ genero }).eq('id', socio_id);
    }

    // 4. Generar el documento Word
    const docxBytes = await generarDocumentoCandidatura({
      nombreCompleto: nombre_completo,
      dni: dniVerificado,
      direccion,
      territorioNombre: territorio.nombre,
      ccaaNombre,
      motivacion,
      genero,
      periodoDescripcion: periodo.descripcion || 'Elecciones Rectores',
    });

    const stamp = Date.now();
    const baseName = `${socio_id}-${stamp}`;
    const docxPath = `${baseName}/candidatura.docx`;

    const { error: errUploadDocx } = await supabase.storage.from(BUCKET).upload(
      docxPath,
      docxBytes,
      { contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', upsert: false }
    );
    if (errUploadDocx) {
      return new Response(JSON.stringify({ ok: false, error: 'Error al guardar el documento: ' + errUploadDocx.message }), { status: 500 });
    }

    let firmaPath: string | null = null;
    let dniAnversoPath: string | null = null;
    let dniReversoPath: string | null = null;

    if (tipo_presentacion === 'email') {
      firmaPath = `${baseName}/firma.png`;
      dniAnversoPath = `${baseName}/dni-anverso.jpg`;
      dniReversoPath = `${baseName}/dni-reverso.jpg`;

      await supabase.storage.from(BUCKET).upload(firmaPath, base64ToUint8Array(firma_base64), { contentType: 'image/png', upsert: false });
      await supabase.storage.from(BUCKET).upload(dniAnversoPath, base64ToUint8Array(dni_anverso_base64), { contentType: 'image/jpeg', upsert: false });
      await supabase.storage.from(BUCKET).upload(dniReversoPath, base64ToUint8Array(dni_reverso_base64), { contentType: 'image/jpeg', upsert: false });
    }

    // 5. Insertar registro en postulaciones_rector
    const { data: inserted, error: errInsert } = await supabase
      .from('postulaciones_rector')
      .insert({
        socio_id, territorio_id, motivacion,
        telefono_contacto: telefono_contacto || null,
        estado: 'pendiente',
        tipo_presentacion,
        nombre_completo, dni: dniVerificado, direccion,
        documento_generado_url: docxPath,
        firma_url: firmaPath,
        dni_anverso_url: dniAnversoPath,
        dni_reverso_url: dniReversoPath,
        enviado_at: tipo_presentacion === 'email' ? new Date().toISOString() : null,
      })
      .select('id')
      .single();

    if (errInsert) {
      return new Response(JSON.stringify({ ok: false, error: 'Error al registrar la postulación: ' + errInsert.message }), { status: 500 });
    }

    // 6. Vía email: enviar a info@lasoci.org con adjuntos
    if (tipo_presentacion === 'email') {
      const attachments = [
        { filename: 'candidatura.docx', content: uint8ToBase64(docxBytes) },
        { filename: 'firma.png', content: firma_base64.includes(',') ? firma_base64.split(',')[1] : firma_base64 },
        { filename: 'dni-anverso.jpg', content: dni_anverso_base64.includes(',') ? dni_anverso_base64.split(',')[1] : dni_anverso_base64 },
        { filename: 'dni-reverso.jpg', content: dni_reverso_base64.includes(',') ? dni_reverso_base64.split(',')[1] : dni_reverso_base64 },
      ];

      const resendRes = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${import.meta.env.RESEND_API_KEY}`,
        },
        body: JSON.stringify({
          from: 'La Soci <onboarding@resend.dev>',
          to: ['info@lasoci.org'],
          subject: `Candidatura a Rector/a — ${nombre_completo} (${territorio.nombre})`,
          html: `
            <h2>Nueva candidatura a Rector/a</h2>
            <ul>
              <li><strong>Nombre:</strong> ${nombre_completo}</li>
              <li><strong>DNI:</strong> ${dniVerificado}</li>
              <li><strong>Territorio:</strong> ${territorio.nombre} (${ccaaNombre})</li>
              <li><strong>Teléfono:</strong> ${telefono_contacto || '-'}</li>
            </ul>
            <p>Se adjunta el documento de candidatura firmado y el DNI (anverso y reverso).</p>
          `,
          attachments,
        }),
      });
      const resendData = await resendRes.json();
      if (!resendRes.ok) {
        console.error('Resend error:', JSON.stringify(resendData));
        // No revertimos el registro: ya quedó guardado. Avisamos del fallo de envío.
        return new Response(JSON.stringify({
          ok: true, id: inserted.id, email_enviado: false,
          aviso: 'La candidatura se registró pero el envío del email falló: ' + (resendData?.message || 'error desconocido'),
        }), { status: 200 });
      }
      return new Response(JSON.stringify({ ok: true, id: inserted.id, email_enviado: true }), { status: 200 });
    }

    // 7. Vía física: devolvemos el documento para descarga inmediata
    return new Response(JSON.stringify({
      ok: true, id: inserted.id,
      docx_base64: uint8ToBase64(docxBytes),
      filename: `candidatura-${dniVerificado}.docx`,
    }), { status: 200 });

  } catch (e: any) {
    console.error('postulacion-rector error:', e);
    return new Response(JSON.stringify({ ok: false, error: e.message || 'Error interno' }), { status: 500 });
  }
};
