# How to construct input.txt from user clicks

```
create table USER_CLICK_TABLE_FILTER
as select
    a.time,a.user_id,a.item_id 
    from
        USER_CLICK_TABLE a
    join
        (select item_id from USER_CLICK_TABLE group by item_id having count(*)>=5) b
    on a.item_id=b.item_id


;;

create table USER_CLICK_TABLE_FILTER_RANK
as select
user_id,time,item_id,row_number() OVER (PARTITION BY user_id ORDER BY time,rand()) as rn
from USER_CLICK_TABLE_FILTER

;;

create table USER_CLICK_TABLE_DICT
as select
item_id,row_number() OVER (ORDER BY item_id) +1 as id
from USER_CLICK_TABLE_FILTER_RANK
group by item_id

;;
-- 3 is the window size of Word2vec

create table USER_CLICK_TABLE_FILTER_WINDOW_PAIR
as select a.user_id,c.id as item1,d.id as item2, 1 as click_times
	from USER_CLICK_TABLE_FILTER_RANK as a
	join  USER_CLICK_TABLE_FILTER_RANK as b
	on a.user_id=b.user_id and a.rn>=b.rn-3 and a.rn<=b.rn+3 and a.rn<>b.rn
	join USER_CLICK_TABLE_DICT c
	on a.item_id = c.item_id
	join USER_CLICK_TABLE_DICT d
	on b.item_id = d.item_id
	
;;
-- 1375017 is the vocabulary size

select concat_ws(' '
,cast(item1 as string) -- word_i
,cast(item2 as string) -- word_j
,cast(floor(rand()*1375017) as string)  -- neg_word_1
,cast(floor(rand()*1375017) as string)  -- neg_word_2
,cast(sum(click_times) as string) -- co_occurrence_ij
)
from USER_CLICK_TABLE_FILTER_WINDOW_PAIR
where item1<>item2
group by item1,item2

-- join item_feature_table for incorporating side information
```