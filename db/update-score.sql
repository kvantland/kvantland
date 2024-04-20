insert into Kvantland.Score (student, tournament, score) (select student, 3, 10 from Kvantland.Student ORDER BY student ASC);
update Kvantland.Student set score = 10;