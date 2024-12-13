insert into Kvantland.AvailableProblem (student, variant)
	select distinct on (student, problem, classes)
		student, variant
		from Kvantland.Student, Kvantland.Variant join Kvantland.Problem using (problem) join Kvantland.CurrentTournament using (tournament)
		order by student, problem, classes, random();
