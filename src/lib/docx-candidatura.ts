import {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel,
  BorderStyle,
} from 'docx';

export interface DatosCandidatura {
  nombreCompleto: string;
  dni: string;
  direccion: string;
  territorioNombre: string;
  ccaaNombre: string;
  motivacion: string;
  genero: 'M' | 'F';
  periodoDescripcion: string;
}

function terminos(genero: 'M' | 'F') {
  const f = genero === 'F';
  return {
    tratamiento: f ? 'Dña.' : 'D.',
    socio: f ? 'socia' : 'socio',
    candidato: f ? 'candidata' : 'candidato',
    cargo: f ? 'Rectora' : 'Rector',
  };
}

const FUENTE = 'Arial';

export async function generarDocumentoCandidatura(datos: DatosCandidatura): Promise<Uint8Array> {
  const t = terminos(datos.genero);
  const fecha = new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });

  const parrafosMotivacion = datos.motivacion
    .split('\n')
    .map(l => l.trim())
    .filter(Boolean)
    .map(linea => new Paragraph({
      children: [new TextRun({ text: linea, font: FUENTE, size: 22 })],
      spacing: { after: 160 },
      alignment: AlignmentType.JUSTIFIED,
    }));

  const doc = new Document({
    styles: {
      default: { document: { run: { font: FUENTE, size: 22 } } },
    },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: 'la', bold: true, color: 'F97316', size: 32, font: FUENTE })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: 'Soci', bold: true, size: 32, font: FUENTE })],
          spacing: { after: 300 },
        }),
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `SOLICITUD DE CANDIDATURA A ${t.cargo.toUpperCase()}`, bold: true, size: 28, font: FUENTE })],
          spacing: { after: 80 },
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: datos.periodoDescripcion, italics: true, size: 20, color: '666666', font: FUENTE })],
          spacing: { after: 400 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'F97316', space: 8 } },
        }),

        new Paragraph({
          alignment: AlignmentType.JUSTIFIED,
          spacing: { after: 240 },
          children: [
            new TextRun({ text: `${t.tratamiento} ${datos.nombreCompleto}, con DNI nº ${datos.dni}, con domicilio en ${datos.direccion}, ${t.socio} de la Associaci\u00F3 del Personal de La Caixa (LA SOCI),`, font: FUENTE, size: 22 }),
          ],
        }),

        new Paragraph({
          children: [new TextRun({ text: 'EXPONE:', bold: true, font: FUENTE, size: 22 })],
          spacing: { after: 120 },
        }),
        new Paragraph({
          alignment: AlignmentType.JUSTIFIED,
          spacing: { after: 320 },
          children: [
            new TextRun({
              text: `Que, de acuerdo con lo establecido en los Estatutos de la Asociaci\u00F3n y la convocatoria del proceso electoral vigente, desea presentar su candidatura al cargo de ${t.cargo} en representaci\u00F3n del territorio de ${datos.territorioNombre} (${datos.ccaaNombre}).`,
              font: FUENTE, size: 22,
            }),
          ],
        }),

        new Paragraph({
          children: [new TextRun({ text: 'MOTIVACI\u00D3N DE LA CANDIDATURA', bold: true, font: FUENTE, size: 22 })],
          spacing: { after: 160 },
        }),
        ...parrafosMotivacion,

        new Paragraph({
          children: [new TextRun({ text: 'SOLICITA:', bold: true, font: FUENTE, size: 22 })],
          spacing: { before: 200, after: 120 },
        }),
        new Paragraph({
          alignment: AlignmentType.JUSTIFIED,
          spacing: { after: 500 },
          children: [
            new TextRun({
              text: `La admisi\u00F3n de la presente candidatura para su consideraci\u00F3n por la Comisi\u00F3n Electoral de LA SOCI en el proceso electoral en curso.`,
              font: FUENTE, size: 22,
            }),
          ],
        }),

        new Paragraph({
          alignment: AlignmentType.RIGHT,
          spacing: { after: 600 },
          children: [new TextRun({ text: `En Espa\u00F1a, a ${fecha}`, font: FUENTE, size: 22 })],
        }),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 800, after: 80 },
          children: [new TextRun({ text: 'Firma:', font: FUENTE, size: 22 })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 80 },
          children: [new TextRun({ text: '_______________________________', font: FUENTE, size: 22 })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `${t.tratamiento} ${datos.nombreCompleto}`, font: FUENTE, size: 20 })],
        }),
      ],
    }],
  });

  const buffer = await Packer.toBuffer(doc);
  return new Uint8Array(buffer);
}
