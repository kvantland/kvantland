insert into AvailableProblem (student, variant)
	select distinct on (student, problem)
		student, variant
		from Student, Variant
		order by student, problem, random();
