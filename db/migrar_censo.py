def esc(v):
    if v is None: return 'null'
    return "'" + str(v).replace("'", "''") + "'"

# (ccaa_codigo, provincia, nombre_censo, n_socios_actual, nombre_territorio_real)
DATOS = [
 ('ANDALUCIA','Almeria/Granada/Malaga/Jaen','ANDALUCÍA (AL GR MA JA)',317,'ANDALUCIA (ALM,GRA,JAE,MAL)'),
 ('ANDALUCIA','Huelva/Cordoba/Cadiz/Sevilla','ANDALUCIA (HU CO CA SE)',376,'ANDALUCIA (HUE,COR,CAD,SEV)'),
 ('ANDALUCIA','Sevilla','ANDALUCIA (SEVILLA CIUDAD)',152,'ANDALUCIA (SEVILLA CIUDAD)'),
 ('ARAGON','Aragon','ARAGON',84,'ARAGÓN'),
 ('ASTURIAS','Asturias','ASTURIAS',48,'ASTURIAS'),
 ('CANTABRIA','Cantabria','CANTABRIA',45,'CANTABRIA'),
 ('CASTILLA Y LEON','Castilla y Leon','CASTILLA Y LEON',313,'CASTILLA Y LEON'),
 ('CASTILLA-LA MANCHA','Castilla-La Mancha','CASTILLA-LA MANCHA',39,'CASTILLA-LA MANCHA'),
 ('CATALUÑA','Barcelona','ALT PENEDES',47,'ALT PENEDES'),
 ('CATALUÑA','Barcelona','ANOIA',59,'ANOIA'),
 ('CATALUÑA','Barcelona','BAGES',118,'BAGES'),
 ('CATALUÑA','Barcelona','BAIX LLOBREGAT',475,'BAIX LLOBREGAT'),
 ('CATALUÑA','Barcelona','BARCELONES',209,'BARCELONÈS'),
 ('CATALUÑA','Barcelona','BCN 01 CIUTAT VELLA',27,'BARCELONA DTE. 01'),
 ('CATALUÑA','Barcelona','BCN 02 EIXAMPLE',617,'BARCELONA DTE. 02'),
 ('CATALUÑA','Barcelona','BCN 03 SANTS-MONTJUIC',185,'BARCELONA DTE. 03'),
 ('CATALUÑA','Barcelona','BCN 04 LES CORTS',357,'BARCELONA DTE. 04'),
 ('CATALUÑA','Barcelona','BCN 05 SARRIA-SANT GERVASI',359,'BARCELONA DTE. 05'),
 ('CATALUÑA','Barcelona','BCN 06 GRACIA',279,'BARCELONA DTE. 06'),
 ('CATALUÑA','Barcelona','BCN 07 HORTA-GUINARDO',207,'BARCELONA DTE. 07'),
 ('CATALUÑA','Barcelona','BCN 08 NOU BARRIS',81,'BARCELONA DTE. 08'),
 ('CATALUÑA','Barcelona','BCN 09 SANT ANDREU',134,'BARCELONA DTE. 09'),
 ('CATALUÑA','Barcelona','BCN 10 SANT MARTI',263,'BARCELONA DTE. 10'),
 ('CATALUÑA','Barcelona','BERGUEDA',28,'BERGUEDÀ'),
 ('CATALUÑA','Barcelona','GARRAF',87,'GARRAF'),
 ('CATALUÑA','Barcelona','LLUÇANES',7,'LLUÇANÈS'),
 ('CATALUÑA','Barcelona','MARESME',398,'MARESME'),
 ('CATALUÑA','Barcelona','MOIANES',8,'MOIANÈS'),
 ('CATALUÑA','Barcelona','OSONA',97,'OSONA'),
 ('CATALUÑA','Barcelona','VALLES OCCIDENTAL',465,'VALLES OCCIDENTAL'),
 ('CATALUÑA','Barcelona','VALLES ORIENTAL',220,'VALLES ORIENTAL'),
 ('CATALUÑA','Girona','ALT EMPORDA',124,'ALT EMPORDA'),
 ('CATALUÑA','Girona','BAIX EMPORDA',149,'BAIX EMPORDA'),
 ('CATALUÑA','Girona','CERDANYA',17,'CERDANYA'),
 ('CATALUÑA','Girona','GIRONES',282,'GIRONÈS'),
 ('CATALUÑA','Girona','LA GARROTXA',48,'LA GARROTXA'),
 ('CATALUÑA','Girona','LA SELVA',143,'LA SELVA'),
 ('CATALUÑA','Girona',"PLA D'ESTANY",44,"PLA DE L'ESTANY"),
 ('CATALUÑA','Girona','RIPOLLES',27,'RIPOLLES'),
 ('CATALUÑA','Lleida','ALT URGELL',35,'ALT URGELL'),
 ('CATALUÑA','Lleida','ALTA RIBAGORÇA',5,'ALTA RIBAGORÇA'),
 ('CATALUÑA','Lleida','LA NOGUERA',35,'LA NOGUERA'),
 ('CATALUÑA','Lleida','LES GARRIGUES',17,'LES GARRIGUES'),
 ('CATALUÑA','Lleida','PALLARS JUSSA',30,'PALLARS JUSSÀ'),
 ('CATALUÑA','Lleida','PALLARS SOBIRA',9,'PALLARS SOBIRÀ'),
 ('CATALUÑA','Lleida',"PLA D'URGELL",17,"PLA D'URGELL"),
 ('CATALUÑA','Lleida','SEGARRA',11,'SEGARRA'),
 ('CATALUÑA','Lleida','SEGRIA',233,'SEGRIA'),
 ('CATALUÑA','Lleida','SOLSONES',15,'SOLSONÈS'),
 ('CATALUÑA','Lleida','URGELL',31,'URGELL'),
 ('CATALUÑA','Lleida',"VALL D'ARAN",11,"VALL D'ARAN"),
 ('CATALUÑA','Tarragona','ALT CAMP',23,'ALT CAMP'),
 ('CATALUÑA','Tarragona','BAIX CAMP',118,'BAIX CAMP'),
 ('CATALUÑA','Tarragona','BAIX EBRE',59,'BAIX EBRE'),
 ('CATALUÑA','Tarragona','BAIX PENEDES',25,'BAIX PENEDES'),
 ('CATALUÑA','Tarragona','CONCA DE BARBERA',18,'CONCA DE BARBERÀ'),
 ('CATALUÑA','Tarragona','MONTSIA',32,'MONTSIA'),
 ('CATALUÑA','Tarragona','PRIORAT',6,'PRIORAT'),
 ('CATALUÑA','Tarragona',"RIBERA D'EBRE",8,"RIBERA D'EBRE"),
 ('CATALUÑA','Tarragona','TARRAGONES',152,'TARRAGONES'),
 ('CATALUÑA','Tarragona','TERRA ALTA',7,'TERRA ALTA'),
 ('COMUNIDAD VALENCIANA','Valencia','COM. VALENC. (EXC. VALENCIA)',413,'COM. VALENCIANA (EXC.VALENCIA CIUTAT)'),
 ('COMUNIDAD VALENCIANA','Valencia','VALENCIA CIUTAT',232,'VALENCIA (CIUTAT)'),
 ('EXTREMADURA','Extremadura','EXTREMADURA',19,'EXTREMADURA'),
 ('GALICIA','Galicia','GALICIA',36,'GALICIA'),
 ('ISLAS BALEARES','Baleares','EIVISSA I FORMENTERA',95,'EIVISSA I FORMENTERA'),
 ('ISLAS BALEARES','Baleares','MALLORCA (EXC. PALMA)',209,'MALLORCA (EXC. PALMA)'),
 ('ISLAS BALEARES','Baleares','MENORCA',65,'MENORCA'),
 ('ISLAS BALEARES','Baleares','PALMA DE MALLORCA',210,'PALMA DE MALLORCA'),
 ('ISLAS CANARIAS','Las Palmas','LAS PALMAS',78,'LAS PALMAS'),
 ('ISLAS CANARIAS','Santa Cruz de Tenerife','SANTA CRUZ DE TENERIFE',228,'SANTA CRUZ DE TENERIFE'),
 ('LA RIOJA','La Rioja','LA RIOJA',64,'LA RIOJA'),
 ('MADRID','Madrid','MADRID (EXC. CIUDAD)',334,'MADRID (EXC. MADRID CIUDAD)'),
 ('MADRID','Madrid','MADRID CIUDAD',419,'MADRID'),
 ('MURCIA','Murcia','MURCIA',221,'MURCIA'),
 ('NAVARRA','Navarra','NAVARRA',64,'NAVARRA'),
 ('PAIS VASCO','Pais Vasco','PAIS VASCO',226,'PAIS VASCO'),
]

out = []
total = 0
sin_match = []
for ccaa, prov, nombre_censo, n, nombre_real in DATOS:
    total += n
    out.append(
        f"insert into censo (territorio_id, apellidos, nombre, n_socios, provincia) values "
        f"((select id from territorios where nombre={esc(nombre_real)}), null, {esc(nombre_censo)}, {n}, {esc(prov)});"
    )

with open('/home/claude/lasoci-web/db/migracion_censo.sql', 'w') as f:
    f.write("\n".join(out))
print("Filas:", len(DATOS), "- Total socios censo:", total)
