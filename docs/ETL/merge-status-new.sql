CREATE TABLE `_status000` (
  `_id_status` bigint(20) NOT NULL,
  `_create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `_text` varchar(512) DEFAULT NULL,
  `_source` varchar(512) DEFAULT NULL,
  `_is_favorited` tinyint(4) DEFAULT '0',
  `_is_truncated` tinyint(4) DEFAULT '0',
  `_in_reply_to_status_id` bigint(20) DEFAULT NULL,
  `_in_reply_to_user_id` bigint(20) DEFAULT NULL,
  `_in_reply_to_screen_name` varchar(512) DEFAULT NULL,
  `_mid` bigint(20) NOT NULL,
  `_reposts_count` int(11) NOT NULL,
  `_comments_count` int(11) NOT NULL,
  `_id_user` bigint(20) NOT NULL,
  `_INSERT_TIMESTAMP` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `_LAST_UPDATE_TIMESTAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`_id_status`, `_LAST_UPDATE_TIMESTAMP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert ignore into _status000
select *
from biae_raw.status;

insert ignore into _status000
select *
from status;

delete from biae_raw.status;
insert into biae_raw.status
select s1.*
from _status000 s1
join (
	select _id_status, max(_last_update_timestamp) as ts
	from _status000
	group by _id_status
) s2 on s1._id_status = s2._id_status and s1._last_update_timestamp = s2.ts;

drop table `_status000`;
