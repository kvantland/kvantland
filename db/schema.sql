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
	, изображение text
);

create table Подсказка (
	задача int not null references Задача on delete cascade,
	текст text not null,
	стоимость int not null,
	primary key (задача)
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
	, пароль text
	, имя text
	, счёт int not null default 10 check (счёт >= 0)
);

create table ДоступнаяЗадача (
	ученик int not null references Ученик on delete cascade,
	вариант int not null references Вариант on delete restrict,
	ответ_верен bool null,
	ответ_дан bool generated always as (ответ_верен is not null) stored,
	подсказка_взята bool not null default false,
	primary key (ученик, вариант)
);

-- kate: syntax SQL (PostgreSQL);
