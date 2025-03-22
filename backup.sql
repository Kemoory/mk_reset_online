--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: joueurs; Type: TABLE; Schema: public; Owner: yanis
--

CREATE TABLE public.joueurs (
    id integer NOT NULL,
    nom character varying(255) NOT NULL,
    score_trueskill double precision,
    tier character(1),
    CONSTRAINT joueurs_tier_check CHECK ((tier = ANY (ARRAY['S'::bpchar, 'A'::bpchar, 'B'::bpchar, 'C'::bpchar])))
);


ALTER TABLE public.joueurs OWNER TO yanis;

--
-- Name: joueurs_id_seq; Type: SEQUENCE; Schema: public; Owner: yanis
--

CREATE SEQUENCE public.joueurs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.joueurs_id_seq OWNER TO yanis;

--
-- Name: joueurs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yanis
--

ALTER SEQUENCE public.joueurs_id_seq OWNED BY public.joueurs.id;


--
-- Name: participations; Type: TABLE; Schema: public; Owner: yanis
--

CREATE TABLE public.participations (
    joueur_id integer NOT NULL,
    tournoi_id integer NOT NULL,
    score integer
);


ALTER TABLE public.participations OWNER TO yanis;

--
-- Name: tournois; Type: TABLE; Schema: public; Owner: yanis
--

CREATE TABLE public.tournois (
    id integer NOT NULL,
    date date NOT NULL
);


ALTER TABLE public.tournois OWNER TO yanis;

--
-- Name: tournois_id_seq; Type: SEQUENCE; Schema: public; Owner: yanis
--

CREATE SEQUENCE public.tournois_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tournois_id_seq OWNER TO yanis;

--
-- Name: tournois_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yanis
--

ALTER SEQUENCE public.tournois_id_seq OWNED BY public.tournois.id;


--
-- Name: joueurs id; Type: DEFAULT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.joueurs ALTER COLUMN id SET DEFAULT nextval('public.joueurs_id_seq'::regclass);


--
-- Name: tournois id; Type: DEFAULT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.tournois ALTER COLUMN id SET DEFAULT nextval('public.tournois_id_seq'::regclass);


--
-- Data for Name: joueurs; Type: TABLE DATA; Schema: public; Owner: yanis
--

COPY public.joueurs (id, nom, score_trueskill, tier) FROM stdin;
1	Kemoory	\N	\N
2	Vakaeltraz	\N	\N
3	Brook1l	\N	\N
\.


--
-- Data for Name: participations; Type: TABLE DATA; Schema: public; Owner: yanis
--

COPY public.participations (joueur_id, tournoi_id, score) FROM stdin;
1	1	203
2	1	180
3	1	171
\.


--
-- Data for Name: tournois; Type: TABLE DATA; Schema: public; Owner: yanis
--

COPY public.tournois (id, date) FROM stdin;
1	2025-02-27
\.


--
-- Name: joueurs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yanis
--

SELECT pg_catalog.setval('public.joueurs_id_seq', 3, true);


--
-- Name: tournois_id_seq; Type: SEQUENCE SET; Schema: public; Owner: yanis
--

SELECT pg_catalog.setval('public.tournois_id_seq', 1, true);


--
-- Name: joueurs joueurs_pkey; Type: CONSTRAINT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.joueurs
    ADD CONSTRAINT joueurs_pkey PRIMARY KEY (id);


--
-- Name: participations participations_pkey; Type: CONSTRAINT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.participations
    ADD CONSTRAINT participations_pkey PRIMARY KEY (joueur_id, tournoi_id);


--
-- Name: tournois tournois_pkey; Type: CONSTRAINT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.tournois
    ADD CONSTRAINT tournois_pkey PRIMARY KEY (id);


--
-- Name: participations participations_joueur_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.participations
    ADD CONSTRAINT participations_joueur_id_fkey FOREIGN KEY (joueur_id) REFERENCES public.joueurs(id);


--
-- Name: participations participations_tournoi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: yanis
--

ALTER TABLE ONLY public.participations
    ADD CONSTRAINT participations_tournoi_id_fkey FOREIGN KEY (tournoi_id) REFERENCES public.tournois(id);


--
-- PostgreSQL database dump complete
--

