use biae;
CREATE TABLE Status(
	id_status BIGINT NOT NULL,
	create_time varchar(512) NULL DEFAULT NULL,
	text varchar(512) NULL DEFAULT NULL,
	source varchar(512) NULL DEFAULT NULL,
	is_favorited tinyint NULL DEFAULT 0,
	is_truncated tinyint NULL DEFAULT 0,
	in_reply_to_status_id BIGINT DEFAULT NULL,
	in_reply_to_user_id BIGINT DEFAULT NULL,
	in_reply_to_screen_name varchar(512) NULL DEFAULT NULL,
	mid BIGINT NOT NULL,
	reposts_count INT NOT NULL,
	comments_count INT NOT NULL,
	id_user BIGINT NOT NULL,

	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (id_status)
);

CREATE TABLE Status_Counter(
	id_status BIGINT NOT NULL,
	reposts_count INT NOT NULL,
	comments_count INT NOT NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	
	PRIMARY KEY (id_status,INSERT_TIMESTAMP)
);
