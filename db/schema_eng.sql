drop schema if exists Kvantland cascade;
create schema Kvantland;
set search_path to Kvantland, public;

create table Type_ (
	type_ int primary key generated always as identity
	, code text not null unique
);

create table Town (
	town int primary key generated always as identity
	, name text not null unique
	, position point
);

create table Problem (
	problem int primary key generated always as identity
	, town int not null references Town on delete cascade
	, type_ int not null references Type_ on delete restrict
	, name text not null unique
	, position point
	, points int not null
	, image text
	, tournament int not null
);

create table Hint (
	problem int not null references Problem on delete cascade,
	content text not null,
	cost int not null,
	primary key (problem)
);

create table Variant (
	variant int primary key generated always as identity
	, problem int not null references Problem on delete cascade
	, description text not null
	, content jsonb not null
);

create table Student (
	student int primary key generated always as identity
	, login text not null unique
	, password text
	, name text
	, surname text
	, school text 
  	, clas text
  	, town text
  	, email text
  	, is_finished bool not null default false
	, score int not null default 10 check (score >= 0)
);

create table AvailableProblem (
	student int not null references Student on delete cascade,
	variant int not null references Variant on delete restrict,
	answer_true bool null,
	answer_given bool generated always as (answer_true is not null) stored,
	hint_taken bool not null default false,
	xhr_amount int not null default 0,
	answer text,
	solution text,
	curr jsonb,
	primary key (student, variant)
);

create table Score (
	student int not null references Student on delete cascade,
	tournament int not null,
	score int not null default 10 check(score >= 0)
);

