USE biae_raw;



-- lu_post
DELETE FROM lu_post;
INSERT INTO biae.lu_post
SELECT
	`id_status` AS post_id,
	`text` AS post_desc,
	DATE(create_time) AS day_date,
	id_user AS enterprise_id
FROM status;

-- lu_repost
DELETE FROM biae.lu_repost;
INSERT INTO biae.lu_repost
SELECT
	r.repost_id,
	r.`text` AS repost_desc,
	DATE(r.created_time) AS day_date,
	r.retweeted_status_id AS post_id,
	r.user_id,
	s.id_user AS enterprise_id
FROM repost r JOIN status s ON s.id_status = r.retweeted_status_id;


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

-- ????? lu_event criteria?
/*DELETE FROM biae.lu_event;
INSERT INTO biae.lu_event
SELECT
	s.id_user AS event_id,
	s.`text` AS event_desc,
	DATE(s.create_time) AS day_date,
	s.id_status AS post_id,
	s.id_user AS enterprise_id
FROM status s
WHERE ?*/;
