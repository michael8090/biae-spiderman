delete from biae_raw.tags;

show create table tags;

CREATE TABLE `_tags000` (
  `idUser` bigint(20) NOT NULL,
  `tagId` bigint(20) NOT NULL,
  `tag` varchar(512) NOT NULL,
  `weight` int(11) DEFAULT NULL,
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `LAST_UPDATE_TIMESTAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idUser`,`tagId`, last_update_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert ignore into _tags000
select * from biae_raw.tags;

insert ignore into _tags000
select * from tags;


delete from biae_raw.tags;
insert into biae_raw.tags
select s1.*
from _tags000 s1
join (
	select idUser, max(last_update_timestamp) as ts
	from _tags000
	group by idUser
) s2 on s1.idUser = s2.idUser
	and s1.last_update_timestamp = s2.ts;

drop table `_tags000`;
