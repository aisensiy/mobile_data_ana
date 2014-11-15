select * into outfile 'C:\\temp\\req_cnt_and_user_cnt_group_by_app_day_hour.csv'
fields terminated by ','
enclosed by '"'
escaped by '"'
lines terminated by '\r\n'
from req_cnt_and_user_cnt_group_by_app_day_hour;

select * into outfile 'C:\\temp\\req_cnt_and_user_cnt_group_by_location_day_hour.csv'
fields terminated by ','
enclosed by '"'
escaped by '"'
lines terminated by '\r\n'
from req_cnt_and_user_cnt_group_by_location_day_hour;
