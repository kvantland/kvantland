insert into AvailableProblem (user, variant)
	select distinct on (user, problem)
		user, variant
		from User, Variant
		order by user, problem, random();
