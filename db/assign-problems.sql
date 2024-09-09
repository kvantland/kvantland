insert into Kvantland.AvailableProblem (student, variant, curr_points)
	select distinct on (student, problem)
		student, variant, points
		from Kvantland.Student, Kvantland.Variant join Kvantland.Problem using (problem) join Kvantland.CurrentTournament using (tournament)
		order by student, problem, random();
