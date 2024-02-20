insert into Kvantland.AvailableProblem (student, variant)
	select distinct on (student, problem)
		student, variant
		from Kvantland.Student, Kvantland.Variant join Kvantland.Problem using (problem) where tournament = 2
		order by student, problem, random();
