USE biae_raw;


CREATE TEMPORARY TABLE biae._fact_enterprise_status_counters
SELECT
	e.idUser AS enterprise_id
	DATE(sc.insert_timestamp) AS create_date
	SUM(sc.reposts_count) AS repost_count
	SUM(sc.comments_count) AS comment_count
FROM EUser e
	JOIN status s ON e.idUser = sc.id_user
	JOIN status_counter sc ON sc.id_status = s.id_status
WHERE SC.insert_timestamp IN
	(
		SELECT
			MAX(insert_timestamp)
		FROM status_counter
		GROUP BY DATE(insert_timestamp)
	)
GROUP BY e.idUser, DATE(sc.insert_timestamp);


INSERT INTO biae.fact_enterprise_comment_count
SELECT
	enterprise_id,
	created_date AS comment_date
	comment_count
FROM biae._fact_enterprise_status_counters;


INSERT INTO biae.fact_enterprise_repost_count
SELECT
	enterprise_id,
	created_date AS repost_date
	repost_count
FROM biae._fact_enterprise_status_counters;

DROP TABLE biae._fact_enterprise_status_counters;




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
	sc.comment_id AS comment_id,
	sc.`text` AS comment_desc,
	DATE(sc.created_time) AS day_date,
	sc.commented_status_id AS post_id,
	sc.user_id AS user_id,
	s.idUser AS enterprise_id
FROM status_comment sc
	JOIN status s ON s.status_id = sc.status_id;

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
	? AS event_id,
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


--- lu_repost

--- lu_user


--- lu_week: no

--- lu_year: no



--- rel_fan



--- rel_user_interest


