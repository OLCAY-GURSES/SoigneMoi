-- Début de la transaction
BEGIN;
CREATE TABLE IF NOT EXISTS "book_appointment" (
	"appointment_id"	integer NOT NULL,
	"start_date"	date,
	"end_date"	date,
	"motif"	text NOT NULL,
	"serial_number"	varchar(200),
	"choise_speciality_id"	integer,
	"doctor_id"	integer NOT NULL,
	"doctor_time_slots_id"	bigint,
	"patient_id"	integer NOT NULL,
	FOREIGN KEY("doctor_id") REFERENCES "book_doctor"("doctor_id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("doctor_time_slots_id") REFERENCES "book_doctortimeslots"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("patient_id") REFERENCES "book_patient"("patient_id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("choise_speciality_id") REFERENCES "book_specialization"("specialization_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("appointment_id" AUTOINCREMENT)
);


CREATE TABLE IF NOT EXISTS "book_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	"last_name"	varchar(150) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"email"	varchar(254) NOT NULL UNIQUE,
	"is_admin"	bool NOT NULL,
	"is_patient"	bool NOT NULL,
	"login_status"	bool NOT NULL,
	"is_doctor"	bool NOT NULL,
	"is_secretary"	bool NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
-- Étape 1: Création de l'utilisateur
SERT INTO "book_user"VALUES (9,'.......','2024-03-16 06:33:49.966509',0,'Victor','Devos',0,1,'2024-03-16 06:26:20.597359','vic.devos@gmail.com',0,1,0,0,0);


-- Étape 2: Réservation d'un séjour associé au patient
INSERT INTO "book_appointment" VALUES (1,'2024-03-16','2024-03-24','','#PTZW5DTS',NULL,1,NULL,1);

-- Fin de la transaction (commit)
COMMIT;