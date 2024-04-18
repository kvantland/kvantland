insert into Kvantland.AvailableProblem (student, variant)
	select distinct on (student, problem)
		student, variant
		from Kvantland.Student, Kvantland.Variant join Kvantland.Problem using (problem) where tournament = 3
		order by student, problem, random();
