use awesome_chocolates;

select * from people;
select * from products;
select * from `sales_data2`;
order by amount desc
desc `sales-data`;
ALTER TABLE `sales-data`
MODIFY Product int;

set sql_safe_updates=0;
UPDATE `sales-data`
SET Product = REPLACE(Product, 'P', '');
UPDATE products
SET `Product ID` = REPLACE(`Product ID`, 'P', '');

08:19:37	UPDATE `sales-data` SET Product = REPLACE(Product, 'P', '') where Product like 
'P%'	Error Code: 1175. You are using safe update mode and you tried to update a table without
 a WHERE that uses a KEY column.  To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.000 sec



select * from products;
desc products;
select * from Geo;



#Print details of shipments (sales) where amounts are > 2,000 and boxes are <100?
select count(*) FROM `sales-data` where Amount>2000 and Boxes<100;

#How many shipments (sales) each of the sales persons had in the month of January 2023?
SELECT `Sales Person`, COUNT(*) AS total_shipments
FROM `sales-data`
WHERE DATE_FORMAT(date, '%Y-%m') = '2023-01'
GROUP BY `Sales Person`;

#3. Which product sells more boxes? Milk Bars or Eclairs?

#me
with cte as(select products.Product,sum(Boxes) as totalboxes, rank() over(order by sum(Boxes) desc) as rnk from `sales-data` inner join
products on Products.`Product Id` = `sales-data`.Product
where Products.Product in ('Eclairs','Milk Bars')
group by product)
select product from cte where rnk=1;

SELECT p.product,
       SUM(s.boxes) AS total_boxes_sold
FROM products p
JOIN `sales-data` s ON p.`Product ID` = s.product
WHERE p.product IN ('Milk Bars', 'Eclairs')
GROUP BY p.product
ORDER BY total_boxes_sold DESC
limit 1;


with cte as(SELECT Products.Product,sum(Boxes) as totalboxes,rank()
over(order by sum(Boxes) desc) as rnk FROM `sales-data` inner join
products on Products. `Product Id` = `sales-data` .Product where
Products.Product in ('Eclairs','Milk Bars') and year( date )='2023'and
month( date )='07'and day( date ) in ('1','2','3','4') group by Products.Product)
select Product from cte where rnk=1;

SELECT Products.Product,sum(Boxes) as totalboxes,rank()
over(order by sum(Boxes) desc) as rnk FROM `sales-data` inner join
products on Products. `Product Id` = `sales-data` .Product where
Products.Product in ('Eclairs','Milk Bars') and year( date )='2023'and
month( date )='07'and day( date ) in ('1','2','3','4','5','6','7')
 group by Products.Product;
 
 #Which sales person shipments(sales)had above350 customers & under 100 boxes? Did any ofthem occur on Wednesday?

SELECT `Sales Person`, COUNT(*) AS totalcustomers,sum(boxes) as totalboxes
FROM `sales-data`
WHERE dayname(date) = 'wednesday'
GROUP BY `Sales Person`;
#having totalcustomers<100 and totalboxes<100;

# Which salespersons did not make any shipments in the first 7 days of January 2023?
select `sales person` from people where `sales person` not in(SELECT DISTINCT sp.`sales person`
FROM `sales-data` s
JOIN people sp ON s.`sales person` = sp.`SP ID`
WHERE s.date BETWEEN '2023-01-01' AND '2023-01-07');

#How many times we shipped more than 1,000boxes in each month?
select extract(year_month from s.date),sum(Boxes) from `sales-data` s 
group by extract(year_month from s.date)
having sum(Boxes)>1000;

#8.Did we ship at least one boxof ‘After Nines’ to ‘NewZealand’ on all the months?
select distinct extract(year_month from s.date) from
`sales-data` s
 join products p on p.`Product ID`= s.Product
 join geo g on g.GeoID=s.Geo
 where g.Geo='New zealand'and p.Product='After Nines';
 
select distinct extract(year_month from `date`) as yearmonth from `sales-data`
where extract(year_month from `date`) not in (select distinct extract(year_month from s.date) as yearmonth1 from
`sales-data` s
 join products p on p.`Product ID`= s.Product
 join geo g on g.GeoID=s.Geo
 where g.Geo='New zealand'and p.Product='After Nines');
 ------------------------------------------------------------------------------
 with cte as(select g.geo,extract(year_month from s.date) as yearmonth1,sum(boxes) as total
  from
`sales-data` s
 join products p on p.`Product ID`= s.Product
 join geo g on g.GeoID=s.Geo
 where g.Geo in('India','Australia')and
 UPPER(p.Product) like '%choco%' and LOWER(p.Product) like '%choco%'
 group by g.geo,extract(year_month from s.date)
 order by extract(year_month from s.date) asc),cte1 as
 (select geo,yearmonth1,total,rank() over(partition by yearmonth1 order by total desc)as rnk from cte)
 select geo,yearmonth1,total from cte1 where rnk=1;
 
 with cte as(select g.geo,extract(year_month from s.date) as yearmonth1,sum(boxes) as total
  from
`sales-data` s
 join products p on p.`Product ID`= s.Product
 join geo g on g.GeoID=s.Geo
 where g.Geo in('India','Australia')and
 UPPER(p.Product) like '%choco%' and LOWER(p.Product) like '%choco%'
 group by g.geo,extract(year_month from s.date)
 order by extract(year_month from s.date) asc)
 select geo,yearmonth1,total,rank() over(partition by yearmonth1 order by total desc)as rnk from cte;
 -------------------------------------------------------------------------------

create table sales_data as(with cte as(select product,`date`,sum(Boxes) as total,rank() over(partition by `date` order by sum(Boxes) desc)as rnk from `sales-data`
group by product,`date`
order by `date`)
select product,date,total,rnk from cte where rnk<5);

select * from sales_data;

create table sales_data2 as(select `Sales Person`,g.geo,p.product,p.`Cost per Box` as price_box,
extract(year_month from s.date) as yearmonth,Amount,Boxes
  from
`sales-data` s
 join products p on p.`Product ID`= s.Product
 join geo g on g.GeoID=s.Geo);


select * from sales_data2;
 
 select `Sales Person`,g.geo,p.product,p.`Cost per Box` as price_box,
extract(year_month from s.date) as yearmonth,Amount,Boxes
  from
`sales-data` s
 join products p on p.`Product ID`= s.Product
 join geo g on g.GeoID=s.Geo;
 
 select distinct product,price_box from sales_data2;
 
 select product,sum(Amount) from sales_data2
 group by product
 order by sum(Amount) desc
 
 select `Sales Person`,sum(Amount) from sales_data2
 group by `Sales Person`
 order by sum(Amount) desc;
 
 UPDATE sales_data2
SET value = 
  CASE
    WHEN Amount >= 20000 THEN value="high"
    WHEN Amount > 10000&Amount < 20000 THEN value="low"
    ELSE 0
  END;
  
  ALTER TABLE sales_data2
ADD COLUMN value text;
 
 
 UPDATE sales_data2
SET value = 
  CASE
    WHEN Amount between 10000 and 30000 THEN 'high'
    WHEN Amount  between 5000 and 10000 THEN 'medium'
    WHEN Amount<5000 THEN 'low'
  END;
 
 
 
 


