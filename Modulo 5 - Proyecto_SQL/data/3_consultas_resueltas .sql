-- 2. Muestra los nombres de todas las películas con una clasificación por edades de ‘R’.
select "title" 
from "film" 
where rating = 'R';

--3. Encuentra los nombres de los actores que tengan un “actor_id” entre 30 y 40.
select concat("first_name", ' ', "last_name") as nombre_completos
from "actor" 
where "actor_id" BETWEEN 30 AND 40;

--4. Obtén las películas cuyo idioma coincide con el idioma original.
select "title" 
from "film" 

--5. Ordena las películas por duración de forma ascendente.
select "title", "length" 
from "film"
order by length asc;

-- 6. Encuentra el nombre y apellido de los actores que tengan ‘Allen’ en su apellido.
select  concat("first_name",' ', "last_name")
from actor
where "last_name" ILIKE '%ALLEN%';

--7. Encuentra la cantidad total de películas en cada clasificación de la tabla “film” y muestra la clasificación junto con el recuento.
select "rating", count("film_id") as total_peliculas
from film
group by "rating";

-- 8. Encuentra el título de todas las películas que son ‘PG-13’ o tienen una duración mayor a 3 horas en la tabla film.
select "title", "rating" , "length" 
from "film" 
where "rating" = 'PG-13' or "length" > 180;

--9. Encuentra la variabilidad de lo que costaría reemplazar las películas.
select  STDDEV("replacement_cost") as desviacion_estandar_reemplazo_fils
from film;

--10. Encuentra la mayor y menor duración de una película de nuestra BBDD.
select  
    MAX("length") as mayor_duracion,
    MIN("length") as menor_duracion
from film;

--11. Encuentra lo que costó el antepenúltimo alquiler ordenado por día.
select "payment_id", "amount", "payment_date"   
from "payment"
order by "payment_date", "payment_id" desc
limit 1
offset 2;

-- 12. Encuentra el título de las películas en la tabla “film” que no sean ni ‘NC-17’ ni ‘G’ en cuanto a su clasificación.
select "title",  "rating"
from "film"
where rating not in ('NC-17', 'G');

--13. Encuentra el promedio de duración de las películas para cada clasificación de la tabla film y muestra la clasificación junto con el
--promedio de duración.
select 
    "rating" as clasificacion,
    AVG("length") as promedio_duracion
from "film"
group by "rating";

-- 14. Encuentra el título de todas las películas que tengan una duración mayor a 180 minutos.
select "title", "length" 
from "film"
where length > 180;

-- 15. ¿Cuánto dinero ha generado en total la empresa?
select sum("amount") as facturacion_total
from "payment";

-- 16. Muestra los 10 clientes con mayor valor de id.
select 
	concat("first_name",' ', "last_name") as cliente,
	"customer_id"
from "customer"
order by "customer_id" desc
limit 10;

-- 17. Encuentra el nombre y apellido de los actores que aparecen en la película con título ‘Egg Igby’.
select  
    concat(a.first_name,' ', a.last_name) as actor,
    f.title 
from "actor" a
inner join "film_actor" fa ON a.actor_id = fa.actor_id
inner join "film" f ON fa.film_id = f.film_id
where lower(f.title) = lower('Egg Igby');

--18. Selecciona todos los nombres de las películas únicos.
select distinct "title"
from film;

--19. Encuentra el título de las películas que son comedias y tienen una duración mayor a 180 minutos en la tabla “film”.
select f.title
from  "film" f
inner join "film_category" fc on f.film_id = fc.film_id
inner join "category" c on fc.category_id = c.category_id
where c.name = 'Comedy'and f.length > 180;

-- 20. Encuentra las categorías de películas que tienen un promedio de
-- duración superior a 110 minutos y muestra el nombre de la categoría
-- junto con el promedio de duración.
select 
    c.name AS categoria,
    AVG(f.length) AS promedio_duracion
from "film" f
inner join "film_category" fc on f.film_id = fc.film_id
inner join category c on fc.category_id = c.category_id
group by c.name
having  AVG(f.length) > 110;

--21. ¿Cuál es la media de duración del alquiler de las películas?
select 
    avg("return_date" - "rental_date") AS media_duracion_alquiler
from "rental";

--22. Crea una columna con el nombre y apellidos de todos los actores y actrices.
select 
	concat("first_name",' ', "last_name") as actor_actric
from "actor"

-- 23. Números de alquiler por día, ordenados por cantidad de alquiler de forma descendente.
select 
	count ("rental_id") as cantidad_alquires_por_dia,
	to_char("rental_date", 'YYYY-MM-DD') as fecha_alquiler
from "rental"
group by fecha_alquiler
order by cantidad_alquires_por_dia desc;

-- Encuentra las películas con una duración superior al promedio.
select title, length  
from film
where length > (select avg(length) from film)
order by length asc;

--Averigua el número de alquileres registrados por mes.
select 
	count ("rental_id") as cantidad_alquires_por_mes,
	to_char("rental_date", 'YYYY-MM') as fecha_alquiler
from "rental"
group by fecha_alquiler
order by cantidad_alquires_por_mes desc;

--26. Encuentra el promedio, la desviación estándar y varianza del total pagado.
select 
	avg("amount") as promedio,
	var_samp("amount") as varianza_muestral,
	stddev_samp("amount") as desviacion_muestral
from payment;

--27. ¿Qué películas se alquilan por encima del precio medio?
select 
    "title", "rental_rate"
from "film"
where "rental_rate" > (
    select avg("rental_rate")
    from "film"
)
order by "rental_rate" desc;

--28. Muestra el id de los actores que hayan participado en más de 40 películas.
select 
    "actor_id",
    count("film_id") as total_peliculas
from "film_actor"
group by "actor_id"
having count("film_id") > 40
order by total_peliculas desc;

--29. Obtener todas las películas y, si están disponibles en el inventario,
--mostrar la cantidad disponible.
select 
    f.film_id,
    f.title,
    count(i.inventory_id) AS cantidad_disponible
from "film" f
left join "inventory" i on f.film_id = i.film_id
group by  f.film_id, f.title
order by cantidad_disponible desc;

--30. Obtener los actores y el número de películas en las que ha actuado.
select 
    a.actor_id,
    concat(a.first_name, ' ', a.last_name) as actor,
    count(fa.film_id) as cantidad_peliculas
from "actor" a
inner join "film_actor" fa ON a.actor_id = fa.actor_id
group by a.actor_id, a.first_name, a.last_name
order by cantidad_peliculas desc;

--31. Obtener todas las películas y mostrar los actores que han actuado en
--ellas, incluso si algunas películas no tienen actores asociados.
select 
    f.film_id,
    f.title,
    a.actor_id,
    concat(a.first_name, ' ', a.last_name) as actor
from "film" f
left join "film_actor" fa ON f.film_id = fa.film_id
left join "actor" a ON fa.actor_id = a.actor_id
Order by f.title, a.last_name;

-- 32.Obtener todos los actores y mostrar las películas en las que han
-- actuado, incluso si algunos actores no han actuado en ninguna película.
select 
    a.actor_id,
    concat(a.first_name, ' ', a.last_name) as actor,
    f.film_id,
    f.title
from actor a
left join "film_actor" fa ON a.actor_id = fa.actor_id
left join "film" f ON fa.film_id = f.film_id
order by a.last_name, a.first_name, f.title;

--33. Obtener todas las películas que tenemos y todos los registros de alquiler.
select 
    f.film_id,
    f.title,
    r.rental_date
from "film" f
left join "inventory" i ON f.film_id = i.film_id
left join "rental" r ON i.inventory_id = r.inventory_id
order by f.title, r.rental_date;

--34. Encuentra los 5 clientes que más dinero se hayan gastado con nosotros.
select 
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as cliente,
    sum(p.amount) as total_gastado
from customer c
inner join "payment" p ON c.customer_id = p.customer_id
group by c.customer_id
order by total_gastado desc
limit 5;

-- 35. Selecciona todos los actores cuyo primer nombre es 'Johnny'.
select 
	"actor_id",
	concat("first_name", ' ', "last_name") as actor
from "actor"
where "first_name" ilike 'Johnny';

--36. Renombra la columna “first_name” como Nombre y “last_name” como Apellido.
select 
	"first_name" as Nombre,
	"last_name" as Apellido 
from "actor";

--37. Encuentra el ID del actor más bajo y más alto en la tabla actor.
select 
	min ("actor_id") as idActorMasBajo,
	max ("actor_id") as idActorMasAlto
from "actor";

--38. Cuenta cuántos actores hay en la tabla “actor”.
select count("actor_id") as numeroActores
from "actor";

--39. Selecciona todos los actores y ordénalos por apellido en orden ascendente.
select 
	"first_name" as Nombre,
	"last_name" as Apellido
from actor
order by "last_name" asc;

--40. Selecciona las primeras 5 películas de la tabla “film”.
select 
	"film_id",
	"title" 
from "film" 
order by "film_id"
limit 5;

-- 41. Agrupa los actores por su nombre y cuenta cuántos actores tienen el mismo nombre. ¿Cuál es el nombre más repetido?
select 
	"first_name" as Nombre,
	count("first_name") as totalActoresElMismoNombre
from "actor"
group by "first_name"            
order by totalActoresElMismoNombre desc
limit 1;

--42. Encuentra todos los alquileres y los nombres de los clientes que los realizaron.
select 
    r.rental_id,
    r.rental_date,
    concat(c.first_name, ' ', c.last_name) as cliente
from  "rental" r
inner join "customer" c ON r.customer_id = c.customer_id
order by r.rental_date;

--43. Muestra todos los clientes y sus alquileres si existen, incluyendo aquellos que no tienen alquileres.
select 
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as cliente,
    r.rental_date
from "customer" c
left join "rental" r ON c.customer_id = r.customer_id
order by c.customer_id, r.rental_date;

--44. Realiza un CROSS JOIN entre las tablas film y category. ¿Aporta valor
-- esta consulta? ¿Por qué? Deja después de la consulta la contestación.
select 
    f.film_id,
    f.title,
    c.category_id,
    c.name AS categoria
from "film" f
cross join "category" c
order by f.film_id, c.category_id;

--Mi entendimiento es que no aporta valor, ya que un CROSS JOIN muestra el producto cartesiano entre las tablas, 
--combinando todas las películas con todas las categorías sin considerar la relación real entre ellas. Esto puede confundir y 
--no proporcionar información útil. Para obtener datos relevantes sobre qué película pertenece a qué categoría, 
--sería más adecuado usar un INNER JOIN a través de la tabla film_category.

--45. Encuentra los actores que han participado en películas de la categoría 'Action'.
select
    a.actor_id,
    concat(a.first_name, ' ', a.last_name) as actor
from "actor" a
inner join "film_actor" fa on a.actor_id = fa.actor_id
inner join "film_category" fc on fa.film_id = fc.film_id
inner join "category" c on fc.category_id = c.category_id
where c.name = 'Action'
group by a.actor_id, a.first_name, a.last_name
order by a.last_name, a.first_name;

-- 46. Encuentra todos los actores que no han participado en películas.
select a.actor_id,
       concat(a.first_name, ' ', a.last_name) as actor
from "actor" a
left join film_actor fa on a.actor_id = fa.actor_id
where fa.actor_id IS NULL
order by actor;

--47. Selecciona el nombre de los actores y la cantidad de películas en las que han participado.
select 
    concat(a.first_name, ' ', a.last_name) as actor,
    count(fa.film_id) as cantidad_peliculas
from actor a
left join film_actor fa on a.actor_id = fa.actor_id
group by a.actor_id, a.first_name, a.last_name
order by cantidad_peliculas desc;

--48. Crea una vista llamada “actor_num_peliculas” que muestre los nombres de los actores y el número de películas en las que han participado.
create or replace view actorNumPeliculas as
select 
    concat(a.first_name, ' ', a.last_name) as actor,
    count(fa.film_id) as cantidad_peliculas
from "actor" a
left join film_actor fa on a.actor_id = fa.actor_id
group by a.actor_id, a.first_name, a.last_name
order by cantidad_peliculas desc;

--49. Calcula el número total de alquileres realizados por cada cliente.
select
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as cliente,
    count(r.rental_id) as total_alquileres
from "customer" c
left join "rental" r on c.customer_id = r.customer_id
group by c.customer_id, c.first_name, c.last_name
order by total_alquileres desc;

--50. Calcula la duración total de las películas en la categoría 'Action'.
select 
    sum(f.length) as duracion_total
from "film" f
inner join film_category fc on f.film_id = fc.film_id
inner join category c on fc.category_id = c.category_id
where c.name ILIKE 'Action';

--51. Crea una tabla temporal llamada “cliente_rentas_temporal” para almacenar el total de alquileres por cliente.
create temp table cliente_rentas_temporal as
select 
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as cliente,
    count(r.rental_id) as total_alquileres
from "customer" c
left join "rental" r on c.customer_id = r.customer_id
group by c.customer_id, c.first_name, c.last_name
order by total_alquileres desc;

select * from cliente_rentas_temporal;

--52. Crea una tabla temporal llamada “peliculas_alquiladas” que almacene las películas que han sido alquiladas al menos 10 veces.
create temp table peliculas_alquiladas as
select 
    f.film_id,
    f.title,
    count(r.rental_id) as total_alquileres
from film f
inner join "inventory" i on f.film_id = i.film_id
inner join "rental" r on i.inventory_id = r.inventory_id
group by f.film_id, f.title
having count(r.rental_id) >= 10
order by total_alquileres desc;

select * from peliculas_alquiladas;

--53. Encuentra el título de las películas que han sido alquiladas por el cliente con el nombre ‘Tammy Sanders’ y que aún no se han devuelto. Ordena
--los resultados alfabéticamente por título de película.
select f.title
from "customer" c
inner join "rental" r on c.customer_id = r.customer_id
inner join "inventory" i on r.inventory_id = i.inventory_id
inner join "film" f ON i.film_id = f.film_id
where c.first_name ILIKE 'Tammy'
  and c.last_name ILIKE 'Sanders'
  and r.return_date IS NULL
order by f.title;

--54. Encuentra los nombres de los actores que han actuado en al menos una película que pertenece a la categoría ‘Sci-Fi’. Ordena los resultados
--alfabéticamente por apellido.
select 
    concat(a.first_name, ' ', a.last_name) as actor
from "actor" a
inner join "film_actor" fa on a.actor_id = fa.actor_id
inner join "film_category" fc on fa.film_id = fc.film_id
inner join "category" c on fc.category_id = c.category_id
where c.name ILIKE 'Sci-Fi'
group by a.actor_id, a.first_name, a.last_name
order by a.last_name, a.first_name;

--55. Encuentra el nombre y apellido de los actores que han actuado en películas que se alquilaron después de que la película ‘Spartacus
--Cheaper’ se alquilara por primera vez. Ordena los resultados alfabéticamente por apellido.
with primera_fecha as (
    select MIN(r.rental_date) as fecha_primera
    from "film" f
    inner join "inventory" i on f.film_id = i.film_id
    inner join "rental" r on i.inventory_id = r.inventory_id
    where f.title ILIKE 'Spartacus Cheaper'
)
select a.first_name,
       a.last_name
from "actor" a
inner join "film_actor" fa on a.actor_id = fa.actor_id
inner join "inventory" i on fa.film_id = i.film_id
inner join "rental" r on i.inventory_id = r.inventory_id
where r.rental_date > (select fecha_primera from primera_fecha)
group by a.actor_id, a.first_name, a.last_name
order by a.last_name, a.first_name;

--56. Encuentra el nombre y apellido de los actores que no han actuado en ninguna película de la categoría ‘Music’.
select concat(a.first_name, ' ', a.last_name) as actor
from "actor" a
where not exists (
    select 1
    from "film_actor" fa
    inner join film_category fc on fa.film_id = fc.film_id
    inner join category c on fc.category_id = c.category_id
    where fa.actor_id = a.actor_id
      and c.name ILIKE 'Music'
)
order by a.last_name, a.first_name;

--57. Encuentra el título de todas las películas que fueron alquiladas por más de 8 días.
select f.title
from "film" f
inner join "inventory" i on f.film_id = i.film_id
inner join "rental" r on i.inventory_id = r.inventory_id
where extract (day from (r.return_date - r.rental_date)) > 8
group by f.title
order by f.title;

--58. Encuentra el título de todas las películas que son de la misma categoría que ‘Animation’.
select f.title
from "film" f
inner join "film_category" fc on f.film_id = fc.film_id
inner join "category" c on fc.category_id = c.category_id
where c.name ILIKE 'Animation'
order by f.title;

--*59. Encuentra los nombres de las películas que tienen la misma duración que la película con el título ‘Dancing Fever’. Ordena los resultados
--alfabéticamente por título de película.
select f.title
from "film" f
where f.length = (
    select f2.length
    from film f2
    where f2.title ILIKE 'Dancing Fever'
)
Order by f.title;

--60. Encuentra los nombres de los clientes que han alquilado al menos 7 películas distintas. Ordena los resultados alfabéticamente por apellido.
select concat(c.first_name, ' ', c.last_name) as cliente
from "customer" c
inner join "rental" r ON c.customer_id = r.customer_id
inner join "inventory" i ON r.inventory_id = i.inventory_id
group by c.customer_id, c.first_name, c.last_name
having count(distinct i.film_id) >= 7
order by c.last_name, c.first_name;

--61. Encuentra la cantidad total de películas alquiladas por categoría y muestra el nombre de la categoría junto con el recuento de alquileres.
select c.name as categoria,
       count(r.rental_id) as total_alquileres
from "category" c
inner join "film_category" fc on c.category_id = fc.category_id
inner join "inventory" i on fc.film_id = i.film_id
inner join "rental" r on i.inventory_id = r.inventory_id
group by c.category_id, c.name
order by total_alquileres desc;

--62. Encuentra el número de películas por categoría estrenadas en 2006.
select c.name as categoria,
       count(f.film_id) as total_peliculas
from "category" c
inner join "film_category" fc on c.category_id = fc.category_id
inner join "film" f on fc.film_id = f.film_id
where f.release_year = 2006
group by c.category_id, c.name
order by total_peliculas desc;

--63. Obtén todas las combinaciones posibles de trabajadores con las tiendas que tenemos.
select s.first_name,
       s.last_name,
       st.store_id
from "staff" s
cross join "store" st
order by s.last_name, st.store_id;

--64. Encuentra la cantidad total de películas alquiladas por cada cliente y muestra el ID del cliente, su nombre y apellido junto con la cantidad de
--películas alquiladas.
select c.customer_id,
       concat(c.first_name, ' ', c.last_name) as cliente,
       count(r.rental_id) as total_alquileres
from "customer" c
left join "rental" r on c.customer_id = r.customer_id
group by c.customer_id, c.first_name, c.last_name
order by total_alquileres desc;