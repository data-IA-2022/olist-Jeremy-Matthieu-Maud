-- public.payment_items source

CREATE OR REPLACE VIEW public.payment_items
AS SELECT
    ood.order_id,
    ood.customer_id,
    ood.order_status,
    ood.order_purchase_timestamp,
    ood.order_approved_at,
    ood.order_delivered_carrier_date,
    ood.order_delivered_customer_date,
    ood.order_estimated_delivery_date,
    count(DISTINCT ooid.order_item_id) AS n_items,
    count(DISTINCT oopd.payment_sequential) AS n_payments,
    ( SELECT sum(oopd2.payment_value) AS somme
           FROM olist_order_payments_dataset oopd2
          WHERE oopd2.order_id = ood.order_id) AS payment_sum
   FROM olist_orders_dataset ood
     LEFT JOIN olist_order_items_dataset ooid USING (order_id)
     LEFT JOIN olist_order_payments_dataset oopd USING (order_id)
  GROUP BY ood.order_id
  ORDER BY (count(DISTINCT ooid.order_item_id)) DESC;