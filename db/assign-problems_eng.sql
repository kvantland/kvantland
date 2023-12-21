insert into Kvantland.AvailableProblem (student, variant)
	select distinct on (student, problem)
		student, variant
		from Kvantland.Student, Kvantland.Variant
		order by student, problem, random();
