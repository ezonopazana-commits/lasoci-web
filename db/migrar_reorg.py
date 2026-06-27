def esc(v):
    if v is None: return 'null'
    return "'" + str(v).replace("'", "''") + "'"

# (ccaa_codigo, [(nombre, socios_estimados, rectores_objetivo), ...])
PROPUESTAS = {
 'ANDALUCIA': [('Almería',317//4,2),('Granada',317//4,3),('Málaga',317//4,5),('Jaén',317//4,3),
               ('Huelva',376//4,1),('Cádiz',376//4,2),('Córdoba',376//4,2),('Sevilla Provincia (rural)',376//4,2),
               ('Sevilla Metropolitana (NUEVO)',0,3),('Sevilla Ciudad',152,3)],
 'MADRID': [('Madrid Centro',419//3,4),('Madrid Norte',419//3,4),('Madrid Sur',419//3,4),
            ('Corona Este',334//2,5),('Corona Oeste',334//2,5)],
 'CASTILLA Y LEON': [('Valladolid',313//9*2,2),('León',313//9,1),('Salamanca',313//9,1),('Burgos',313//9,1),
                     ('Palencia',313//9,1),('Zamora',313//9,1),('Ávila',313//9,1),('Segovia',313//9,1),('Soria',313//9,1)],
 'PAIS VASCO': [('Bizkaia',226//2,3),('Gipuzkoa',226//4,2),('Araba/Álava',226//4,1)],
 'MURCIA': [('Murcia Capital',221//5,1),('Cartagena',221//5,1),('Lorca',221//5,1),('Noroeste',221//5,1),('Altiplano',221//5,1)],
 'ISLAS CANARIAS': [('Gran Canaria',78,1),('Lanzarote-Fuerteventura',0,1),('Tenerife Norte',228//2,4),('Tenerife Sur',228//2,2)],
 'LA RIOJA': [('La Rioja Alta',64//2,1),('La Rioja Baja',64//2,1)],
 'ARAGON': [('Alto Aragón (Huesca)',84//2,1),('Bajo Aragón (Zaragoza+Teruel)',84//2,1)],
 'CATALUÑA': [('Barcelona',6458//2,66),('Girona',6458//8,12),('Lleida',6458//16,6),('Tarragona',6458//16,6)],
 # Sin cambios: 1 propuesta = estructura actual
 'ISLAS BALEARES': [('Islas Baleares (sin cambios)',579,11)],
 'COMUNIDAD VALENCIANA': [('Comunidad Valenciana (sin cambios)',645,10)],
 'ASTURIAS': [('Asturias (sin cambios)',48,2)],
 'CANTABRIA': [('Cantabria (sin cambios)',45,1)],
 'CASTILLA-LA MANCHA': [('Castilla-La Mancha (sin cambios)',39,1)],
 'GALICIA': [('Galicia (sin cambios)',36,1)],
 'EXTREMADURA': [('Extremadura (sin cambios)',19,1)],
 'NAVARRA': [('Navarra (sin cambios)',64,2)],
}

NOTAS = [
 ('Hallazgo', 'Cataluña tiene ratio 51,7 socios/rector por fragmentación (53 territorios pequeños)'),
 ('Regla', 'División por provincias reales (sin atomizar más) ya supera el ratio de Cataluña en todos los casos probados'),
 ('Decisión', 'Recorte Cataluña 125→90 es decisión estratégica fija, no fórmula matemática'),
 ('Hallazgo', "22 territorios catalanes con menos de 33 socios (Alta Ribagorça, Priorat, Lluçanès, Terra Alta, Moianès, Ribera Ebre, Pallars Sobirà, Segarra, Vall d'Aran, Solsonès, Cerdanya, Les Garrigues, Pla Urgell, Conca Barberà, Alt Camp, Baix Penedès, BCN Dte.01, Ripollès, Berguedà, Pallars Jussà, Urgell, Montsià) -- 379 socios total"),
]

out = []
out.append("insert into escenarios (nombre, estado) values ('Borrador Reorganización 2026', 'borrador');")
out.append("")
total = 0
for ccaa, props in PROPUESTAS.items():
    for nombre, socios, rect in props:
        total += rect
        out.append(
            f"insert into territorios_propuestos (escenario_id, ccaa_id, nombre, socios_estimados, rectores_objetivo) values "
            f"((select id from escenarios where nombre='Borrador Reorganización 2026'), (select id from ccaa where codigo={esc(ccaa)}), {esc(nombre)}, {socios}, {rect});"
        )
out.append("")
for cat, texto in NOTAS:
    out.append(
        f"insert into notas_estrategia (escenario_id, categoria, texto) values "
        f"((select id from escenarios where nombre='Borrador Reorganización 2026'), {esc(cat)}, {esc(texto)});"
    )

with open('/home/claude/lasoci-web/db/migracion_reorg.sql', 'w') as f:
    f.write("\n".join(out))
print("Total rectores en propuestas:", total)
