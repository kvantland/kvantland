import psycopg
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)

def resetProblemsForUsers(users_list, problems_list, db):
	warnings = []
	try:
		with psycopg.connect(db) as con:
			with con.transaction():
				with con.cursor() as cur:
					for user_mail in users_list:
						for problem in problems_list:
							cur.execute("select student from Kvantland.Student where email=%s", (user_mail,))
							students = list(cur.fetchall())
							if (len(students) > 1):
								warnings.append(f"Больше одного пользователя с почтой {user_mail}")
							for (student, ) in students:
									cur.execute("""select variant from 
												Kvantland.Variant join Kvantland.Problem using (problem) join Kvantland.AvailableProblem using (variant)
												where name=%s and student=%s""", (problem, student,))
									variants = list(cur.fetchall())
									for (variant, ) in variants:
										yield f"Executing query: update Kvantland.AvailableProblem set curr=NULL, answer=NULL, solution=NULL, answer_given=DEFAULT, answer_true=NULL where student={student} and variant={variant} \n"
										cur.execute("""
										update Kvantland.AvailableProblem set curr=NULL, answer=NULL, solution=NULL, answer_given=DEFAULT, answer_true=NULL where
										student=%s and
										variant=%s""", (student, variant))
		if warnings:
			warnings = list(set(warnings))
			yield "DB succesfully updated" + " \nusers : " + ", ".join(users_list) + " \nproblems : " + ", ".join(problems_list) + "\n\nWarnings :\n" + "\n".join(warnings)
		else:
			yield "DB succesfully updated" + " \nusers : " + ", ".join(users_list) + " \nproblems : " + ", ".join(problems_list)
	except Exception:
		ex_type, ex_value, ex_traceback = sys.exc_info()
		yield "Error : " + str(ex_value)
