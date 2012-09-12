use biae_raw;
CREATE TABLE Followers(
	id_user BIGINT NOT NULL,
	id_follower BIGINT NOT NULL,
	is_ActiveFun tinyint NOT NULL DEFAULT 0, 
	INSERT_TIMESTAMP TIMESTAMP DEFAULT 0,
	PRIMARY KEY (id_user,id_follower)
);
