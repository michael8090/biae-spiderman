CREATE TABLE EUser (
	idUser BIGINT NOT NULL,
	screen_name varchar(512) NULL,
	primary key(idUser)
);

INSERT INTO `EUser` (`idUser`, `screen_name`) VALUES (2202387347, "小米手机"), (2798510462, "360用户特供机"), (2202847500, "HTC_China"), (1645915085, "摩托罗拉"), (1660811367, "诺基亚");

CREATE TABLE WeiboUser (
	idUser BIGINT NOT NULL,
	screen_name varchar(512) NULL,
	name varchar(512) NULL,
	province integer NULL,
	city integer NULL,
	location varchar(512) NULL,
	description varchar(512) NULL,
	url varchar(512) NULL,
	profile_image varchar(512) NULL,
	domain varchar(512) NULL,
	gender Tinyint NULL, -- M:1, F:2, Null:0
	followers_count BIGINT NULL,                    -- added
	friends_count BIGINT NULL,                      -- added
	statuses_count BIGINT NULL,                     -- added
	favourites_count BIGINT NULL,                   -- added
	created_at TIMESTAMP NULL,                      -- added
	avatar_large varchar(512) NULL,
	verified Boolean DEFAULT False,
	verified_reason Varchar(1024) DEFAULT NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	primary key(idUser)
)COLLATE='utf8_general_ci'
ENGINE=InnoDB;

CREATE TABLE UserCounters(
	idUser BIGINT NOT NULL,
	followers_count BIGINT NOT NULL DEFAULT 0,
	friends_count BIGINT NOT NULL DEFAULT 0,
	statuses_count BIGINT NOT NULL DEFAULT 0,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(idUser, INSERT_TIMESTAMP)
);

CREATE TABLE status_comment(
	comment_id BIGINT NOT NULL,
	commented_status_id BIGINT NOT NULL,
	user_id BIGINT NOT NULL,
	created_time TIMESTAMP DEFAULT 0,
	`text` varchar(4096) NOT NULL,
	source varchar(512) NOT NULL,
	mid BIGINT NOT NULL,
	replied_to_comment_id BIGINT NOT NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP
		DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (comment_id), 
	INDEX (commented_status_id)
);

CREATE TABLE repost(
	repost_id BIGINT NOT NULL,
	retweeted_status_id BIGINT NOT NULL,
	user_id BIGINT NOT NULL,
	created_time TIMESTAMP DEFAULT 0,
	text VARCHAR(4096) NOT NULL,
	source VARCHAR(512) NOT NULL,
	favorited TINYINT NOT NULL,	
	truncated TINYINT NOT NULL,
	in_reply_to_status_id BIGINT NOT NULL DEFAULT 0,
	in_reply_to_screen_name VARCHAR(512) NOT NULL DEFAULT '',
	mid BIGINT NOT NULL,
	reposts_count INT NOT NULL, 
	comments_count INT NOT NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP
		DEFAULT CURRENT_TIMESTAMP
		ON UPDATE CURRENT_TIMESTAMP,

	PRIMARY KEY (repost_id),
	INDEX (retweeted_status_id)
);

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

CREATE TABLE Followers(
	id_user BIGINT NOT NULL,
	id_follower BIGINT NOT NULL,
	is_ActiveFun tinyint NOT NULL DEFAULT 0, 
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	PRIMARY KEY (id_user,id_follower)
);

CREATE TABLE Status(
	id_status BIGINT NOT NULL,
	create_time TIMESTAMP DEFAULT 0,
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


CREATE TABLE `Public_Token_Pool` (
	`UserID` BIGINT(20) NOT NULL,
	`Access_Token` TEXT NULL,
	`TokenStatus` INT(11) NULL DEFAULT '1',
	`TeamID` INT(11) NULL DEFAULT NULL,
	`INSERT_TIMESTAMP` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
	`LAST_UPDATE_TIMESTAMP` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`UserID`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;

INSERT INTO `Public_Token_Pool` (`UserID`, `Access_Token`, `TokenStatus`, `TeamID`, `INSERT_TIMESTAMP`, `LAST_UPDATE_TIMESTAMP`) VALUES (1971408223, '2.00p1p6JCdL65TC26afccfc45UURz8C', 1, NULL, '0000-00-00 00:00:00', '2012-08-30 07:21:36');	