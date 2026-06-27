-- ============================================================
-- RECTORES — esquema relacional (Postgres / Supabase)
-- Pensado para ser portable a Azure Database for PostgreSQL
-- sin cambios de tipos (solo tipos ANSI estándar, sin
-- extensiones propietarias salvo gen_random_uuid()/pgcrypto,
-- disponible también en Azure Postgres Flexible Server).
-- ============================================================

create extension if not exists pgcrypto;

-- ============================================================
-- BLOQUE A — OPERATIVO (sustituye al Google Sheet RECTORES)
-- ============================================================

create table ccaa (
  id          uuid primary key default gen_random_uuid(),
  codigo      text not null unique,        -- 'ANDALUCIA', 'MADRID', ...
  nombre      text not null,               -- 'Andalucía', 'Madrid', ...
  es_afin     boolean not null default false,
  created_at  timestamptz not null default now()
);

create table territorios (
  id           uuid primary key default gen_random_uuid(),
  ccaa_id      uuid not null references ccaa(id) on delete restrict,
  nombre       text not null,              -- 'Madrid Ciudad', 'Andalucía (Sevilla Ciudad)', ...
  cuota_total  integer not null default 0 check (cuota_total >= 0),
  activo       boolean not null default true,
  created_at   timestamptz not null default now(),
  unique (ccaa_id, nombre)
);

create table personas (
  id          uuid primary key default gen_random_uuid(),
  nombre      text not null,
  apellidos   text not null,
  email       text,
  movil       text,
  idioma      text default 'es',
  created_at  timestamptz not null default now()
);

create type estado_candidatura as enum ('ACTIVO', 'PENDIENTE', 'INACTIVO', 'VACANTE');

create table candidaturas (
  id                  uuid primary key default gen_random_uuid(),
  persona_id          uuid references personas(id) on delete set null,  -- null = plaza vacante
  territorio_id       uuid not null references territorios(id) on delete cascade,
  estado              estado_candidatura not null default 'PENDIENTE',
  tipo_asociado       text,                -- 'SOCIO' | 'DELEGADO'
  seccion             text,
  interes_rector       boolean default false,
  candidatura_presentada boolean default false,
  presentada_en       date,
  notas               text,
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now()
);

create index idx_candidaturas_territorio on candidaturas(territorio_id);
create index idx_candidaturas_estado on candidaturas(estado);

-- ============================================================
-- BLOQUE B — PLANIFICACIÓN / SIMULACIÓN (CRM Reorganización)
-- Todo lo "borrador" vive separado de los datos operativos.
-- ============================================================

create type estado_escenario as enum ('borrador', 'guardado_final');

create table escenarios (
  id          uuid primary key default gen_random_uuid(),
  nombre      text not null,               -- 'Borrador 2026', 'Estructura final v2'...
  estado      estado_escenario not null default 'borrador',
  creado_por  uuid references auth.users(id),
  created_at  timestamptz not null default now()
);

create table territorios_propuestos (
  id                 uuid primary key default gen_random_uuid(),
  escenario_id       uuid not null references escenarios(id) on delete cascade,
  ccaa_id            uuid not null references ccaa(id) on delete restrict,
  nombre             text not null,        -- 'Sevilla Metropolitana (NUEVO)', ...
  socios_estimados   integer not null default 0,
  rectores_objetivo  integer not null default 0,
  orden              integer default 0,
  created_at         timestamptz not null default now()
);

create table censo (
  id            uuid primary key default gen_random_uuid(),
  territorio_id uuid not null references territorios(id) on delete cascade,
  apellidos     text,
  nombre        text,
  n_socios      integer not null default 0,
  provincia     text,
  created_at    timestamptz not null default now()
);

create table censo_reorganizacion (
  id                        uuid primary key default gen_random_uuid(),
  censo_id                  uuid not null references censo(id) on delete cascade,
  escenario_id              uuid not null references escenarios(id) on delete cascade,
  territorio_propuesto_id   uuid references territorios_propuestos(id) on delete set null,
  delegado_seccion          text,
  provincia_nueva           text,
  socios_nuevo_territorio   integer,
  updated_at                timestamptz not null default now(),
  unique (censo_id, escenario_id)
);

create type categoria_nota as enum ('Regla', 'Hallazgo', 'Decisión', 'Pendiente');

create table notas_estrategia (
  id           uuid primary key default gen_random_uuid(),
  escenario_id uuid references escenarios(id) on delete set null,
  categoria    categoria_nota not null default 'Regla',
  texto        text not null,
  autor_id     uuid references auth.users(id),
  created_at   timestamptz not null default now()
);

create table snapshots (
  id                uuid primary key default gen_random_uuid(),
  fecha             date not null,
  etiqueta          text,
  activos           integer not null default 0,
  pendientes        integer not null default 0,
  inactivos         integer not null default 0,
  candidaturas_total integer not null default 0,
  afines            integer not null default 0,
  created_at        timestamptz not null default now()
);

create table snapshots_ccaa (
  id           uuid primary key default gen_random_uuid(),
  snapshot_id  uuid not null references snapshots(id) on delete cascade,
  ccaa_id      uuid not null references ccaa(id) on delete cascade,
  activos      integer not null default 0,
  pendientes   integer not null default 0,
  unique (snapshot_id, ccaa_id)
);

-- ============================================================
-- BLOQUE C — CONTROL DE ACCESO
-- ============================================================

create type rol_usuario as enum ('socio', 'delegado_rectores', 'admin_rectores', 'superadmin');

create table perfiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  rol           rol_usuario not null default 'socio',
  territorio_id uuid references territorios(id) on delete set null,  -- solo aplica a delegados
  created_at    timestamptz not null default now()
);

create table periodo_electoral (
  id            uuid primary key default gen_random_uuid(),
  activo        boolean not null default false,
  fecha_inicio  date,
  fecha_fin     date,
  descripcion   text,
  created_at    timestamptz not null default now()
);

-- Solo debe existir un periodo activo a la vez
create unique index uq_periodo_activo on periodo_electoral (activo) where (activo = true);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

alter table ccaa enable row level security;
alter table territorios enable row level security;
alter table personas enable row level security;
alter table candidaturas enable row level security;
alter table escenarios enable row level security;
alter table territorios_propuestos enable row level security;
alter table censo enable row level security;
alter table censo_reorganizacion enable row level security;
alter table notas_estrategia enable row level security;
alter table snapshots enable row level security;
alter table snapshots_ccaa enable row level security;
alter table perfiles enable row level security;
alter table periodo_electoral enable row level security;

-- Función helper: rol del usuario autenticado
create or replace function auth_rol() returns rol_usuario as $$
  select rol from perfiles where id = auth.uid();
$$ language sql stable security definer;

create or replace function hay_periodo_activo() returns boolean as $$
  select exists (select 1 from periodo_electoral where activo = true and now()::date between fecha_inicio and fecha_fin);
$$ language sql stable security definer;

-- Lectura pública de datos operativos (ccaa/territorios/candidaturas/personas)
-- solo si hay periodo electoral activo, o si el usuario ya es admin/delegado.
create policy "lectura_operativa" on ccaa for select
  using (hay_periodo_activo() or auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));
create policy "lectura_operativa" on territorios for select
  using (hay_periodo_activo() or auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));
create policy "lectura_operativa" on candidaturas for select
  using (hay_periodo_activo() or auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));
create policy "lectura_operativa" on personas for select
  using (hay_periodo_activo() or auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));
create policy "lectura_snapshots" on snapshots for select
  using (hay_periodo_activo() or auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));
create policy "lectura_snapshots_ccaa" on snapshots_ccaa for select
  using (hay_periodo_activo() or auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));

-- Escritura operativa: delegado solo en su territorio, admin en todos
create policy "escritura_delegado_propio" on candidaturas for update
  using (
    auth_rol() in ('admin_rectores','superadmin')
    or (auth_rol() = 'delegado_rectores' and territorio_id = (select territorio_id from perfiles where id = auth.uid()))
  );
create policy "insercion_admin" on candidaturas for insert
  with check (auth_rol() in ('delegado_rectores','admin_rectores','superadmin'));
create policy "borrado_admin" on candidaturas for delete
  using (auth_rol() in ('admin_rectores','superadmin'));

-- Bloque de planificación/simulación: SIEMPRE solo admin (nunca público, con o sin periodo electoral)
create policy "solo_admin" on escenarios for all
  using (auth_rol() in ('admin_rectores','superadmin'));
create policy "solo_admin" on territorios_propuestos for all
  using (auth_rol() in ('admin_rectores','superadmin'));
create policy "solo_admin" on censo for all
  using (auth_rol() in ('admin_rectores','superadmin'));
create policy "solo_admin" on censo_reorganizacion for all
  using (auth_rol() in ('admin_rectores','superadmin'));
create policy "solo_admin" on notas_estrategia for all
  using (auth_rol() in ('admin_rectores','superadmin'));

-- Perfiles: cada usuario ve el suyo; admin ve todos
create policy "ver_propio_perfil" on perfiles for select
  using (id = auth.uid() or auth_rol() in ('admin_rectores','superadmin'));
create policy "admin_gestiona_perfiles" on perfiles for update
  using (auth_rol() in ('admin_rectores','superadmin'));

-- Periodo electoral: lectura pública (para mostrar/ocultar el enlace), escritura solo admin
create policy "lectura_publica_periodo" on periodo_electoral for select using (true);
create policy "admin_gestiona_periodo" on periodo_electoral for all
  using (auth_rol() in ('admin_rectores','superadmin'));
