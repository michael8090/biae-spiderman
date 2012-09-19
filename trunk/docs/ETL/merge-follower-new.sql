CREATE TABLE `_followers000` (
  `_id_user` bigint(20) NOT NULL,
  `_id_follower` bigint(20) NOT NULL,
  `_is_ActiveFun` tinyint(4) NOT NULL DEFAULT '0',
  `_INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`_id_user`,`_id_follower`)
) ENGINE=InnoDB AUTO_INCREMENT=1097711 DEFAULT CHARSET=utf8;

insert into _followers000
select *
from biae_raw.followers
on duplicate key update
	_is_activefun = if(_is_activefun = 0, values(_is_activefun), 1),
	_insert_timestamp = if(_insert_timestamp = 0, values(_insert_timestamp),
		if(_insert_timestamp <= values(_insert_timestamp), _insert_timestamp,
			values(_insert_timestamp)))
;

insert into _followers000
select
	f.id_user as _id_user,
	f.id_follower as _id_follower,
	f.is_activefun as _is_activefun,
	f.insert_timestamp as _insert_timestamp
from followers f
on duplicate key update
	_is_activefun = if(_is_activefun = 0, values(_is_activefun), 1),
	_insert_timestamp = if(_insert_timestamp = 0, values(_insert_timestamp),
		if(_insert_timestamp <= values(_insert_timestamp), _insert_timestamp,
			values(_insert_timestamp)))
;

select date(_insert_timestamp), count(*)
from _followers000 fo
join (
	select _id_user, _id_follower, max(_insert_timestamp) as _insert_timestamp
	from _followers000
	group by _id_user, _id_follower, date(_insert_timestamp)
) fo2 using (_insert_timestamp, _id_user, _id_follower)
group by date(_insert_timestamp);

select date(insert_timestamp), count(*)
from biae_raw.followers fo
join (
	select id_user, id_follower, max(insert_timestamp) as insert_timestamp
	from biae_raw.followers
	group by id_user, id_follower, date(insert_timestamp)
) fo2 using (insert_timestamp, id_user, id_follower)
group by date(insert_timestamp);

delete from biae_raw.followers;
insert into biae_raw.followers
select * from _followers000;


drop table _followers000;
