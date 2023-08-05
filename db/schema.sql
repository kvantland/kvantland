drop schema if exists Квантландия cascade;
create schema Квантландия;

set search_path to Квантландия, public;

create table Тип (
	тип int primary key generated always as identity
	, код text not null unique
	, название text not null unique
);

create table Город (
	город int primary key generated always as identity
	, название text not null unique
	, положение point
);

create table Задача (
	задача int primary key generated always as identity
	, город int not null references Город on delete cascade
	, тип int not null references Тип on delete restrict
	, название text not null unique
	, положение point
	, баллы int not null
);

create table Вариант (
	вариант int primary key generated always as identity
	, задача int not null references Задача on delete cascade
	, описание text not null
	, содержание jsonb not null
);

create table Ученик (
	ученик int primary key generated always as identity
	, логин text not null unique
	, пароль bytea
	, имя text
	, счёт int not null default 10
);

create table ТекущаяЗадача (
	ученик int not null unique references Ученик on delete cascade,
	вариант int not null references Вариант on delete cascade,
	primary key (ученик, вариант)
);

create table ЗакрытиеЗадачи (
	ученик int not null references Ученик on delete cascade,
	задача int not null references Задача on delete cascade,
	primary key (ученик, задача)
);

insert into Тип (код, название) values
('radio', 'С выбором ответа'),
('integer', 'С целочисленным ответом');

-- kate: syntax SQL (PostgreSQL);
