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

create table Season (
	season int not null,
	tournament int not null
);

create table Previousmail (
	student int not null references Student on delete cascade,
	email text
);

insert into Kvantland.Type_ (code) (select код from Квантландия.Тип ORDER BY тип ASC);

insert into Kvantland.Town (name, position) values
('Чиселбург', '(436,411)'),
('Остров Лжецов', '(926,522)'),
('Головоломск', '(323,256)'),
('Геома', '(782,383)'),
('Республика Комби', '(1020,270)');


insert into Kvantland.Problem (town, points, name, type_, image, tournament) (select город, баллы, название, тип, изображение, 1 from Квантландия.Задача ORDER BY задача ASC);

insert into Kvantland.Hint (problem, content, cost) (select задача, текст, стоимость from Квантландия.Подсказка ORDER BY задача ASC);

insert into Kvantland.Variant (problem, description, content) (select задача, описание, содержание from Квантландия.Вариант ORDER BY вариант ASC);

insert into Kvantland.Student (login, password, name, surname, school, clas, town, email, is_finished, score) (select логин, пароль, имя, фамилия, школа, класс, город, null, false, счёт + 10 from Квантландия.Ученик ORDER BY ученик ASC);

insert into Kvantland.AvailableProblem (student, variant, answer_true, hint_taken, answer, solution) 
	(select ученик, вариант, ответ_верен, подсказка_взята, ответ, решение from Квантландия.ДоступнаяЗадача ORDER BY ученик ASC, вариант ASC);

insert into Kvantland.Score (student, tournament, score) (select ученик, 1, счёт from Квантландия.Ученик ORDER BY ученик ASC);

insert into Kvantland.Score (student, tournament, score) (select ученик, 2, 10 from Квантландия.Ученик ORDER BY ученик ASC);

insert into Kvantland.Previousmail (student, email) (select ученик, почта from Квантландия.Ученик ORDER BY ученик ASC);

update Kvantland.Previousmail set email='vlador3et@gmail.com' where student=3;