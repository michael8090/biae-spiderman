USE biae_raw;

-- Get count at {status, day} level.
CREATE TEMPORARY TABLE biae._sc0
SELECT
	sc.id_status AS status_id,
	DATE(sc.insert_timestamp) AS create_date,
	sc.reposts_count AS repost_count,
	sc.comments_count AS comment_count
FROM status_counter sc
WHERE sc.insert_timestamp IN
	(
		SELECT
			MAX(insert_timestamp)
		FROM status_counter
		GROUP BY DATE(insert_timestamp)
	);

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


INSERT INTO biae.fact_enterprise_comment_count (enterprise_id, post_id, comment_date, comment_count, comment_count_today)
SELECT
	enterprise_id,
  status_id AS post_id,
	create_date AS comment_date,
	comment_count,
  comment_count_today
FROM biae._sc2;


INSERT INTO biae.fact_enterprise_repost_count (enterprise_id, post_id, repost_date, repost_count, repost_count_today)
SELECT
	enterprise_id,
  status_id AS post_id,
	create_date AS repost_date,
	repost_count,
	repost_count_today
FROM biae._sc2;

DROP TABLE biae._sc0;
DROP TABLE biae._sc0_ld;
DROP TABLE biae._sc1;
DROP TABLE biae._sc2;




INSERT INTO biae.fact_enterprise_fans
SELECT
	e.idUser AS enterprise_id
	DATE(uc.insert_timestamp) AS day_date
	uc.followers_count AS fans_count
	uc.statuses_count AS posts_count

FROM EUser e
	JOIN UserCounters uc ON uc.idUser = e.idUser
WHERE uc.insert_timestamp IN
	(
		SELECT
			MAX(insert_timestamp)
		FROM UserCounters
		GROUP BY DATE(insert_timestamp)
	);

	
--- lu_city


--- lu_province

	
--- lu_comment
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

--- lu_day: no

--- ????? lu_enterprise optional
INSERT INTO biae.lu_enterprise
SELECT
	e.idUser AS enterprise_id,
	e.screen_name AS enterprise_desc
FROM EUser e;


--- ????? lu_event criteria?
INSERT INTO biae.lu_event
SELECT
	s.id_user AS event_id,
	s.`text` AS event_desc,
	DATE(s.create_time) AS day_date,
	s.id_status AS post_id,
	s.id_user AS enterprise_id
FROM status s
WHERE ?;


--- lu_gender: no

--- lu_interest: no


--- lu_month: no

--- lu_post
INSERT INTO biae.lu_post
SELECT
	`id_status` AS post_id,
	`text` AS post_desc,
	DATE(create_time) AS day_date,
	id_user AS enterprise_id
FROM status;

--- lu_repost
INSERT INTO biae.lu_repost
SELECT
	r.repost_id,
	r.`text` AS repost_desc,
	DATE(r.created_time) AS day_date,
	r.retweeted_status_id AS post_id,
	r.user_id,
	s.id_user AS enterprise_id
FROM repost r JOIN status s ON s.id_status = r.retweeted_status_id;


--- lu_user
INSERT INTO biae.lu_user
SELECT
	fo.id_follower AS user_id,
	u.screen_name AS user_name,
	u.gender AS gender_id,
	10000 * u.province + u.city AS city_id,
	u.followers_count AS fans_count,
	u.verified AS has_v
FROM followers fo JOIN euser e ON e.idUser = fo.id_user
	JOIN WeiboUser u ON u.idUser = fo.id_follower;




--- lu_week: no

--- lu_year: no



--- rel_fan




--- lu_qualified_user
--- SELECT 



--- rel_qualified_fan
SELECT
FROM 


--- rel_user_interest





