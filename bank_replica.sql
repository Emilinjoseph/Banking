use bank_replica;

create table bank_user(
id int primary key auto_increment,
first_name varchar(10),
last_name varchar(10),
mobile_no bigint unique,
account_no varchar(10) unique,
user_password varchar(10),
balance float default 0);

desc bank_user;

create table acct_stmt(
ref_id int primary key auto_increment,
user_id int,
credit_amt float,
debit_amt float,
current_balance float,
date_of_transaction datetime,
foreign key (user_id) references bank_user(id)
on delete cascade);


desc bank_user;


create procedure insert_user(in first_name varchar(10),in last_name varchar(10),in mobile_no bigint,in account_no varchar(10),in user_password varchar(10))
insert into bank_user(first_name,last_name,mobile_no,account_no,user_password)values(first_name,last_name,mobile_no,account_no,user_password);

delimiter $$
create procedure depositing(in userId int,in credit_amt float)
begin
DECLARE  bal float;
set bal=(select balance from bank_user where id=userId)+credit_amt ;
insert into acct_stmt(user_id,credit_amt,current_balance,date_of_transaction)values(userId,credit_amt,bal,now());
update bank_user set balance=bal where id=userId;
end $$
delimiter ;

delimiter $$
create procedure withdrawal(in userId int,in withdraw_amt float)
begin
DECLARE  bal float;
set bal=(select balance from bank_user where id=userId)-withdraw_amt;
update bank_user set balance=bal where id=userId;
insert into acct_stmt(user_id,debit_amt,current_balance,date_of_transaction)values(userId,withdraw_amt,bal,now());

end $$
delimiter ;

DELIMITER $$
CREATE TRIGGER before_withdrawal
before update ON bank_user
FOR EACH ROW
BEGIN
 if new.balance<0 then signal sqlstate '45000'
 set message_text= "can't withdraw the money bcoz balance amount is not enough ";
 end if;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER before_withdrawal1
before insert ON acct_stmt
FOR EACH ROW
BEGIN
 if new.balance<0 then signal sqlstate '45000'
 set message_text= "can't withdraw the money bcoz balance amount is not enough ";
 end if;
END $$
DELIMITER ;


create procedure check_valid_user(in userId int,in userPassword varchar(10) ,out checkFlag int)
select count(id) into checkFlag from bank_user where id= userId and user_password=userPassword;



select * from bank_user;
select * from acct_stmt;

drop trigger before_withdrawal;
drop table bank_user;
drop table acct_stmt;
drop procedure insert_user;
drop procedure check_valid_user;
drop procedure depositing;
drop procedure withdrawal;
truncate table bank_user;
truncate table acct_stmt;
SET foreign_key_checks = 0;



