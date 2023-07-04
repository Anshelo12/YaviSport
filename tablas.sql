create table inscripcione(
	idins serial primary key not null,
	numeroe int not null,
	nombree varchar(25) not null,
	nombred varchar(25) not null,
	telefono varchar(10) not null,
	Categoriae Varchar(10) not null
)

create table programacionp(
	idp serial primary key not null,
	equipo1pro varchar(25) not null,
	equipo2pro varchar(25) not null,
	fechapro date not null,
	estadiopro varchar(25) not null
)

create table partidosju(
	idj serial primary key not null,
	equipo1jug varchar(25) not null,
	equipo2jug varchar(25) not null,
	equipogana varchar(25) not null
)

select * from inscripcione
select * from programacionp
select * from partidosju
select * from users

truncate table inscripcione