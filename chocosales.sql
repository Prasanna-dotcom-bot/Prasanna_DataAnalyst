#top 5 salesperson id who made more money
select Sales Person ,sum(Amount) as totalamount,rank() over(order by sum(Amount) desc) as rnk from sales-data group by Sales Person ; 
#top 5 salesperson id who made more money based on geography 
select Sales Person ,Geo,sum(Amount) as totalamount,rank() over(order by sum(Amount) desc) as rnk from sales-data group by Sales Person ,Geo; 
#top 5 salesperson id who made more money based on geography and product 
select Sales Person ,Geo,Product,sum(Amount) as totalamount,rank() over(order by sum(Amount) desc) as rnk from sales-data group by Sales Person ,Geo,Product; 
ALTER TABLE sales-data MODIFY COLUMN date DATE; 
select extract(year_month from date ),sum(Amount) as totalamount from sales-data group by extract(year_month from date ) order by sum(Amount) desc; 
#top 5 salesperson name who made more money 
select p. Sales Person ,sum(Amount) as totalamount,rank() over(order by sum(Amount) desc) as rnk from sales-data s join people p on s. Sales Person =p. SP ID group by p. Sales Person limit 5; 
select p. Sales Person ,g.geo,sum(Amount) as totalamount,rank() over(order by sum(Amount) desc) as rnk from sales-data s join people p join Geo g on s. Sales Person =p. SP ID and s.Geo=g.GeoID group by p. Sales Person ,g.geo 
limit 5; 
#Print details of shipments (sales) whereamounts are > 2,000 and boxes are <100?
select * from sales-data where Amount>2000 and Boxes<100;
#How many shipments (sales) each of the sales persons had in the month of July 2022?
select p.Sales Person,count(Amount) as totalamount,rank() over(order bysum(Amount) desc) as rnk from sales-data s join people p on s.SalesPerson=p.SP ID where extract(year_month from date)=202207 group byp.Sales Person;
#Which product sells more boxes? Milk Bars orEclairs?
with cte_more as (select p.Product,sum(Boxes) as NoofBoxes,rank()over(order by sum(Boxes) desc) as rnk from sales-data s join Products pon s.Product=p.Product ID where p.Product in('Milk Bars','Eclairs') groupby p.Product)
select product from cte_more where rnk=1;
#Which product sold more boxes in the first 7days of july 2022? Milk Bars or Eclairs?
select p.Product,sum(Boxes) as NoofBoxes,rank() over(order bysum(Boxes) desc) as rnk from sales-data s join Products p ons.Product=p.Product ID where p.Product in('Milk Bars','Eclairs') and datebetween '2022-07-1' and '2022-07-7' group by p.Product;
select Product,sum(boxes) from sales-data where date between '2022-07-1' and '2022-07-7' and product in ('P01','P06') group by Product;
with cte_july_more as (select p.Product,sum(Boxes) as NoofBoxes,rank()over(order by sum(Boxes) desc) as rnk from sales-data s join Products pon s.Product=p.Product ID where p.Product in('Milk Bars','Eclairs') anddate between '2022-07-1' and '2022-07-7' group by p.Product) selectProduct from cte_july_more where rnk=1;
#Which Product shipments(sales)had above350 customers & under 100 boxes? Did any ofthem occur on Wednesday?
select * from sales-data where Boxes<100;
Select count(*) from sales-data WHERE Product="P14";
select Product,count(sales person) as customers from sales-datawhere Boxes<100 group by product having count(sales person)<100;
select p.Product,count(sales person) as customers from sales-data sjoin products p on s.Product=p.Product ID where Boxes<100 anddayofweek(date)=4 group by p.product having count(sales person)<100;
select day(date) from sales-data;
select p. Sales Person ,g.geo,p1.product,sum(Amount) as totalamount,rank() over(order by sum(Amount) desc) as rnk from sales-data s join people p join Geo g join products p1 on s. Sales Person =p. SP ID and s.Geo=g.GeoID and s.Product=p1. Product ID group by p. Sales Person ,g.geo,p1.product 
limit 5;

dayofweek returns1,2,3,4,5,6,7...sunday,mon,tue..so wed means4
#What are the names of salespersons who had at least one shipment (sale) in the first 7 daysof july 2022?
select p.Sales Person,count(Amount) as totalamount from sales-data sjoin people p on s.Sales Person=p.SP ID where date between '2022-07-01' and '2022-07-07' group by p.Sales Person having count(Amount)>1
#Which salespersons did not make any shipments in the first 7 days of july 2022?
select p.Sales Person from sales-data s join people p on s.SalesPerson=p.SP ID where p.Sales Person not in (select p.Sales Personfrom sales-data s join people p on s.Sales Person=p.SP ID where datebetween '2022-07-01' and '2022-07-07' group by p.Sales Person havingcount(Amount)>=1);
create temporary table names_sp as( select Sales Person,count(amount)as total from sales-data where date between '2022-07-01' and '2022-07-07' group by Sales Person having count(amount)>=1);
select Sales Person from people where SP ID not in(select Sales Personfrom names_sp);
other way
select p.Sales Person from people p left join sales-data s on p.SPID=s.Sales Person and date between '2022-07-01' and '2022-07-07' wheres.Sales Person is null;
select * from people p left join sales-data s on p.SP ID=s.Sales Personand date between '2022-07-01' and '2022-07-07' where s.Sales Person isnull;
#How many times we shipped more than 1,000boxes in each month?
wrong
select extract(year_month from date),sum(Boxes) as totalBoxes fromsales-data group by extract(year_month from date) order by sum(Boxes)desc;
select month(date)as month,count(*) as shipments from sales-datawhere Boxes>1000 group by month(date) order by month(date);
select count(*) from sales-data where month(date)=1 and Boxes>1000
