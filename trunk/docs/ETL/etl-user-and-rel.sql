USE biae_raw;


-- ????? lu_enterprise optional
DELETE FROM biae.lu_enterprise;
INSERT INTO biae.lu_enterprise
SELECT
	e.idUser AS enterprise_id,
	e.screen_name AS enterprise_desc
FROM EUser e;



-- lu_user
DELETE FROM biae.lu_user;
INSERT INTO biae.lu_user (user_id, user_name, gender_id, city_id, fans_count, has_v)
SELECT DISTINCT
	u.idUser,
	u.screen_name,
	u.gender,
	10000 * u.province + u.city,
	u.followers_count,
	u.verified
FROM followers fo JOIN euser e ON e.idUser = fo.id_user
	JOIN WeiboUser u ON u.idUser = fo.id_follower;

-- rel_fan
DELETE FROM biae.rel_fan;
INSERT INTO biae.rel_fan (enterprise_id, user_id, fan_date, DUMMYC)
SELECT
	fo.id_user,
	fo.id_follower,
	DATE(fo.insert_timestamp),
	0
FROM EUser e
	JOIN followers fo ON fo.id_user = e.idUser
WHERE INSERT_TIMESTAMP > 0;





-- rel_qualified_fan
DELETE FROM biae.rel_qualified_fan;
INSERT INTO biae.rel_qualified_fan (enterprise_id, qualified_user_id)
SELECT
  e.idUser,
  fo.id_follower
FROM EUser e
	JOIN followers fo ON fo.id_user = e.idUser
WHERE fo.is_activefun = 1;

create table __uuu (
foid bigint not null,
primary key (foid)
);

insert into __uuu
select distinct id_follower
from followers
where is_activefun = 1;

-- lu_qualified_user
DELETE FROM biae.lu_qualified_user;
INSERT INTO biae.lu_qualified_user (qualified_user_id, user_name, gender_id, city_id, fans_count, has_v)
SELECT
	u.idUser,
	u.screen_name,
	u.gender,
	10000 * u.province + u.city,
	u.followers_count,
	u.verified
FROM
 WeiboUser u 
WHERE u.idUser IN (SELECT foid FROM __uuu);

DROP table __uuu;
