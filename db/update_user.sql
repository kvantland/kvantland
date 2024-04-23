update Kvantland.Student set score=score + 3 where email = 'kitarchik@gmail.com'
update Kvantland.Score set score=score + 3 where student = 'kitarchik@gmail.com' and tournament = 3

update Kvantland.AvailableProblem set answer_true = true 
where variant in (select variant from Kvantland.Variant 
			   where problem=(select problem from Kvantland.Problem 
							  where name='Гномы на клетках')) 
and student=(select student from Kvantland.Student where email = 'kitarchik@gmail.com')