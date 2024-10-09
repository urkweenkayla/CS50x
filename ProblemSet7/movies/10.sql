SELECT name FROM people WHERE id IN (SELECT person_id FROM directors WHERE movie_id IN (SELECT movie_id FROM ratings WHERE rating >= 9.0 AND movie_id IN (SELECT id FROM movies))) ORDER BY name ASC;
