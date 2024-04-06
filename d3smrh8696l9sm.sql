
DROP TABLE IF EXISTS "accidents2023";
CREATE TABLE "public"."accidents2023" (
    "incident_info" text NOT NULL,
    "description" text NOT NULL,
    "start_dt" text NOT NULL,
    "modified_dt" text NOT NULL,
    "quadrant" text NOT NULL,
    "longitude" text NOT NULL,
    "latitude" text NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "reports";
DROP SEQUENCE IF EXISTS reports_report_id_seq;
CREATE SEQUENCE reports_report_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."reports" (
    "report_user" text NOT NULL,
    "comments" text NOT NULL,
    "report_id" integer DEFAULT nextval('reports_report_id_seq') NOT NULL,
    "report_time" timestamp NOT NULL,
    "report_location" text NOT NULL,
    "longitude" text,
    "latitude" text,
    "photo_filename" text,
    "video_filename" text,
    CONSTRAINT "reports_pkey" PRIMARY KEY ("report_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_user_id_seq;
CREATE SEQUENCE users_user_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."users" (
    "username" text NOT NULL,
    "password" text NOT NULL,
    "user_id" integer DEFAULT nextval('users_user_id_seq') NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);


