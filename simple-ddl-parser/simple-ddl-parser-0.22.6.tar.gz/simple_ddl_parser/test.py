from simple_ddl_parser import DDLParser

ddl =  """
--
-- PostgreSQL database dump
--

-- Dumped from database version 11.6 (Debian 11.6-1.pgdg90+1)
-- Dumped by pg_dump version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: myapp
--

CREATE TABLE public.accounts (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    created_on timestamp without time zone NOT NULL,
    last_login timestamp without time zone
);


ALTER TABLE public.accounts OWNER TO myapp;

--
-- Name: accounts_user_id_seq; Type: SEQUENCE; Schema: public; Owner: myapp
--

CREATE SEQUENCE public.accounts_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_user_id_seq OWNER TO myapp;

--
-- Name: accounts_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myapp
--

ALTER SEQUENCE public.accounts_user_id_seq OWNED BY public.accounts.user_id;


--
-- Name: sps; Type: TABLE; Schema: public; Owner: myapp
--

CREATE TABLE public.sps (
    ts tstzrange
);


ALTER TABLE public.sps OWNER TO myapp;

--
-- Name: accounts user_id; Type: DEFAULT; Schema: public; Owner: myapp
--

ALTER TABLE ONLY public.accounts ALTER COLUMN user_id SET DEFAULT nextval('public.accounts_user_id_seq'::regclass);


--
-- Name: accounts accounts_email_key; Type: CONSTRAINT; Schema: public; Owner: myapp
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_email_key UNIQUE (email);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: myapp
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (user_id);


--
-- Name: accounts accounts_username_key; Type: CONSTRAINT; Schema: public; Owner: myapp
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--


"""
result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
import pprint

pprint.pprint(result)
