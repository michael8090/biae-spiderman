	
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
	avatar_large varchar(512) NULL,
	verified Boolean DEFAULT False,
	verified_reason Varchar(1024) DEFAULT NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	primary key(idUser)
);

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


CREATE TABLE Status(
	idStatus BIGINT NOT NULL,
	mid BIGINT NOT NULL,
	id_creatorUID BIGINT NULL DEFAULT  NULL,
	id_crawlerUID BIGINT NOT NULL,
	source varchar(512) NULL DEFAULT NULL,
	text varchar(512) NULL DEFAULT NULL,
	is_truncated tinyint NULL DEFAULT 0,
	is_favorited tinyint NULL DEFAULT 0,
	created_time TIMESTAMP DEFAULT 0,
	in_reply_to_screen_name	varchar(512) NULL DEFAULT NULL,
	in_reply_to_status_id BIGINT DEFAULT NULL,
	in_reply_to_user_id	BIGINT DEFAULT NULL,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (idStatus)
);

CREATE TABLE StatusComment(
	idComment BIGINT NOT NULL,
	mid BIGINT NOT NULL,
	idCommenting_User BIGINT NOT NULL,
	idCommented_Status BIGINT NOT NULL,
	message varchar(4096) NOT NULL,
	source varchar(512) NOT NULL,
	idReply_To_Comment BIGINT DEFAULT NULL,  -- could be null, depending on whether the comment is a reply to some previous comment
	created_time TIMESTAMP DEFAULT 0,
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (idComment, idCommented_Status)
);


CREATE TABLE Repost(
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




-- the relationship table presents the relationship between user pairs, 
-- for <A, B>, if A follows B, that makes A B's follower and B A's friend, we then should insert a pair <B, A>
CREATE TABLE Relationships (
     idFriend BIGINT NOT NULL,
     idFollower BIGINT NOT NULL,
     relationship_status TINYINT NOT NULL DEFAULT 1,
     INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
     LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
     PRIMARY KEY (idFriend, idFollower, INSERT_TIMESTAMP),
     Index (idFriend),
     Index (idFollower)
);
 
CREATE TABLE StatusCounts(
	idStatus BIGINT NOT NULL,
	id_crawlerUID BIGINT NULL DEFAULT  NULL,
	created_time datetime NULL DEFAULT  NULL,
	comments_count int NULL DEFAULT NULL,
	reposts_count int NULL DEFAULT NULL,
	
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	LAST_UPDATE_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,
	Primary key (idStatus),
	KEY IDX_PostCounts_1(id_crawlerUID)
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
