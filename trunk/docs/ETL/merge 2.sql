select
	count(*), id_user, date(insert_timestamp)
from _followers
where insert_timestamp > 0
and id_user in (select iduser from biae_raw.euser)
group by id_user, date(insert_timestamp)
order by id_user, date(insert_timestamp);





-- update _followers0 set is_activefun = 
show create table _followers0;

CREATE TABLE `_followers__1` (
  `id_user` bigint(20) NOT NULL,
  `id_follower` bigint(20) NOT NULL,
  `is_ActiveFun` tinyint(4) NOT NULL DEFAULT '0',
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id_user`,`id_follower`)
) ENGINE=InnoDB AUTO_INCREMENT=1097711 DEFAULT CHARSET=utf8;


lock tables _followers1 write, _followers read, biae_raw.euser read;
delete from _followers1;

insert into _followers1 (id_user, id_follower, is_activefun, insert_timestamp)
select
	id_user, id_follower, is_activefun, insert_timestamp
from _followers
where insert_timestamp > 0
and id_user in (select iduser from biae_raw.euser);

unlock tables;

update _followers1 set is_activefun = 0;

insert into _followers1 (id_user, id_follower, is_activefun, insert_timestamp)
select * from biae_raw__yong2.followers;


select count(*) from biae_raw__yong2.followers
where id_user in (select iduser from biae_raw.euser);




delete from _followers__1;
insert into _followers__1 (id_user, id_follower, is_activefun, insert_timestamp)
select id_user, id_follower, max(is_activefun), min(insert_timestamp) as insert_timestamp
from _followers1
where insert_timestamp > 0
group by id_user, id_follower;

insert into _followers__1 (id_user, id_follower, is_activefun, insert_timestamp)
select id_user, id_follower, max(is_activefun), 0 as insert_timestamp
from _followers1
group by id_user, id_follower
having max(_followers1.insert_timestamp) <= 0;


select date(insert_timestamp), count(*) from _followers__1
where is_activefun = 1 and id_user in (select iduser from biae_raw.euser)
group by date(insert_timestamp);


select date(insert_timestamp), count(*) from _followers__1
where id_user in (select iduser from biae_raw.euser)
group by date(insert_timestamp);

select count(*) from _followers__1;

