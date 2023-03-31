-- public.items_info source

 CREATE OR REPLACE FUNCTION distance(
    lat1 double precision,
    lon1 double precision,
    lat2 double precision,
    lon2 double precision)
  RETURNS double precision AS
$BODY$
DECLARE
    R integer = 6371e3; -- Meters
    rad double precision = 0.01745329252;
    φ1 double precision = lat1 * rad;
    φ2 double precision = lat2 * rad;
    Δφ double precision = (lat2-lat1) * rad;
    Δλ double precision = (lon2-lon1) * rad;
    a double precision = sin(Δφ/2) * sin(Δφ/2) + cos(φ1) * cos(φ2) * sin(Δλ/2) * sin(Δλ/2);
    c double precision = 2 * atan2(sqrt(a), sqrt(1-a));    
BEGIN                                                     
    RETURN R * c;        
END  
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE VIEW public.items_info
AS SELECT 
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.shipping_limit_date,
    oi.price,
    oi.freight_value,
    p.product_category_name,
    s.seller_zip_code_prefix,
    gs.lat AS seller_lat,
    gs.lng AS seller_lng,
    c.customer_zip_code_prefix,
    gc.lat AS customer_lat,
    gc.lng AS customer_lng,
    distance(gs.lat::double precision, gs.lng::double precision, gc.lat::double precision, gc.lng::double precision) / 1000::double precision AS distance,
    avg(r.review_score) AS score_moy
   FROM olist_order_items_dataset oi
     LEFT JOIN olist_products_dataset p USING (product_id)
     LEFT JOIN olist_orders_dataset o USING (order_id)
     LEFT JOIN olist_customers_dataset c USING (customer_id)
     LEFT JOIN olist_sellers_dataset s USING (seller_id)
     LEFT JOIN olist_order_reviews_dataset r USING (order_id)
     LEFT JOIN avg_geo gc ON c.customer_zip_code_prefix::text = gc.zip_code::text
     LEFT JOIN avg_geo gs ON s.seller_zip_code_prefix::text = gs.zip_code::text
  GROUP BY oi.order_id, oi.order_item_id, p.product_id, s.seller_id, c.customer_id, gs.zip_code, gc.zip_code;
  
 
