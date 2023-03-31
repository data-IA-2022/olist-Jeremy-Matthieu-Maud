/*------------------------------------------------------------Formatage------------------------------------------------------------------------*/

ALTER TABLE public.olist_customers_dataset
    ALTER COLUMN customer_zip_code_prefix TYPE varchar(5) USING customer_zip_code_prefix::varchar,
    ALTER COLUMN customer_state TYPE varchar(2) USING customer_state::varchar;

ALTER TABLE public.olist_sellers_dataset
    ALTER COLUMN seller_zip_code_prefix TYPE varchar(5) USING seller_zip_code_prefix::varchar,
    ALTER COLUMN seller_state TYPE varchar(2) USING seller_state::varchar;
 
ALTER TABLE public.olist_orders_dataset ALTER COLUMN order_purchase_timestamp TYPE timestamp USING order_purchase_timestamp::timestamp;
ALTER TABLE public.olist_orders_dataset ALTER COLUMN order_approved_at TYPE timestamp USING order_approved_at::timestamp;
ALTER TABLE public.olist_orders_dataset ALTER COLUMN order_delivered_carrier_date TYPE timestamp USING order_delivered_carrier_date::timestamp;
ALTER TABLE public.olist_orders_dataset ALTER COLUMN order_delivered_customer_date TYPE timestamp USING order_delivered_customer_date::timestamp;
ALTER TABLE public.olist_orders_dataset ALTER COLUMN order_estimated_delivery_date TYPE timestamp USING order_estimated_delivery_date::timestamp;
ALTER TABLE public.olist_order_reviews_dataset ALTER COLUMN review_creation_date TYPE timestamp USING review_creation_date::timestamp;
ALTER TABLE public.olist_order_reviews_dataset ALTER COLUMN review_answer_timestamp TYPE timestamp USING review_answer_timestamp::timestamp;

/*-----------------------------------------------Création de la table moyenne des geopoints-----------------------------------------------------*/   
   
CREATE TABLE avg_geo (
    zip_code varchar(5),
    lat float4,
    lng float4,
    nbr float4
);

INSERT INTO avg_geo (zip_code, lat, lng, nbr)
SELECT geolocation_zip_code_prefix, AVG(geolocation_lat), AVG(geolocation_lng), count(*) as nbr
FROM olist_geolocation_dataset ogd 
GROUP BY geolocation_zip_code_prefix;

update olist_sellers_dataset set seller_zip_code_prefix =null 
where seller_zip_code_prefix in (
select S.seller_zip_code_prefix 
from olist_sellers_dataset  S
left join avg_geo G on (S.seller_zip_code_prefix=G.zip_code)
where G.zip_code is null
);

update olist_customers_dataset set customer_zip_code_prefix =null 
where customer_zip_code_prefix in (
select C.customer_zip_code_prefix 
from olist_customers_dataset C
left join avg_geo G on (C.customer_zip_code_prefix=G.zip_code)
where G.zip_code is null
);

/*----------------------------------------------------------Création des clés étrangères---------------------------------------------------------*/ 

ALTER TABLE public.olist_customers_dataset ADD CONSTRAINT olist_customers_dataset_pk PRIMARY KEY (customer_id);
ALTER TABLE public.avg_geo ADD CONSTRAINT avg_geo_pk PRIMARY KEY (zip_code);
ALTER TABLE public.olist_order_items_dataset ADD CONSTRAINT olist_order_items_dataset_pk PRIMARY KEY (order_id,order_item_id);
ALTER TABLE public.olist_order_payments_dataset ADD CONSTRAINT olist_order_payments_dataset_pk PRIMARY KEY (order_id,payment_sequential);
ALTER TABLE public.olist_order_reviews_dataset ADD CONSTRAINT olist_order_reviews_dataset_pk PRIMARY KEY (review_id,order_id);
ALTER TABLE public.olist_orders_dataset ADD CONSTRAINT olist_orders_dataset_pk PRIMARY KEY (order_id);
ALTER TABLE public.olist_products_dataset ADD CONSTRAINT olist_products_dataset_pk PRIMARY KEY (product_id);
ALTER TABLE public.olist_sellers_dataset ADD CONSTRAINT olist_sellers_dataset_pk PRIMARY KEY (seller_id);

ALTER TABLE public.olist_sellers_dataset ADD CONSTRAINT olist_sellers_dataset_fk FOREIGN KEY (seller_zip_code_prefix) REFERENCES public.avg_geo(zip_code);
ALTER TABLE public.olist_orders_dataset ADD CONSTRAINT olist_orders_dataset_fk FOREIGN KEY (customer_id) REFERENCES public.olist_customers_dataset(customer_id);
ALTER TABLE public.olist_order_reviews_dataset ADD CONSTRAINT olist_order_reviews_dataset_fk FOREIGN KEY (order_id) REFERENCES public.olist_orders_dataset(order_id);
ALTER TABLE public.olist_order_payments_dataset ADD CONSTRAINT olist_order_payments_dataset_fk FOREIGN KEY (order_id) REFERENCES public.olist_orders_dataset(order_id);
ALTER TABLE public.olist_order_items_dataset ADD CONSTRAINT olist_order_items_dataset_fk FOREIGN KEY (seller_id) REFERENCES public.olist_sellers_dataset(seller_id);
ALTER TABLE public.olist_order_items_dataset ADD CONSTRAINT olist_order_items_dataset_fk_1 FOREIGN KEY (product_id) REFERENCES public.olist_products_dataset(product_id);
ALTER TABLE public.olist_customers_dataset ADD CONSTRAINT olist_customers_dataset_fk FOREIGN KEY (customer_zip_code_prefix) REFERENCES public.avg_geo(zip_code);
ALTER TABLE public.olist_order_items_dataset ADD CONSTRAINT olist_order_items_dataset_fk_2 FOREIGN KEY (order_id) REFERENCES public.olist_orders_dataset(order_id);

/*------------------------------------Création de la colonne product_category_name_french & sans categorie--------------------------------------*/

/*ALTER TABLE public.product_category_name_translation ADD product_category_name_french varchar NULL;*/

INSERT INTO product_category_name_translation (product_category_name, product_category_name_english, product_category_name_french)
VALUES 
('portateis_cozinha_e_preparadores_de_alimentos', 'kitchen_portables_and_food_preparators', 'ustensiles_de_cuisine_et_préparateurs_aliments'),
('pc_gamer', 'pc_gamer', 'pc_gamer'),
('sem categoria', 'without category', 'Sans catégorie');

ALTER TABLE public.product_category_name_translation ADD CONSTRAINT product_category_name_translation_pk PRIMARY KEY (product_category_name);
ALTER TABLE public.olist_products_dataset ADD CONSTRAINT olist_products_dataset_fk FOREIGN KEY (product_category_name) REFERENCES public.product_category_name_translation(product_category_name);

/*-------------------------------------------------Remplacement des null par sans categorie-----------------------------------------------------*/

UPDATE olist_products_dataset
SET product_category_name = 'sem categoria'
WHERE product_category_name is null;

