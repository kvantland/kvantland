insert into Kvantland.Score (student, tournament, score) (select student, 3, 10 from Kvantland.Student ORDER BY student ASC);
update Kvantland.Student set score = 10;
insert into Kvantland.Season (tournament, season) values 
(1, 1),
(2, 1),
(3, 1);