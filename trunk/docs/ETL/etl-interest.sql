USE biae_raw;

create table biae._user_interest
(
user_id bigint not null,
interest_id int not null,
times int not null,
primary key (user_id, interest_id)
);

create table biae._follower_interest
(
follower_id bigint not null,
interest_id int not null,
times int not null,
primary key (follower_id, interest_id)
);


insert into biae._user_interest
SELECT
	idUser AS user_id,
	interest_id,
	COUNT(*) AS times
FROM tags t
	JOIN keyword_interest i ON t.tag LIKE CONCAT('%', i.keyword, '%')
group by idUser, interest_id;

insert into biae._follower_interest
select fo.id_follower, ui.interest_id, sum(ui.times)
from followers fo
join biae._user_interest ui on ui.user_id = fo.id_user
where fo.is_activefun = 1
group by fo.id_follower, ui.interest_id;


delete from biae.rel_user_interest;
INSERT INTO biae.rel_user_interest (user_id, interest_id)
SELECT
	ui1.follower_id,
	ui1.interest_id
FROM biae._follower_interest ui1
	LEFT OUTER JOIN biae._follower_interest ui2
		ON ui1.follower_id = ui2.follower_id AND ui1.times < ui2.times
GROUP BY ui1.follower_id, ui1.interest_id
HAVING COUNT(*) < 3;


select ui.*, i.interest_desc from biae.rel_user_interest ui
join biae.lu_interest i on i.interest_id = ui.interest_id
order by ui.user_id;

drop table biae._user_interest;
drop table biae._follower_interest;


-- select count(*) from biae.rel_user_interest;
-- select count(distinct user_id) from biae.rel_user_interest;
-- select count(*) from biae.lu_qualified_user;
