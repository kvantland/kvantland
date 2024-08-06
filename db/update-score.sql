insert into Kvantland.Score (student, tournament)
select student.*,
(select tournament from Kvantland.CurrentTournament limit 1) as tournament
from (select student from Kvantland.Student ) as student;

update Kvantland.Student set score = 10;