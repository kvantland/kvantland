insert into ДоступнаяЗадача (ученик, вариант)
	select distinct on (ученик, задача)
		ученик, вариант
		from Ученик, Вариант
		order by ученик, задача, random();

-- kate: syntax SQL (PostgreSQL);
