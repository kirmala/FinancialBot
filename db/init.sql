-- Table: public.chat

-- DROP TABLE IF EXISTS public.chat;

CREATE TABLE IF NOT EXISTS public.chat
(
    chat_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    create_date date NOT NULL,
    CONSTRAINT chat_pkey PRIMARY KEY (chat_id)
)

CREATE TABLE IF NOT EXISTS public.receipt
(
    receipt_id uuid NOT NULL,
    receipt_fn bigint NOT NULL,
    receipt_fd bigint NOT NULL,
    receipt_fpd bigint NOT NULL,
    chat_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receipt_ofd character varying(10) COLLATE pg_catalog."default" NOT NULL,
    receipt_place character varying(250) COLLATE pg_catalog."default" NOT NULL,
    receipt_sum numeric(10,2) NOT NULL,
    receipt_date date NOT NULL,
    CONSTRAINT pk_receipt_pkey PRIMARY KEY (receipt_id),
    CONSTRAINT ak_receipt UNIQUE (receipt_fn, receipt_fd, receipt_fpd),
    CONSTRAINT fk_receipt_chat FOREIGN KEY (chat_id)
        REFERENCES public.chat (chat_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.receipt_item
(
    item_name character varying(100) NOT NULL,
    item_price numeric(10,2) NOT NULL,
    item_amount bigint NOT NULL,
    item_sum numeric(10,2) NOT NULL,
    item_id uuid NOT NULL,
    receipt_id uuid NOT NULL,
    CONSTRAINT pk_item_pkey PRIMARY KEY (item_id),
    CONSTRAINT fk_item_receipt FOREIGN KEY (receipt_id)
        REFERENCES public.receipt (receipt_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

