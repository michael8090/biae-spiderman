select
	count(*), id_user, date(insert_timestamp)
from _followers
where insert_timestamp > 0
and id_user in (select iduser from biae_raw.euser)
group by id_user, date(insert_timestamp)
order by id_user, date(insert_timestamp);





-- update _followers0 set is_activefun = 
show create table _followers0;

CREATE TABLE `_followers__3` (
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

select date(insert_timestamp), count(*) from biae_raw__yong2.followers
where is_activefun = 1 and id_user in (select iduser from biae_raw.euser)
group by date(insert_timestamp);


select count(*) from _followers__1;


select count(*) from _followers__1
where is_activefun = 1 and id_user in (select iduser from biae_raw.euser)
;

	select count(*) from biae_raw__yong2.followers
	where is_activefun = 1 and id_user in (select iduser from biae_raw.euser)
	;

select count(*) from _followers__1
where insert_timestamp > 0 and id_user in (select iduser from biae_raw.euser);

create table _followers__2
select * from _followers__1
where id_user in (select iduser from biae_raw.euser)
and insert_timestamp > 0;

select count(*) from biae_raw.euser;
select count(*) from _followers__2;


drop table _followers__2;


insert into _followers2
select null, _followers__2.*
from _followers__2;

insert into _followers2
select null, fo.*
from biae_raw__yong3.followers fo;

select count(*) from _followers2;


delete from _followers__3;
insert into _followers__3 (id_user, id_follower, is_activefun, insert_timestamp)
select id_user, id_follower, max(is_activefun), min(insert_timestamp) as insert_timestamp
from _followers2 fo
where insert_timestamp > 0
group by id_user, id_follower;

insert into _followers__3 (id_user, id_follower, is_activefun, insert_timestamp)
select id_user, id_follower, max(is_activefun), 0 as insert_timestamp
from _followers2 fo
group by id_user, id_follower
having max(insert_timestamp) <= 0;

select count(distinct id_follower) from _followers__3;

select count(*) from _followers__3 where is_activefun = 1 and id_user in 
(select iduser from biae_raw.euser);


select count(distinct id_user) from _followers__3;



insert into _weibouser__02
select u.* from _weibouser__01 u join __uuu uu on u.iduser = uu.uid;


create table __uuu (
uid bigint not null,
primary key (uid)
);

insert ignore into __uuu
select id_follower from _followers__3;

select count(*) from _weibouser__02;

select uid
from __uuu uu left join _weibouser__02 u on uu.uid = u.iduser
where iduser is null;

delete from biae_raw.weibouser;
insert into biae_raw.weibouser
select * from _weibouser__02;

show create table biae_raw.__old_followers;

CREATE TABLE biae_raw.`followers` (
  `id_user` bigint(20) NOT NULL,
  `id_follower` bigint(20) NOT NULL,
  `is_ActiveFun` tinyint(4) NOT NULL DEFAULT '0',
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id_user`,`id_follower`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


insert into biae_raw.followers
select * from _followers__3;



