-- Table: public.chat

-- DROP TABLE IF EXISTS public.chat;

CREATE TABLE IF NOT EXISTS public.chat
(
    chat_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    create_date date NOT NULL,
    CONSTRAINT chat_pkey PRIMARY KEY (chat_id)
)

