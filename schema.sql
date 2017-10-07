drop table if exists users;
create table users (
  user_id integer primary key autoincrement,
  username text not null,
  password text not null,
  venmo text not null,
  phone_number integer not null
);

drop table if exists listings;
create table listings (
	listing_id integer primary key autoincrement,
	user_id integer not null,
	meal_time integer not null,
	place text not null,
	cost decimal not null,
	status text not null,
	user2_id integer not null
);