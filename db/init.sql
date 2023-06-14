-- Table: public.chat

-- DROP TABLE IF EXISTS public.chat;

CREATE TABLE IF NOT EXISTS public.chat
(
    chat_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    create_date date NOT NULL,
    CONSTRAINT chat_pkey PRIMARY KEY (chat_id)
)

CREATE TABLE IF NOT EXISTS public.check
(
    check_id uuid NOT NULL,
    check_fn bigint NOT NULL,
    check_fd bigint NOT NULL,
    check_fpd bigint NOT NULL,
    chat_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    check_ofd character varying(10) COLLATE pg_catalog."default" NOT NULL,
    check_place character varying(250) COLLATE pg_catalog."default" NOT NULL,
    check_sum numeric(10,2) NOT NULL,
    check_date date NOT NULL,
    CONSTRAINT pk_check_pkey PRIMARY KEY (check_id),
    CONSTRAINT ak_check UNIQUE (check_fn, check_fd, check_fpd),
    CONSTRAINT fk_check_chat FOREIGN KEY (chat_id)
        REFERENCES public.chat (chat_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)