use biae_raw;
select date(insert_timestamp), count(*)
from biae_raw.followers fo
join (
	select id_follower, id_user, max(insert_timestamp) as ts
	from biae_raw.followers
	group by id_follower, id_user
) fo2 on fo.id_follower = fo2.id_follower and fo.id_user = fo2.id_user
	and fo.insert_timestamp = fo2.ts
group by date(insert_timestamp);

select distinct date(insert_timestamp) from tags;

select distinct date(insert_timestamp) from usercounters;

select distinct date(insert_timestamp) from weibouser;

