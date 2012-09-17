USE biae_raw;
START TRANSACTION;

-- Get count at {status, day} level.
CREATE TEMPORARY TABLE biae._sc0
SELECT
	sc.id_status AS status_id,
	DATE(sc.insert_timestamp) AS create_date,
	sc.reposts_count AS repost_count,
	sc.comments_count AS comment_count
FROM status_counter sc
  JOIN (
		SELECT
			id_status,
      MAX(insert_timestamp) AS insert_timestamp
		FROM status_counter
		GROUP BY id_status, DATE(insert_timestamp)
	) sc1 ON sc.id_status = sc1.id_status AND sc.insert_timestamp = sc1.insert_timestamp;

-- Get last day's count (still {status, day} level).
CREATE TEMPORARY TABLE biae._sc0_ld
SELECT
	status_id,
	ADDDATE(create_date, 1) AS create_date,
	repost_count AS ld_repost_count,
	comment_count AS ld_comment_count
FROM biae._sc0;



-- Get count and daily count (still {status, day} level).
CREATE TEMPORARY TABLE biae._sc1
SELECT
	sc0.status_id,
	sc0.create_date,
	sc0.repost_count,
	sc0.comment_count,
	sc0.repost_count - sc0_ld.ld_repost_count AS repost_count_today,
	sc0.comment_count - sc0_ld.ld_comment_count AS comment_count_today
FROM biae._sc0 AS sc0
	JOIN biae._sc0_ld AS sc0_ld ON sc0.create_date = sc0_ld.create_date
;


-- Aggregate to {enterprise, day} level.
CREATE TEMPORARY TABLE biae._sc2
SELECT
	e.idUser AS enterprise_id,
  sc.status_id,
	sc.create_date,
  repost_count,
	comment_count,
	repost_count_today,
	comment_count_today
FROM EUser e
	JOIN status s ON e.idUser = s.id_user
	JOIN biae._sc1 sc ON sc.status_id = s.id_status
GROUP BY sc.status_id, sc.create_date;


DELETE FROM biae.fact_enterprise_comment_count;
INSERT INTO biae.fact_enterprise_comment_count
	(enterprise_id, post_id, comment_date, comment_count, comment_count_today)
SELECT
	enterprise_id, status_id, create_date, comment_count, comment_count_today
FROM biae._sc2;


INSERT INTO biae.fact_enterprise_repost_count
	(enterprise_id, post_id, repost_date, repost_count, repost_count_today)
SELECT
	enterprise_id, status_id, create_date, repost_count, repost_count_today
FROM biae._sc2;

DROP TABLE biae._sc0;
DROP TABLE biae._sc0_ld;
DROP TABLE biae._sc1;
DROP TABLE biae._sc2;



DELETE FROM biae.fact_enterprise_fans;
INSERT INTO biae.fact_enterprise_fans (
	enterprise_id,
	day_date,
	fans_count,
	posts_count)
SELECT
	e.idUser,
	DATE(uc.insert_timestamp),
	uc.followers_count,
	uc.statuses_count
FROM EUser e
  JOIN (
		SELECT
			idUser,
      MAX(insert_timestamp) AS insert_timestamp
		FROM UserCounters
		GROUP BY idUser, DATE(insert_timestamp)
	) uc1 ON e.idUser = uc1.idUser
	JOIN UserCounters uc ON e.idUser = uc1.idUser AND UC.insert_timestamp = uc1.insert_timestamp;


-- lu_city


-- lu_province


-- lu_comment
DELETE FROM biae.lu_comment;
INSERT INTO biae.lu_comment
SELECT
	c.comment_id AS comment_id,
	c.`text` AS comment_desc,
	DATE(c.created_time) AS day_date,
	c.commented_status_id AS post_id,
	c.user_id AS user_id,
	s.id_user AS enterprise_id
FROM status_comment c
	JOIN status s ON s.id_status = c.commented_status_id;

-- lu_day: no

-- ????? lu_enterprise optional
DELETE FROM biae.lu_enterprise;
INSERT INTO biae.lu_enterprise
SELECT
	e.idUser AS enterprise_id,
	e.screen_name AS enterprise_desc
FROM EUser e;


-- ????? lu_event criteria?
DELETE FROM biae.lu_event;
INSERT INTO biae.lu_event
SELECT
	s.id_user AS event_id,
	s.`text` AS event_desc,
	DATE(s.create_time) AS day_date,
	s.id_status AS post_id,
	s.id_user AS enterprise_id
FROM status s
WHERE ?;


-- lu_gender: no

-- lu_interest: no


-- lu_month: no

-- lu_post
INSERT INTO biae.lu_post
SELECT
	`id_status` AS post_id,
	`text` AS post_desc,
	DATE(create_time) AS day_date,
	id_user AS enterprise_id
FROM status;

-- lu_repost
INSERT INTO biae.lu_repost
SELECT
	r.repost_id,
	r.`text` AS repost_desc,
	DATE(r.created_time) AS day_date,
	r.retweeted_status_id AS post_id,
	r.user_id,
	s.id_user AS enterprise_id
FROM repost r JOIN status s ON s.id_status = r.retweeted_status_id;


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




-- lu_week: no

-- lu_year: no


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
DELETE FROM rel_fan;
INSERT INTO rel_fan (enterprise_id, qualified_user_id)
SELECT
	fo.id_follower,
	u.screen_name,
	u.gender,
	10000 * u.province + u.city,
	u.followers_count,
	u.verified
FROM EUser e
	JOIN followers fo ON fo.id_user = e.idUser
WHERE fo.is_activefun = 1;


-- lu_qualified_user
INSERT INTO lu_qualified_user (qualified_user_id, user_name, gender_id, city_id, fans_count, has_v)
SELECT
	u.idUser,
	u.screen_name,
	u.gender,
	10000 * u.province + u.city,
	u.followers_count,
	u.verified
FROM WeiboUser u
WHERE u.idUser IN (SELECT DISTINCT qualified_user_id FROM rel_fan);




-- rel_user_interest
CREATE TABLE Tags (
	idUser BIGINT NOT NULL,
	tagId BIGINT NOT NULL,
	tag varchar(512) NOT NULL,
	weight integer NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (idUser, tagId)
);


CREATE TABLE biae._user_interest
SELECT
	idUser AS user_id,
	interest_id,
	COUNT(*) AS times
FROM tags t
	JOIN keyword_interest i ON t.tag LIKE CONCAT('%', t.keyword, '%');


INSERT INTO biae.rel_user_interest (user_id, interest_id)
SELECT
	ui1.user_id,
	ui1.interest_id
FROM biae._user_interest ui1
	LEFT OUTER JOIN biae.user_interest ui2
		ON ui1.user_id = ui2.user_id AND ui1.times < ui2.times
GROUP BY ui1.user_id, ui1.interest_id
HAVING COUNT(*) < 3
ORDER BY ui1.user_id, ui1.times DESC;

DROP TABLE biae._user_interest;

COMMIT;
