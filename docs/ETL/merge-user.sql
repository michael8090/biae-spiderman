show create table biae_raw.weibouser;

drop table _weibouser__01;

CREATE TABLE `_weibouser__02` (
  `idUser` bigint(20) NOT NULL,
  `screen_name` varchar(512) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `province` int(11) DEFAULT NULL,
  `city` int(11) DEFAULT NULL,
  `location` varchar(512) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `profile_image` varchar(512) DEFAULT NULL,
  `domain` varchar(512) DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  `followers_count` bigint(20) DEFAULT NULL,
  `friends_count` bigint(20) DEFAULT NULL,
  `statuses_count` bigint(20) DEFAULT NULL,
  `favourites_count` bigint(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `avatar_large` varchar(512) DEFAULT NULL,
  `verified` tinyint(1) DEFAULT '0',
  `verified_reason` varchar(1024) DEFAULT NULL,
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `LAST_UPDATE_TIMESTAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`idUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



insert into _weibouser0
select null, u.*
from biae_raw.weibouser u;

insert into _weibouser0
select null, u.*
from biae_raw1.weibouser u;

insert into _weibouser0
select null, u.*
from biae_raw__dump3.weibouser u;

insert into _weibouser0
select null, u.*
from biae_raw__dump4.weibouser u;

insert into _weibouser0
select null, u.*
from biae_raw__yong2.weibouser u;

select count(*) from _weibouser0 where last_update_timestamp = 0;

create index last_update_timestamp on _weibouser0 (last_update_timestamp);

delete from _weibouser__01;
insert into _weibouser__01 
select distinct
	u1.idUser,
	max(screen_name),
	max(`name`),
	max(`province`),
	max(`city`),
	max(`location`),
	max(`description`),
	max(`url`),
	max(`profile_image`),
	max(`domain`),
	max(`gender`),
	max(`followers_count`),
	max(`friends_count`),
	max(`statuses_count`),
	max(`favourites_count`),
	max(`created_at`),
	max(`avatar_large`),
	max(`verified`),
	max(`verified_reason`),
	max(`INSERT_TIMESTAMP`),
	max(u1.`LAST_UPDATE_TIMESTAMP`)
from _weibouser0 u1
	join (
		select iduser, max(last_update_timestamp) as last_update_timestamp from _weibouser0
		group by iduser
	) u0
		on u0.iduser = u1.iduser
			and u0.last_update_timestamp = u1.last_update_timestamp
group by u1.idUser;


delete from _weibouser0
where rid in (select rid from _weibouser0 u1
	join (
		select iduser, max(last_update_timestamp) as last_update_timestamp from _weibouser0
		group by iduser
	) u0
		on u0.iduser = u1.iduser
			and u0.last_update_timestamp = u1.last_update_timestamp); 



SET SESSION tmp_table_size=536870912;
SET SESSION max_heap_table_size=536870912; 


select idUser from (
select
	u1.idUser
from _weibouser0 u1
	join (
		select iduser, max(last_update_timestamp) as last_update_timestamp from _weibouser0
		group by iduser
	) u0
		on u0.iduser = u1.iduser
			and u0.last_update_timestamp = u1.last_update_timestamp
group by u1.idUser
) u
group by idUser
having count(*) > 1;





CREATE TABLE `_weibouser3` (
  `rid` bigint(20) NOT NULL AUTO_INCREMENT,
  `idUser` bigint(20) NOT NULL,
  `screen_name` varchar(512) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `province` int(11) DEFAULT NULL,
  `city` int(11) DEFAULT NULL,
  `location` varchar(512) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `profile_image` varchar(512) DEFAULT NULL,
  `domain` varchar(512) DEFAULT NULL,
  `gender` tinyint(4) DEFAULT NULL,
  `followers_count` bigint(20) DEFAULT NULL,
  `friends_count` bigint(20) DEFAULT NULL,
  `statuses_count` bigint(20) DEFAULT NULL,
  `favourites_count` bigint(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `avatar_large` varchar(512) DEFAULT NULL,
  `verified` tinyint(1) DEFAULT '0',
  `verified_reason` varchar(1024) DEFAULT NULL,
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `LAST_UPDATE_TIMESTAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`rid`),
  KEY `idUser` (`idUser`)
) ENGINE=InnoDB AUTO_INCREMENT=710430 DEFAULT CHARSET=utf8;





delete from _weibouser1;
insert into _weibouser1
select u1.*
from _weibouser0 u1
	join (
		select iduser, max(last_update_timestamp) as last_update_timestamp from _weibouser0
		group by iduser
	) u0
		on u0.iduser = u1.iduser
			and u0.last_update_timestamp = u1.last_update_timestamp;

insert into _weibouser2
select null, u.* from biae_raw__yong3.weibouser u;

show create table _weibouser2;

delete from _weibouser3;
insert into _weibouser3
select u1.*
from _weibouser2 u1
	join (
		select iduser, max(rid) as rid from _weibouser2
		group by iduser
	) u0
		on u0.iduser = u1.iduser
			and u0.rid = u1.rid;

select count(distinct iduser) from _weibouser2;


delete from _weibouser__01;
insert into _weibouser__01
select
	u1.idUser,
	(screen_name),
	(`name`),
	(`province`),
	(`city`),
	(`location`),
	(`description`),
	(`url`),
	(`profile_image`),
	(`domain`),
	(`gender`),
	(`followers_count`),
	(`friends_count`),
	(`statuses_count`),
	(`favourites_count`),
	(`created_at`),
	(`avatar_large`),
	(`verified`),
	(`verified_reason`),
	(`INSERT_TIMESTAMP`),
	(u1.`LAST_UPDATE_TIMESTAMP`)
from _weibouser3 u1;





select count(distinct iduser) from _weibouser0;
select count(distinct iduser) from _weibouser1;

create temporary table __weibouser0__1
select iduser, last_update_timestamp, max(rid) as rid
from _weibouser0
group by iduser, last_update_timestamp;

drop table __weibouser0__1;

create temporary table __weibouser0__2
select idu;


drop index multi on _weibouser0;


select count(*)
from _weibouser0 u1
left join _weibouser0 u2 on
	u1.iduser = u2.iduser and
	(u1.last_update_timestamp < u2.last_update_timestamp or
		(u1.last_update_timestamp = u2.last_update_timestamp
			and u1.rid < u2.rid)
	)
where u2.rid is null;

select count(*) from _weibouser0
where verified = 1;

select count(distinct iduser) from _weibouser3;
select count(*) from _weibouser3;

select *
from _weibouser0 u1
join _weibouser0 u2
where u1.iduser = u2.iduser and (u2.last_update_timestamp > u1.last_update_timestamp
	OR (u2.last_update_timestamp = u1.last_update_timestamp AND u2.rid > u1.rid))
group by u1.rid
having count(*) = 0;



