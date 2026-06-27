import json, re

# ---------- CCAA (17) con es_afin ----------
CCAA = {
 'ANDALUCIA': True, 'ARAGON': True, 'ASTURIAS': True, 'CANTABRIA': True,
 'CASTILLA Y LEON': True, 'CASTILLA-LA MANCHA': True, 'CATALUÑA': False,
 'COMUNIDAD VALENCIANA': False, 'EXTREMADURA': True, 'GALICIA': True,
 'ISLAS BALEARES': False, 'ISLAS CANARIAS': True, 'LA RIOJA': True,
 'MADRID': True, 'MURCIA': True, 'NAVARRA': True, 'PAIS VASCO': True,
}

# ---------- Territorios reales (nombre tal cual en candidaturas.TERRITORIO, cuota_total, ccaa) ----------
TERRITORIOS = [
 ('ALT CAMP',1,'CATALUÑA'),('ALT EMPORDA',2,'CATALUÑA'),('ALT PENEDES',2,'CATALUÑA'),
 ('ALT URGELL',1,'CATALUÑA'),('ALTA RIBAGORÇA',1,'CATALUÑA'),
 ('ANDALUCIA (ALM,GRA,JAE,MAL)',5,'ANDALUCIA'),('ANDALUCIA (HUE,COR,CAD,SEV)',5,'ANDALUCIA'),
 ('ANDALUCIA (SEVILLA CIUDAD)',3,'ANDALUCIA'),
 ('ANOIA',2,'CATALUÑA'),('ARAGÓN',2,'ARAGON'),('ASTURIAS',2,'ASTURIAS'),
 ('BAGES',2,'CATALUÑA'),('BAIX CAMP',2,'CATALUÑA'),('BAIX EBRE',2,'CATALUÑA'),
 ('BAIX EMPORDA',3,'CATALUÑA'),('BAIX LLOBREGAT',7,'CATALUÑA'),('BAIX PENEDES',1,'CATALUÑA'),
 ('BARCELONA DTE. 01',1,'CATALUÑA'),('BARCELONA DTE. 02',8,'CATALUÑA'),
 ('BARCELONA DTE. 03',3,'CATALUÑA'),('BARCELONA DTE. 04',5,'CATALUÑA'),
 ('BARCELONA DTE. 05',5,'CATALUÑA'),('BARCELONA DTE. 06',4,'CATALUÑA'),
 ('BARCELONA DTE. 07',3,'CATALUÑA'),('BARCELONA DTE. 08',2,'CATALUÑA'),
 ('BARCELONA DTE. 09',3,'CATALUÑA'),('BARCELONA DTE. 10',4,'CATALUÑA'),
 ('BARCELONÈS',3,'CATALUÑA'),('BERGUEDÀ',1,'CATALUÑA'),
 ('CANTABRIA',1,'CANTABRIA'),('CASTILLA-LA MANCHA',1,'CASTILLA-LA MANCHA'),
 ('CASTILLA Y LEON',5,'CASTILLA Y LEON'),('CERDANYA',1,'CATALUÑA'),
 ('COM. VALENCIANA (EXC.VALENCIA CIUTAT)',6,'COMUNIDAD VALENCIANA'),
 ('CONCA DE BARBERÀ',1,'CATALUÑA'),('EIVISSA I FORMENTERA',2,'ISLAS BALEARES'),
 ('EXTREMADURA',1,'EXTREMADURA'),('GALICIA',1,'GALICIA'),('GARRAF',2,'CATALUÑA'),
 ('GIRONÈS',4,'CATALUÑA'),('LA GARROTXA',2,'CATALUÑA'),('LA NOGUERA',1,'CATALUÑA'),
 ('LA RIOJA',2,'LA RIOJA'),('LA SELVA',3,'CATALUÑA'),('LAS PALMAS',2,'ISLAS CANARIAS'),
 ('LES GARRIGUES',1,'CATALUÑA'),('LLUÇANÈS',1,'CATALUÑA'),
 ('MADRID (EXC. MADRID CIUDAD)',5,'MADRID'),('MADRID',6,'MADRID'),
 ('MALLORCA (EXC. PALMA)',3,'ISLAS BALEARES'),('MARESME',6,'CATALUÑA'),
 ('MENORCA',2,'ISLAS BALEARES'),('MOIANÈS',1,'CATALUÑA'),('MONTSIA',1,'CATALUÑA'),
 ('MURCIA',3,'MURCIA'),('NAVARRA',2,'NAVARRA'),('OSONA',2,'CATALUÑA'),
 ('PALLARS JUSSÀ',1,'CATALUÑA'),('PALLARS SOBIRÀ',1,'CATALUÑA'),
 ('PALMA DE MALLORCA',4,'ISLAS BALEARES'),('PAIS VASCO',4,'PAIS VASCO'),
 ("PLA DE L'ESTANY",2,'CATALUÑA'),("PLA D'URGELL",1,'CATALUÑA'),('PRIORAT',1,'CATALUÑA'),
 ("RIBERA D'EBRE",1,'CATALUÑA'),('RIPOLLES',1,'CATALUÑA'),
 ('SANTA CRUZ DE TENERIFE',4,'ISLAS CANARIAS'),('SEGARRA',1,'CATALUÑA'),
 ('SEGRIA',4,'CATALUÑA'),('SOLSONÈS',1,'CATALUÑA'),('TARRAGONES',3,'CATALUÑA'),
 ('TERRA ALTA',1,'CATALUÑA'),('URGELL',1,'CATALUÑA'),("VALL D'ARAN",1,'CATALUÑA'),
 ('VALLES OCCIDENTAL',7,'CATALUÑA'),('VALLES ORIENTAL',4,'CATALUÑA'),
 ('VALENCIA (CIUTAT)',4,'COMUNIDAD VALENCIANA'),
 ('LOGROÑO',0,'LA RIOJA'),  # comarca real usada en candidaturas, cupo ya contado en 'LA RIOJA'
]

# ---------- Candidaturas reales (id_origen, apellidos, nombre, territorio, idioma, email, ccaa, movil, estado, interes, seccion, tipo_asociado, presentada) ----------
CAND = [
('1','CALERO VALLS','JOAN','ALT EMPORDA','ca','jcalerovalls@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('2','RIGALL CARRE','PERE','ALT EMPORDA','ca','rigallbordas@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('3','GONZALEZ TORRES','ABEL','ALT PENEDES','ca','abel.gonzalez.to@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('4','CABRERA CRUZ','ISIDRO','ANDALUCIA (ALM,GRA,JAE,MAL)','es','icabreracruz@gmail.com','ANDALUCIA',None,'ACTIVO',True,'VELA ANDALUCIA ORIENTAL','DELEGADO',True),
('5','LOPEZ URQUIZAR','JOSE MANUEL','ANDALUCIA (ALM,GRA,JAE,MAL)','es','ascenjosemanuel2019@gmail.com','ANDALUCIA',None,'ACTIVO',True,None,'SOCIO',True),
('6','MARTINEZ GARCIA','MARCELO','ANDALUCIA (ALM,GRA,JAE,MAL)','es','frommotril@gmail.com','ANDALUCIA','640266805','ACTIVO',True,'FUTBOL GRANADA','DELEGADO',True),
('7','RUBI CASTILLO','FRANCISCO','ANDALUCIA (ALM,GRA,JAE,MAL)','es','frubi@caixabank.com','ANDALUCIA',None,'ACTIVO',True,'FUTBOL ALMERIA','DELEGADO',True),
('8','VANEGAS LOPEZ','JORGE JUAN','ANDALUCIA (ALM,GRA,JAE,MAL)','es','jjvanegas@caixabank.com','ANDALUCIA',None,'ACTIVO',True,None,'SOCIO',True),
('9','CODER GALLEGO','ELISA ISABEL','ANDALUCIA (HUE,COR,CAD,SEV)','es','eicoder@hotmail.com','ANDALUCIA',None,'ACTIVO',True,'GASTRONOMIA HUELVA','DELEGADO',True),
('10','MONTIJANO LOPEZ','SAMUEL','ANDALUCIA (HUE,COR,CAD,SEV)','es','samuelmontijano@yahoo.es','ANDALUCIA',None,'INACTIVO',False,'ESQUI CORDOBA','DELEGADO',False),
('11','VAZQUEZ PAVON','JUAN','ANDALUCIA (HUE,COR,CAD,SEV)','es','vazparra@yahoo.es','ANDALUCIA',None,'ACTIVO',True,'PESCA ANDALUCIA OCCIDENTAL','DELEGADO',True),
('12','RUBIALES ALVAREZ DARDET','FERNANDO','ANDALUCIA (SEVILLA CIUDAD)','es','fernandorubiales01@icloud.com','ANDALUCIA',None,'ACTIVO',True,'TRIATLON Y FONDISTAS SEVILLA','DELEGADO',True),
('13','COYA ALAEZ','LUIS','ASTURIAS','es','luiscoyaalaez@gmail.com','ASTURIAS',None,'ACTIVO',True,'HISTORIA ASTURIAS','DELEGADO',True),
('14','LUQUE SAN JUAN','JAVIER','ASTURIAS','es','jluquesj@gmail.com','ASTURIAS',None,'ACTIVO',True,'KARTING ASTURIAS','DELEGADO',True),
('15','SANFELIU SARRI','JOSEP','BAGES','ca','sanfeliu8789@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('16','BASORA SANJUAN','JOSEP MARIA','BAIX CAMP','ca','jmbasora@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('17','CASONI-VALENTI SAMARANCH','VERA PAOLA','BAIX EMPORDA','ca','verasonica@hotmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('18','CASTELLO PROVENSAL','CRISTINA','BAIX EMPORDA','ca','cristinacastelloprovensal@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('19','MATEU PALE','RAFAEL','BAIX EMPORDA','ca','rafelmateu@yahoo.es','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('20','LLISO LIS','ELISABET','BAIX LLOBREGAT','ca','bethlissol@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('21','MITJANS RIUS','JOSEP','BAIX LLOBREGAT','ca','mitjans.josep@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('22','RIU VIDAL','EDUARDO','BAIX LLOBREGAT','ca','lasoci.eduardriu@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('23','SIBERA ARESTE','JORDI','BAIX LLOBREGAT','ca','siberkey0@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('24','MENDOZA ROSSO','JOSEP','BAIX PENEDES','ca','peprosso@hotmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('25','MARIEGES ASENSIO','FERRAN','BARCELONA DTE. 02','ca','fmarieges@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('26','PADRO BALCELLS','PERE','BARCELONA DTE. 02','ca','perepadrob@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('27','PAEZ MARTINEZ','ROSER','BARCELONA DTE. 02','ca','paez.roser@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('28','POYATOS JORDA','XAVIER','BARCELONA DTE. 02','ca','prexavier@yahoo.es','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('29','CORRECHER CASTRO','JOSEP','BARCELONA DTE. 03','ca','josepcorrecher@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('30','RUIZ CABALLERO','JOAN FRANCESC','BARCELONA DTE. 03','ca','jfruizc.lasoci@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('31','AGEA TOMAS','RAFAEL','BARCELONA DTE. 04','ca','rafelagea@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('32','PLANDOLIT ARUMI','JOAN','BARCELONA DTE. 04','ca','golfbcn@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('33','GAZULLA BADENAS','FERMIN','BARCELONA DTE. 05','ca','fergaz1997@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('34','SOLANS NAVARRO','ANTONI','BARCELONA DTE. 05','ca','antonsol25@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('35','LUMBRERAS PALOMARES','LUIS','BARCELONA DTE. 06','ca','lumbreraspalomares@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('36','PUIG LLINARES','FERMIN','BARCELONA DTE. 06','ca','fermipuig@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('37','ROIG ROCA','FRANCESC XAVIER','BARCELONA DTE. 07','ca','fxroig@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('38','MONLEON NOVELLA','AMADOR','BARCELONA DTE. 10','ca','amonleonn@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('39','RAMOS HERRERO','MIQUEL','BARCELONA DTE. 10','ca','miquelramosbcn@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('40','GOMEZ GONZALEZ','JOSE MANUEL','CANTABRIA','es','gomezcaixa@gmail.com','CANTABRIA',None,'ACTIVO',True,None,'DELEGADO',True),
('41','ALONSO GONZALEZ','OSCAR','CASTILLA Y LEON','es','oscaralonsoglez@msn.com','CASTILLA Y LEON',None,'ACTIVO',True,None,'SOCIO',True),
('42','GALAN DE LA CONCEPCION','IRINEO','CASTILLA Y LEON','es','igalandela@gmail.com','CASTILLA Y LEON',None,'ACTIVO',True,None,'SOCIO',True),
('43','HORGA MANZANAL','GREGORIO','CASTILLA Y LEON','es','ghorga@caixabank.com','CASTILLA Y LEON',None,'ACTIVO',True,None,'SOCIO',True),
('44','MONTES HERNANDEZ','TEOFILO','CASTILLA Y LEON','es','amadeorey@me.com','CASTILLA Y LEON',None,'ACTIVO',True,'GOLF CASTILLA Y LEON','DELEGADO',True),
('45','PEREZ PANIEGO','ROBERTO','CASTILLA Y LEON','es','roberto.perezpa@gmail.com','CASTILLA Y LEON',None,'ACTIVO',True,None,'SOCIO',True),
('46','MUR PLEITE','DANIEL','CASTILLA-LA MANCHA','es','danimurp@gmail.com','CASTILLA-LA MANCHA',None,'ACTIVO',True,None,'SOCIO',True),
('47','ALBALADEJO GISBERT','JOSE JOAQUIN','COM. VALENCIANA (EXC.VALENCIA CIUTAT)','es','josealbala@telefonica.net','COMUNIDAD VALENCIANA',None,'ACTIVO',True,None,'DELEGADO',True),
('48','COLLADO SAN EUSTAQUIO','JUAN','COM. VALENCIANA (EXC.VALENCIA CIUTAT)','es','juancooperante@gmail.com','COMUNIDAD VALENCIANA',None,'ACTIVO',True,None,'DELEGADO',True),
('49','GARCIA ESPELETA','RAMON','COM. VALENCIANA (EXC.VALENCIA CIUTAT)','es','ramon.garcia.e@caixabank.com','COMUNIDAD VALENCIANA',None,'ACTIVO',True,None,'SOCIO',True),
('50','SONADELLES PLA','ALICIA','COM. VALENCIANA (EXC.VALENCIA CIUTAT)','es','asonadelles@hotmail.es','COMUNIDAD VALENCIANA',None,'ACTIVO',True,None,'SOCIO',True),
('51','PALERM SERRA','JOAN ANTONI','EIVISSA I FORMENTERA','ca','joanpalerm@gmail.com','ISLAS BALEARES',None,'ACTIVO',True,None,'SOCIO',True),
('52','RIBAS FERRER','MARIA CARMEN','EIVISSA I FORMENTERA','ca','mcribas2@gmail.com','ISLAS BALEARES',None,'ACTIVO',True,None,'SOCIO',True),
('53','JEREZ FONTAO','LLUIS','GIRONÈS','ca','jerser5@hotmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('54','BUSQUETS PICART','JOSEP','LA GARROTXA','ca','jbusquets04@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('55','MAYOLA PRAT','XAVIER','LA GARROTXA','ca','xevimayola@hotmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('56','GONZALEZ CABRERA','ISRAEL','LAS PALMAS','es','israel.gonzalez@caixabank.com','ISLAS CANARIAS',None,'ACTIVO',True,None,'SOCIO',True),
('57','SANMARTIN GARCIA DE','JOSE CARLOS','LAS PALMAS','es','cirus@telefonica.net','ISLAS CANARIAS',None,'ACTIVO',True,None,'SOCIO',True),
('58','TOVAL DEL SOL','RAFAEL','MADRID','es','rtovaldel@gmail.com','MADRID',None,'ACTIVO',True,'F.S. MADRID','DELEGADO',True),
('59','DEL CASTILLO GARCIA','CANDIDO','MADRID (EXC. MADRID CIUDAD)','es','candidocastillo@hotmail.com','MADRID',None,'ACTIVO',True,'MONTAÑA MADRID','DELEGADO',True),
('60','GOMEZ LOPEZ','FRANCISCO','MADRID (EXC. MADRID CIUDAD)','es','pinareja@telefonica.net','MADRID',None,'ACTIVO',True,'MUSICA MODERNA MADRID','DELEGADO',True),
('61','TORREGO DE FRUTOS','FELIX','MADRID (EXC. MADRID CIUDAD)','es','torrego47@yahoo.es','MADRID',None,'INACTIVO',False,None,'SOCIO',False),
('62','MAYRATA MASCARO','MIQUEL','MALLORCA (EXC. PALMA)','ca','mmairatam@hotmail.com','ISLAS BALEARES',None,'ACTIVO',True,None,'SOCIO',True),
('63','PLANELLS TORRES','JOAN','MALLORCA (EXC. PALMA)','ca','jplanells1@yahoo.es','ISLAS BALEARES',None,'ACTIVO',True,None,'SOCIO',True),
('64','TOMAS MORLA','DAMIAN','MALLORCA (EXC. PALMA)','ca','teatrepicadis@gmail.com','ISLAS BALEARES',None,'ACTIVO',True,'HISTORIA MALLORCA','DELEGADO',True),
('65','DEL RIO HUERTAS','ANTONIO','MARESME','ca','delriohuertas@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('66','SORIANO ADZERIAS','ANDREU','MARESME','ca','andreusoriano50@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('67','SALAS HOYOS','PEDRO JOSE','MURCIA','es','pjsalas@caixabank.com','MURCIA',None,'ACTIVO',True,None,'SOCIO',True),
('68','DE IRUETA CALCEDO','ALVARO','PAIS VASCO','es','beverlymartinezgarcia@gmail.com','PAIS VASCO',None,'ACTIVO',True,'PADEL PAIS VASCO','DELEGADO',True),
('69','MINTEGUI ECHALECU','IBON','PAIS VASCO','es','imintegui73@gmail.com','PAIS VASCO',None,'ACTIVO',True,'BALONCESTO BIZKAIA ARABA','DELEGADO',True),
('70','BARCELO RIERA','FRANCESC','PALMA DE MALLORCA','ca','xisbari@hotmail.com','ISLAS BALEARES',None,'ACTIVO',True,'JOCS DE TAULA MALLORCA','DELEGADO',True),
('71','CRESPO MARTIN','MANUEL','PALMA DE MALLORCA','ca','papa.crespo@gmail.com','ISLAS BALEARES',None,'ACTIVO',True,None,'SOCIO',True),
('72','FERRER MOTOS','ENRIC','PALMA DE MALLORCA','ca','eferrermotos@hotmail.com','ISLAS BALEARES',None,'ACTIVO',True,'GOLF MALLORCA','DELEGADO',True),
('73','TUGORES SOLIVELLAS','JUAN','PALMA DE MALLORCA','ca','tugores45@gmail.com','ISLAS BALEARES',None,'ACTIVO',True,None,'SOCIO',True),
('74','COLL COMERMA','JOAN',"PLA DE L'ESTANY",'ca','joancollc@hotmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('75','TORRAS CONGOST','MARTIRIA',"PLA DE L'ESTANY",'ca','martiriatorras@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('76','CLUA LLOP','JOSEP','PRIORAT','ca','josepcluallop@hotmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('77','AYALA CORREA','CEFERINO GUILLERMO','SANTA CRUZ DE TENERIFE','es','cgayala@caixabank.com','ISLAS CANARIAS',None,'ACTIVO',True,None,'SOCIO',True),
('78','CABA BETANCORT','MARIA DEL MAR','SANTA CRUZ DE TENERIFE','es','marcaba65@gmail.com','ISLAS CANARIAS',None,'ACTIVO',True,'GASTRONOMIA TENERIFE','DELEGADO',True),
('79','PEREZ PEREZ','SIXTO GREGORIO','SANTA CRUZ DE TENERIFE','es','goyoperez23@gmail.com','ISLAS CANARIAS',None,'ACTIVO',True,'F.S. TENERIFE','DELEGADO',True),
('80','CREUS VILA','JORDI','SEGARRA','ca','jordi.creusvila@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('81','PICANYOL TARRES','JOAN','SEGRIA','ca','joan.piccas@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('82','MEIX BOIRA','JOSE RAMON','TARRAGONES','ca','josepmeix@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('83','GONZALEZ RODRIGUEZ','JOSE MANUEL','VALENCIA (CIUTAT)','es','jmgr_9@hotmail.com','COMUNIDAD VALENCIANA',None,'ACTIVO',True,None,'DELEGADO',True),
('84','HUERTA PALAU','JESUS MANUEL','VALENCIA (CIUTAT)','es','j.m.a.huerta@gmail.com','COMUNIDAD VALENCIANA',None,'ACTIVO',True,None,'DELEGADO',True),
('85','GARCIA SANTANACH','ROBERT',"VALL D'ARAN",'ca','robertgsan@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('86','URGELES BORRAS','DELFI','VALLES OCCIDENTAL','ca','delfi.urgeles@gmail.com','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('87','ALEGRET LLORENS','RICARDO','VALLES ORIENTAL','es','ricardoalegret@ricardoalegret.es','CATALUÑA',None,'ACTIVO',True,None,'DELEGADO',True),
('VAC3544754300','GONZALEZ MUÑOZ','JOSE LUIS','ANDALUCIA (HUE,COR,CAD,SEV)','es','jlmunoz@gmail.com','ANDALUCIA',None,'ACTIVO',True,'KARTING SEVILLA','DELEGADO',True),
('VAC3544905571','ESPINOSA GARCIA','JUAN CARLOS','ANDALUCIA (HUE,COR,CAD,SEV)','es','espyweb@gmail.com','ANDALUCIA',None,'ACTIVO',True,'MULTIJUEGOS SEVILLA','DELEGADO',True),
('VAC3545046118','LOPEZ RIVERA','MANUEL','ANDALUCIA (SEVILLA CIUDAD)','es',None,'ANDALUCIA',None,'ACTIVO',True,'MULTIAVENTURA SEVILLA','DELEGADO',True),
('VAC3545183640','CORTES LOPEZ','CARLOS JAVIER','ANDALUCIA (SEVILLA CIUDAD)','es',None,'ANDALUCIA',None,'ACTIVO',True,'VELA Y MOTONAUTICA HUELVA','DELEGADO',True),
('VAC3545683377','GARCIA CABANES','JORGE','ARAGÓN','es',None,'ARAGON',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3545823395','FLAMARIQUE BORREGO','FERNANDO','ARAGÓN','es',None,'ARAGON',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3546727888','Numero 1',None,'BAIX EBRE','es',None,'CATALUÑA',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3548854337','Numero 8',None,'BARCELONA DTE. 05','es',None,'CATALUÑA',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3554701948','LEMOS SANTIAGO','DAVID','EXTREMADURA','es',None,'EXTREMADURA',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3555324431','SOTO VARELA','JAVIER','GALICIA','es',None,'GALICIA',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3556071580','Numero 7',None,'GIRONÈS','es',None,'CATALUÑA',None,'ACTIVO',True,None,'SOCIO',True),
('VAC3556733098','LASANTA ESTEBAN','RAQUEL','LOGROÑO','es',None,'LA RIOJA',None,'ACTIVO',True,'ACTIVIDAD FISICA LOGROÑO','DELEGADO',True),
]

def esc(v):
    if v is None: return 'null'
    return "'" + str(v).replace("'", "''") + "'"

def slug(s):
    s = (s or '').lower()
    for a,b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),(' ','.'),(',','')]:
        s = s.replace(a,b)
    return re.sub(r'[^a-z0-9.]', '', s)

out = []
out.append("-- ============================================================")
out.append("-- Migracion de datos reales RECTORES (Google Sheets -> Supabase)")
out.append("-- ============================================================\n")

out.append("insert into ccaa (codigo, nombre, es_afin) values")
out.append(",\n".join(f"  ({esc(k)}, {esc(k.title())}, {str(v).lower()})" for k,v in CCAA.items()) + "\non conflict (codigo) do nothing;\n")

out.append("insert into territorios (ccaa_id, nombre, cuota_total) values")
rows=[f"  ((select id from ccaa where codigo={esc(ccaa)}), {esc(nombre)}, {cuota})" for nombre,cuota,ccaa in TERRITORIOS]
out.append(",\n".join(rows) + "\non conflict (ccaa_id, nombre) do nothing;\n")

socio_vals=[]
cand_vals=[]
for (idorig,ape,nom,terr,idioma,email,ccaa,movil,estado,interes,seccion,tipo,presentada) in CAND:
    if not ape:
        continue
    final_email = email or f"{slug(nom)}.{slug(ape)}.pendiente@pendiente.lasoci.org"
    socio_vals.append(f"  ({esc(ape)}, {esc(nom or '')}, {esc(final_email)}, {esc(movil)}, {esc(idioma)})")
    cand_vals.append(
        f"  ((select id from socios where email={esc(final_email)}), "
        f"(select id from territorios where nombre={esc(terr)}), "
        f"{esc(estado)}, {esc(tipo)}, {esc(seccion)}, {str(interes).lower()}, {str(presentada).lower()})"
    )

out.append("insert into socios (apellidos, nombre, email, telefono, idioma, rol, activo) values")
socio_lines = [v[:-1] + ", 'socio', true)" for v in socio_vals]
out.append(",\n".join(socio_lines) + "\non conflict (email) do nothing;\n")

out.append("insert into candidaturas (socio_id, territorio_id, estado, tipo_asociado, seccion, interes_rector, candidatura_presentada) values")
out.append(",\n".join(cand_vals) + ";\n")

out.append("-- Snapshot inicial (14/6/2026)")
out.append("""insert into snapshots (fecha, etiqueta, activos, pendientes, inactivos, candidaturas_total, afines) values
  ('2026-06-14', 'Situación inicial', 87, 113, 0, 87, 31);""")

snap_ccaa = {"CATALUÑA":(42,83),"ANDALUCIA":(9,4),"ASTURIAS":(2,0),"CANTABRIA":(1,0),"CASTILLA Y LEON":(5,0),
 "CASTILLA-LA MANCHA":(1,0),"COMUNIDAD VALENCIANA":(6,4),"ISLAS BALEARES":(9,2),"ISLAS CANARIAS":(5,1),
 "MADRID":(4,7),"MURCIA":(1,2),"PAIS VASCO":(2,2),"ARAGON":(0,2),"EXTREMADURA":(0,1),"GALICIA":(0,1),
 "LA RIOJA":(0,2),"NAVARRA":(0,2)}
out.append("\ninsert into snapshots_ccaa (snapshot_id, ccaa_id, activos, pendientes) values")
rows=[f"  ((select id from snapshots where fecha='2026-06-14'), (select id from ccaa where codigo={esc(k)}), {a}, {p})" for k,(a,p) in snap_ccaa.items()]
out.append(",\n".join(rows) + ";")

with open('/home/claude/lasoci-web/db/migracion_datos.sql','w') as f:
    f.write("\n".join(out))
print("Generado. Socios:", len(socio_vals), "Candidaturas:", len(cand_vals))

