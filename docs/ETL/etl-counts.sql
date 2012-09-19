USE biae_raw;

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
