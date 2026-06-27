import re

def esc(v):
    if v is None: return 'null'
    return "'" + str(v).replace("'", "''") + "'"

def slug(s):
    s = (s or '').lower()
    for a,b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),(' ','.'),(',','')]:
        s = s.replace(a,b)
    return re.sub(r'[^a-z0-9.]', '', s) or 'x'

# (apellidos, nombre, territorio, estado, tipo_asociado, seccion, interes, presentada)
NUEVOS = [
('AMUTIO PERAITA','M. ANGELES','LOGROÑO','ACTIVO','DELEGADO','PADEL LOGROÑO',True,True),
('Numero 1','','LA SELVA','ACTIVO','SOCIO',None,True,True),
('Numero 4','','LLUÇANÈS','ACTIVO','SOCIO',None,True,True),
('GUERRA COLSA','INMACULADA','MADRID','ACTIVO','DELEGADO','PADEL MADRID',True,True),
('TORO ALBA','FRANCISCO JAVIER','MADRID (EXC. MADRID CIUDAD)','ACTIVO','DELEGADO','ACTIVIDADES SUBACUATICAS MADRID',True,True),
('GESTOSO CARIDE','GONZALO','MADRID','ACTIVO','SOCIO',None,True,True),
('LOPEZ DEL AMO','ESPERANZA','MADRID','ACTIVO','DELEGADO','ESQUI MADRID',True,True),
('PALOMARES ALONSO','PABLO','MADRID','ACTIVO','SOCIO',None,True,True),
('DE GREGORIO MUÑOZ','FRANCISCO JAVIER','MADRID','ACTIVO','SOCIO',None,True,True),
('SAINZ DE LA MAZA','JUAN CARLOS','MADRID (EXC. MADRID CIUDAD)','ACTIVO','SOCIO',None,True,True),
('Numero 6','','MOIANÈS','ACTIVO','SOCIO',None,True,True),
('LOPEZ-CORTIJO LOPEZ','JUAN','MURCIA','ACTIVO','SOCIO',None,True,True),
('FAJIN OCERIN','ANTONIO ROQUE','MURCIA','ACTIVO','DELEGADO','KARTING MURCIA',True,True),
('CASADO FUENTES','EDUARDO','NAVARRA','ACTIVO','DELEGADO','MULTIAVENTURA NAVARRA',True,True),
('','KOTTE','NAVARRA','ACTIVO','SOCIO',None,True,False),
('Numero 2','','OSONA','ACTIVO','SOCIO',None,True,True),
('HURTADO DE MENDOZA VELASCO','JOSE','PAIS VASCO','ACTIVO','DELEGADO','GASTRONOMIA BILBAO',True,True),
('ULLOA SALDAÑA','OSCAR','PAIS VASCO','ACTIVO','DELEGADO','GOLF BIZKAIA',True,True),
('HERNANDEZ JIMENEZ','PABLO','SANTA CRUZ DE TENERIFE','ACTIVO','DELEGADO','VELA Y MOTONAUTICA TENERIFE',True,True),
('Numero 5','','TERRA ALTA','ACTIVO','SOCIO',None,True,True),
('CASAS POY','JAIME','VALENCIA (CIUTAT)','ACTIVO','DELEGADO','MUSICA MODERNA VALENCIA',True,True),
('PENDIENTE DE JAIME','','VALENCIA (CIUTAT)','ACTIVO','SOCIO',None,True,True),
('IGLESIAS BALAGUER','JUAN JOSE','ANDALUCIA (HUE,COR,CAD,SEV)','ACTIVO','DELEGADO','GASTRONOMIA SEVILLA',True,True),
('ARCE MURILLO','PABLO','CASTILLA Y LEON','ACTIVO','DELEGADO','F.S. LEON',True,True),
('RODRIGUEZ CHAMORRO','LUIS MIGUEL','CASTILLA-LA MANCHA','ACTIVO','DELEGADO','BICI T.T. CIUDAD REAL',True,True),
('LARGO FERNANDEZ','FERNANDO','CASTILLA Y LEON','ACTIVO','DELEGADO','MOTOTURISMO CASTILLA Y LEON',True,True),
('NAVARRO ALVAREZ DE QUEVEDO','CRISTINA','MADRID (EXC. MADRID CIUDAD)','ACTIVO','SOCIO',None,True,True),
('COLORADO MORENO','ALFONSO','MADRID (EXC. MADRID CIUDAD)','ACTIVO','SOCIO',None,True,True),
('DE LA RED SANCHEZ','JUAN CARLOS','MADRID (EXC. MADRID CIUDAD)','ACTIVO','SOCIO',None,True,True),
('JURADO NEVA','MARIA JOSE','ANDALUCIA (HUE,COR,CAD,SEV)','ACTIVO','DELEGADO','MULTIAVENTURA CADIZ',True,True),
# Nota: existe tambien un ID 444820 duplicado de Jurado Neva en estado INACTIVO (version antigua/superada) - se omite a proposito.
]

socio_lines = []
cand_lines = []
for ape, nom, terr, estado, tipo, seccion, interes, presentada in NUEVOS:
    email = f"{slug(nom)}.{slug(ape)}.pendiente@pendiente.lasoci.org"
    socio_lines.append(f"  ({esc(ape)}, {esc(nom)}, {esc(email)}, null, 'es', 'socio', true)")
    cand_lines.append(
        f"  ((select id from socios where email={esc(email)}), "
        f"(select id from territorios where nombre={esc(terr)}), "
        f"{esc(estado)}, {esc(tipo)}, {esc(seccion)}, {str(interes).lower()}, {str(presentada).lower()})"
    )

out = "-- Personas reales que faltaban (la lectura anterior via Drive se truncaba)\n"
out += "insert into socios (apellidos, nombre, email, telefono, idioma, rol, activo) values\n"
out += ",\n".join(socio_lines) + "\non conflict (email) do nothing;\n\n"
out += "insert into candidaturas (socio_id, territorio_id, estado, tipo_asociado, seccion, interes_rector, candidatura_presentada) values\n"
out += ",\n".join(cand_lines) + ";\n"

with open('/home/claude/lasoci-web/db/migracion_datos_2.sql', 'w') as f:
    f.write(out)
print("Generado:", len(NUEVOS), "personas nuevas")
