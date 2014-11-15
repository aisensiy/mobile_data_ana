-- app stat by day and hour
create table if not exists
req_cnt_and_user_cnt_group_by_app_day_hour as
select count(1) as req_cnt, count(distinct user_id) as user_cnt,
       busi_name, day, hour from log_v2
       group by busi_name, day, hour;

-- location stat by day and hour
create table if not exists
req_cnt_and_user_cnt_group_by_location_day_hour as
select count(1) as req_cnt, count(distinct user_id) as user_cnt,
       location, day, hour from log_v2
       group by location, day, hour;

-- location app stat by day and hour
create table if not exists
req_cnt_group_by_app_location_day_hour as
select count(1) as req_cnt,
       location, busi_name, day, hour from log_v2
       group by location, busi_name, day, hour;
