create database VIS;


create table results_prod_pattern(

ID int primary key auto_increment,
result  bool not null,
patterns_found int not null,
time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL

);

create table results_prod_gap(

ID int primary key auto_increment,
result  bool not null,
gap_result int not null,
time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL

);

SELECT * FROM vis.results_prod_gap;
INSERT INTO `vis`.`results_prod_gap` (`result`, `gap_result`) VALUES ('1', '8');

SELECT * FROM vis.results_prod_pattern;
INSERT INTO `vis`.`results_prod_pattern` (`result`, `patterns_found`) VALUES ('0', '3');

