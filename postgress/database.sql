--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: add_vote_karma_to_karma_on_insert(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.add_vote_karma_to_karma_on_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
        IF new.is_upvote THEN
            UPDATE 
                karma 
            set 
                upvotes = upvotes + 1 
            where 
                id = new.karma_id;
        ELSE
            UPDATE 
                karma 
            set 
                downvotes = downvotes + 1 
            where 
                id = new.karma_id;
        END IF;
 
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.add_vote_karma_to_karma_on_insert() OWNER TO prod;

--
-- Name: add_vote_karma_to_karma_on_update(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.add_vote_karma_to_karma_on_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
        IF old.is_upvote != new.is_upvote THEN
            IF new.is_upvote THEN
                UPDATE 
                    karma 
                set 
                    upvotes = upvotes + 1,
                    downvotes = downvotes - 1
                where 
                    id = new.karma_id;
            ELSE
                UPDATE 
                    karma 
                set 
                    upvotes = upvotes - 1,
                    downvotes = downvotes + 1 
                where 
                    id = new.karma_id;
            END IF;
        ELSE
            RETURN NEW;
        END IF;

 
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.add_vote_karma_to_karma_on_update() OWNER TO prod;

--
-- Name: add_vote_karma_to_users_on_update(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.add_vote_karma_to_users_on_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    k_id CONSTANT integer := (SELECT karma_id FROM users WHERE karma_id = new.id);
BEGIN
    IF old.upvotes != new.upvotes THEN
        UPDATE
            karma k
        SET 
            k.upvotes = k.upvotes
        WHERE  
            karma_id = k_id;
    END IF;  
    IF old.downvotes != new.downvotes THEN
        UPDATE
            karma k
        SET 
            k.downvotes = k.downvotes
        WHERE  
            karma_id = k_id;
    END IF;                                                         
    RETURN NEW;                               
END;                                          
$$;


ALTER FUNCTION public.add_vote_karma_to_users_on_update() OWNER TO prod;

--
-- Name: create_karma_for_comments(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.create_karma_for_comments() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  with x as (
    insert into karma(upvotes) values (default) returning id
    )
    update comments set karma_id = (select x.id from x) where id = NEW.id;
    return new;
END$$;


ALTER FUNCTION public.create_karma_for_comments() OWNER TO prod;

--
-- Name: create_karma_for_posts(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.create_karma_for_posts() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  with x as (
    insert into karma(upvotes) values (default) returning id
    )
    update posts set karma_id = (select x.id from x) where id = NEW.id;
    return new;
END$$;


ALTER FUNCTION public.create_karma_for_posts() OWNER TO prod;

--
-- Name: create_karma_for_users(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.create_karma_for_users() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  with x as (
    insert into karma(upvotes) values (default) returning id
    )
    update users set karma_id = (select x.id from x) where id = NEW.id;
    return new;
END$$;


ALTER FUNCTION public.create_karma_for_users() OWNER TO prod;

--
-- Name: update_modified_on_column(); Type: FUNCTION; Schema: public; Owner: prod
--

CREATE FUNCTION public.update_modified_on_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    NEW.modified_on = NOW();
    RETURN NEW;
  END;
$$;


ALTER FUNCTION public.update_modified_on_column() OWNER TO prod;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: prod
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    post_id integer NOT NULL,
    content text NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    parent_id integer,
    modified_on timestamp without time zone DEFAULT now() NOT NULL,
    karma_id integer,
    user_id integer NOT NULL,
    hanesst_id integer
);


ALTER TABLE public.comments OWNER TO prod;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: prod
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comments_id_seq OWNER TO prod;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: prod
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: karma; Type: TABLE; Schema: public; Owner: prod
--

CREATE TABLE public.karma (
    upvotes integer DEFAULT 0 NOT NULL,
    downvotes integer DEFAULT 0 NOT NULL,
    id integer NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    modified_on timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.karma OWNER TO prod;

--
-- Name: karma_id_seq; Type: SEQUENCE; Schema: public; Owner: prod
--

CREATE SEQUENCE public.karma_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.karma_id_seq OWNER TO prod;

--
-- Name: karma_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: prod
--

ALTER SEQUENCE public.karma_id_seq OWNED BY public.karma.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: prod
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    content text NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    modified_on timestamp without time zone DEFAULT now() NOT NULL,
    is_link boolean NOT NULL,
    karma_id integer,
    user_id integer NOT NULL,
    hanesst_id integer,
    title text
);


ALTER TABLE public.posts OWNER TO prod;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: prod
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_id_seq OWNER TO prod;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: prod
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: prod
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    password integer NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    modified_on timestamp without time zone DEFAULT now() NOT NULL,
    karma_id integer
);


ALTER TABLE public.users OWNER TO prod;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: prod
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO prod;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: prod
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_karma; Type: TABLE; Schema: public; Owner: prod
--

CREATE TABLE public.users_karma (
    user_id integer NOT NULL,
    karma_id integer NOT NULL,
    is_upvote boolean DEFAULT true
);


ALTER TABLE public.users_karma OWNER TO prod;

--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: karma id; Type: DEFAULT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.karma ALTER COLUMN id SET DEFAULT nextval('public.karma_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: karma karma_pkey; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.karma
    ADD CONSTRAINT karma_pkey PRIMARY KEY (id);


--
-- Name: posts posts_hanesst_id_key; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_hanesst_id_key UNIQUE (hanesst_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: users_karma users_karma_user_id_karma_id_key; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.users_karma
    ADD CONSTRAINT users_karma_user_id_karma_id_key UNIQUE (user_id, karma_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: users_karma_id_idx; Type: INDEX; Schema: public; Owner: prod
--

CREATE INDEX users_karma_id_idx ON public.users USING btree (karma_id);


--
-- Name: karma add_karma_to_user_karma_on_update; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER add_karma_to_user_karma_on_update BEFORE UPDATE ON public.karma FOR EACH ROW EXECUTE PROCEDURE public.add_vote_karma_to_users_on_update();


--
-- Name: users_karma add_vote_karma_to_karma_on_insert; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER add_vote_karma_to_karma_on_insert AFTER INSERT ON public.users_karma FOR EACH ROW EXECUTE PROCEDURE public.add_vote_karma_to_karma_on_insert();


--
-- Name: users_karma add_vote_karma_to_karma_on_update; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER add_vote_karma_to_karma_on_update BEFORE UPDATE ON public.users_karma FOR EACH ROW EXECUTE PROCEDURE public.add_vote_karma_to_karma_on_update();


--
-- Name: users insert_karma_trigger; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER insert_karma_trigger AFTER INSERT ON public.users FOR EACH ROW EXECUTE PROCEDURE public.create_karma_for_users();


--
-- Name: posts insert_karma_trigger; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER insert_karma_trigger AFTER INSERT ON public.posts FOR EACH ROW EXECUTE PROCEDURE public.create_karma_for_posts();


--
-- Name: comments insert_karma_trigger; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER insert_karma_trigger AFTER INSERT ON public.comments FOR EACH ROW EXECUTE PROCEDURE public.create_karma_for_comments();


--
-- Name: posts update_modified_on; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER update_modified_on BEFORE UPDATE ON public.posts FOR EACH ROW EXECUTE PROCEDURE public.update_modified_on_column();


--
-- Name: users update_modified_on; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER update_modified_on BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE PROCEDURE public.update_modified_on_column();


--
-- Name: comments update_modified_on; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER update_modified_on BEFORE UPDATE ON public.comments FOR EACH ROW EXECUTE PROCEDURE public.update_modified_on_column();


--
-- Name: karma update_modified_on; Type: TRIGGER; Schema: public; Owner: prod
--

CREATE TRIGGER update_modified_on BEFORE UPDATE ON public.karma FOR EACH ROW EXECUTE PROCEDURE public.update_modified_on_column();


--
-- Name: comments comments_karma_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_karma_id_fkey FOREIGN KEY (karma_id) REFERENCES public.karma(id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: posts posts_karma_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_karma_id_fkey FOREIGN KEY (karma_id) REFERENCES public.karma(id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_karma_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: prod
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_karma_id_fkey FOREIGN KEY (karma_id) REFERENCES public.karma(id);


--
-- PostgreSQL database dump complete
--

