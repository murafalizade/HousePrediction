create table Estate(
    e_id int primary key,
    e_loc varchar2(200),
    e_floor int,
    e_area number,
    e_room INT,
    price int
);
drop table estate;
insert into estate values(1,'28may',3,120.34,4,12000);
select nvl("Floor",'4/2') from estate;
alter session set"_ORACLE_SCRIPT"=true;
create user murad99 identified by asd;
GRANT create session TO murad99;
GRANT ALL PRIVILEGES TO murad99;
select Floor,Area from estate;
