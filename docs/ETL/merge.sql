

show create table biae_raw.followers;

CREATE TABLE `followers` (
  `rid` bigint not null auto_increment,
  `id_user` bigint(20) NOT NULL,
  `id_follower` bigint(20) NOT NULL,
  `is_ActiveFun` tinyint(4) NOT NULL DEFAULT '0',
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into biae__all_raw.`followers` (`id_user`, `id_follower`, `is_ActiveFun`, `INSERT_TIMESTAMP`)
select `id_user`, `id_follower`, `is_ActiveFun`, `INSERT_TIMESTAMP`
from biae_raw__yong2.followers;



CREATE TABLE `followers_real` (
  `id_user` bigint(20) NOT NULL,
  `id_follower` bigint(20) NOT NULL,
  `is_ActiveFun` tinyint(4) NOT NULL DEFAULT '0',
  `INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id_user`, `id_follower`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


delete from followers_real;
insert into followers_real (id_user, id_follower, is_activefun, insert_timestamp)
select id_user, id_follower, max(is_activefun), min(insert_timestamp) as insert_timestamp
from followers
where insert_timestamp > 0
group by id_user, id_follower;

insert into followers_real (id_user, id_follower, is_activefun, insert_timestamp)
select id_user, id_follower, max(is_activefun), 0 as insert_timestamp
from followers
group by id_user, id_follower
having max(followers.insert_timestamp) <= 0;

select count(*) from (
(select id_user, id_follower, max(is_activefun), 0 as insert_timestamp
from followers
group by id_user, id_follower
having max(followers.insert_timestamp) <= 0)) fo;



select count(*) from (select distinct id_user, id_follower from followers) fo;

select date(insert_timestamp) from followers group by date(insert_timestamp);

select id_user, id_follower from followers fo
where id_user in (select idUser from biae_raw.euser)
group by id_user, id_follower;
