BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	bigint NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	bigint NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_admin" (
	"admin_id"	integer NOT NULL,
	"user_id"	bigint UNIQUE,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("admin_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	bigint NOT NULL,
	"action_time"	datetime NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "authtoken_token" (
	"key"	varchar(40) NOT NULL,
	"created"	datetime NOT NULL,
	"user_id"	bigint NOT NULL UNIQUE,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("key")
);
CREATE TABLE IF NOT EXISTS "book_hospital" (
	"hospital_id"	integer NOT NULL,
	"name"	varchar(200),
	"address"	varchar(200),
	"featured_image"	varchar(100),
	"description"	text,
	"email"	varchar(200),
	"phone_number"	varchar(10),
	PRIMARY KEY("hospital_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_specialization" (
	"specialization_id"	integer NOT NULL,
	"specialization_name"	varchar(200),
	"hospital_id"	integer,
	FOREIGN KEY("hospital_id") REFERENCES "book_hospital"("hospital_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("specialization_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_doctor" (
	"doctor_id"	integer NOT NULL,
	"first_name"	varchar(200),
	"last_name"	varchar(200),
	"phone_number"	varchar(200),
	"hospital_name_id"	integer,
	"specialization_id"	integer,
	"user_id"	bigint UNIQUE,
	"date_of_birth"	date,
	"reg_number"	varchar(6),
	FOREIGN KEY("specialization_id") REFERENCES "book_specialization"("specialization_id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("hospital_name_id") REFERENCES "book_hospital"("hospital_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("doctor_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_patient" (
	"patient_id"	integer NOT NULL,
	"first_name"	varchar(200),
	"last_name"	varchar(200),
	"phone_number"	varchar(10),
	"address"	varchar(200),
	"serial_number"	varchar(200),
	"user_id"	bigint UNIQUE,
	"date_of_birth"	date,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("patient_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_doctortimeslots" (
	"id"	integer NOT NULL,
	"doc_start_date"	date,
	"doc_end_date"	date,
	"doctor_id"	integer NOT NULL,
	FOREIGN KEY("doctor_id") REFERENCES "book_doctor"("doctor_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
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
CREATE TABLE IF NOT EXISTS "book_prescription" (
	"prescription_id"	integer NOT NULL,
	"create_date"	date,
	"doctor_id"	integer,
	"patient_id"	integer,
	"extra_information"	text,
	FOREIGN KEY("patient_id") REFERENCES "book_patient"("patient_id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("doctor_id") REFERENCES "book_doctor"("doctor_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("prescription_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_test_information" (
	"test_id"	integer NOT NULL,
	"test_name"	varchar(200),
	"test_description"	text,
	PRIMARY KEY("test_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_prescription_medicine" (
	"medicine_id"	integer NOT NULL,
	"medicine_name"	varchar(200),
	"quantity"	varchar(200),
	"start_day"	date,
	"end_day"	date,
	"frequency"	varchar(200),
	"instruction"	text,
	"prescription_id"	integer,
	"dosage"	varchar(200),
	FOREIGN KEY("prescription_id") REFERENCES "book_prescription"("prescription_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("medicine_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_prescription_test" (
	"test_id"	integer NOT NULL,
	"test_name"	varchar(200),
	"test_description"	text,
	"test_info_id"	varchar(200),
	"prescription_id"	integer,
	"test_results"	text,
	FOREIGN KEY("prescription_id") REFERENCES "book_prescription"("prescription_id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("test_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "book_secretary" (
	"secretary_id"	integer NOT NULL,
	"first_name"	varchar(200),
	"last_name"	varchar(200),
	"phone_number"	varchar(200),
	"reg_number"	varchar(6),
	"hospital_name_id"	integer,
	"user_id"	bigint UNIQUE,
	"address"	varchar(200),
	"date_of_birth"	date,
	FOREIGN KEY("hospital_name_id") REFERENCES "book_hospital"("hospital_id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "book_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("secretary_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2024-03-16 05:40:59.841146');
INSERT INTO "django_migrations" VALUES (2,'contenttypes','0002_remove_content_type_name','2024-03-16 05:40:59.850410');
INSERT INTO "django_migrations" VALUES (3,'auth','0001_initial','2024-03-16 05:40:59.864424');
INSERT INTO "django_migrations" VALUES (4,'auth','0002_alter_permission_name_max_length','2024-03-16 05:40:59.872428');
INSERT INTO "django_migrations" VALUES (5,'auth','0003_alter_user_email_max_length','2024-03-16 05:40:59.877440');
INSERT INTO "django_migrations" VALUES (6,'auth','0004_alter_user_username_opts','2024-03-16 05:40:59.884458');
INSERT INTO "django_migrations" VALUES (7,'auth','0005_alter_user_last_login_null','2024-03-16 05:40:59.890504');
INSERT INTO "django_migrations" VALUES (8,'auth','0006_require_contenttypes_0002','2024-03-16 05:40:59.895489');
INSERT INTO "django_migrations" VALUES (9,'auth','0007_alter_validators_add_error_messages','2024-03-16 05:40:59.903067');
INSERT INTO "django_migrations" VALUES (10,'auth','0008_alter_user_username_max_length','2024-03-16 05:40:59.910071');
INSERT INTO "django_migrations" VALUES (11,'auth','0009_alter_user_last_name_max_length','2024-03-16 05:40:59.916128');
INSERT INTO "django_migrations" VALUES (12,'auth','0010_alter_group_name_max_length','2024-03-16 05:40:59.924134');
INSERT INTO "django_migrations" VALUES (13,'auth','0011_update_proxy_permissions','2024-03-16 05:40:59.930136');
INSERT INTO "django_migrations" VALUES (14,'auth','0012_alter_user_first_name_max_length','2024-03-16 05:40:59.937093');
INSERT INTO "django_migrations" VALUES (15,'book','0001_initial','2024-03-16 05:40:59.952672');
INSERT INTO "django_migrations" VALUES (16,'admin','0001_initial','2024-03-16 05:40:59.966121');
INSERT INTO "django_migrations" VALUES (17,'admin','0002_logentry_remove_auto_add','2024-03-16 05:40:59.978121');
INSERT INTO "django_migrations" VALUES (18,'admin','0003_logentry_add_action_flag_choices','2024-03-16 05:40:59.986762');
INSERT INTO "django_migrations" VALUES (19,'authtoken','0001_initial','2024-03-16 05:40:59.996788');
INSERT INTO "django_migrations" VALUES (20,'authtoken','0002_auto_20160226_1747','2024-03-16 05:41:00.014208');
INSERT INTO "django_migrations" VALUES (21,'authtoken','0003_tokenproxy','2024-03-16 05:41:00.019995');
INSERT INTO "django_migrations" VALUES (22,'book','0002_hospital_alter_admin_user','2024-03-16 05:41:00.030303');
INSERT INTO "django_migrations" VALUES (23,'book','0003_specialization','2024-03-16 05:41:00.041323');
INSERT INTO "django_migrations" VALUES (24,'book','0004_user_is_patient_user_login_status_patient','2024-03-16 05:41:00.061949');
INSERT INTO "django_migrations" VALUES (25,'book','0005_user_is_doctor_doctor','2024-03-16 05:41:00.083678');
INSERT INTO "django_migrations" VALUES (26,'book','0006_rename_dob_doctor_date_of_bird_and_more','2024-03-16 05:41:00.114784');
INSERT INTO "django_migrations" VALUES (27,'book','0007_alter_doctor_date_of_bird_alter_patient_date_of_bird_and_more','2024-03-16 05:41:00.181748');
INSERT INTO "django_migrations" VALUES (28,'book','0008_appointment','2024-03-16 05:41:00.198796');
INSERT INTO "django_migrations" VALUES (29,'book','0009_prescription_prescription_medicine_prescription_test','2024-03-16 05:41:00.231852');
INSERT INTO "django_migrations" VALUES (30,'book','0010_rename_id_appointment_appointment_id','2024-03-16 05:41:00.244927');
INSERT INTO "django_migrations" VALUES (31,'book','0011_test_information_and_more','2024-03-16 05:41:00.267971');
INSERT INTO "django_migrations" VALUES (32,'book','0012_user_is_secretary_secretary','2024-03-16 05:41:00.294227');
INSERT INTO "django_migrations" VALUES (33,'book','0013_secretary_address_secretary_patients_of_the_day_and_more','2024-03-16 05:41:00.346677');
INSERT INTO "django_migrations" VALUES (34,'book','0014_remove_secretary_patients_of_the_day','2024-03-16 05:41:00.363722');
INSERT INTO "django_migrations" VALUES (35,'book','0015_secretary_appointment','2024-03-16 05:41:00.382513');
INSERT INTO "django_migrations" VALUES (36,'book','0016_remove_patientexit_patient_and_more','2024-03-16 05:41:00.414844');
INSERT INTO "django_migrations" VALUES (37,'book','0017_remove_prescription_days_and_more','2024-03-16 05:41:00.547868');
INSERT INTO "django_migrations" VALUES (38,'book','0018_remove_prescription_prescription_medecine_and_more','2024-03-16 05:41:00.626869');
INSERT INTO "django_migrations" VALUES (39,'book','0019_alter_prescription_medicine_prescription_and_more','2024-03-16 05:41:00.654973');
INSERT INTO "django_migrations" VALUES (40,'book','0020_remove_prescription_medicine_prescription_and_more','2024-03-16 05:41:00.784833');
INSERT INTO "django_migrations" VALUES (41,'book','0021_test_information_remove_prescription_end_day_and_more','2024-03-16 05:41:00.848043');
INSERT INTO "django_migrations" VALUES (42,'book','0022_rename_date_of_bird_doctor_date_of_birth_and_more','2024-03-16 05:41:00.887688');
INSERT INTO "django_migrations" VALUES (43,'book','0023_prescription_medicine_dosage_and_more','2024-03-16 05:41:00.901725');
INSERT INTO "django_migrations" VALUES (44,'book','0024_remove_secretary_appointment','2024-03-16 05:41:00.922913');
INSERT INTO "django_migrations" VALUES (45,'sessions','0001_initial','2024-03-16 05:41:00.932951');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (5,'sessions','session');
INSERT INTO "django_content_type" VALUES (6,'book','user');
INSERT INTO "django_content_type" VALUES (7,'book','admin');
INSERT INTO "django_content_type" VALUES (8,'book','hospital');
INSERT INTO "django_content_type" VALUES (9,'book','specialization');
INSERT INTO "django_content_type" VALUES (10,'book','patient');
INSERT INTO "django_content_type" VALUES (11,'book','doctor');
INSERT INTO "django_content_type" VALUES (12,'book','doctortimeslots');
INSERT INTO "django_content_type" VALUES (13,'book','appointment');
INSERT INTO "django_content_type" VALUES (14,'book','prescription');
INSERT INTO "django_content_type" VALUES (15,'book','secretary');
INSERT INTO "django_content_type" VALUES (16,'book','test_information');
INSERT INTO "django_content_type" VALUES (17,'book','prescription_medicine');
INSERT INTO "django_content_type" VALUES (18,'book','prescription_test');
INSERT INTO "django_content_type" VALUES (19,'authtoken','token');
INSERT INTO "django_content_type" VALUES (20,'authtoken','tokenproxy');
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (21,6,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (22,6,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (23,6,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (24,6,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (25,7,'add_admin','Can add admin');
INSERT INTO "auth_permission" VALUES (26,7,'change_admin','Can change admin');
INSERT INTO "auth_permission" VALUES (27,7,'delete_admin','Can delete admin');
INSERT INTO "auth_permission" VALUES (28,7,'view_admin','Can view admin');
INSERT INTO "auth_permission" VALUES (29,8,'add_hospital','Can add hospital');
INSERT INTO "auth_permission" VALUES (30,8,'change_hospital','Can change hospital');
INSERT INTO "auth_permission" VALUES (31,8,'delete_hospital','Can delete hospital');
INSERT INTO "auth_permission" VALUES (32,8,'view_hospital','Can view hospital');
INSERT INTO "auth_permission" VALUES (33,9,'add_specialization','Can add specialization');
INSERT INTO "auth_permission" VALUES (34,9,'change_specialization','Can change specialization');
INSERT INTO "auth_permission" VALUES (35,9,'delete_specialization','Can delete specialization');
INSERT INTO "auth_permission" VALUES (36,9,'view_specialization','Can view specialization');
INSERT INTO "auth_permission" VALUES (37,10,'add_patient','Can add patient');
INSERT INTO "auth_permission" VALUES (38,10,'change_patient','Can change patient');
INSERT INTO "auth_permission" VALUES (39,10,'delete_patient','Can delete patient');
INSERT INTO "auth_permission" VALUES (40,10,'view_patient','Can view patient');
INSERT INTO "auth_permission" VALUES (41,11,'add_doctor','Can add doctor');
INSERT INTO "auth_permission" VALUES (42,11,'change_doctor','Can change doctor');
INSERT INTO "auth_permission" VALUES (43,11,'delete_doctor','Can delete doctor');
INSERT INTO "auth_permission" VALUES (44,11,'view_doctor','Can view doctor');
INSERT INTO "auth_permission" VALUES (45,12,'add_doctortimeslots','Can add doctor time slots');
INSERT INTO "auth_permission" VALUES (46,12,'change_doctortimeslots','Can change doctor time slots');
INSERT INTO "auth_permission" VALUES (47,12,'delete_doctortimeslots','Can delete doctor time slots');
INSERT INTO "auth_permission" VALUES (48,12,'view_doctortimeslots','Can view doctor time slots');
INSERT INTO "auth_permission" VALUES (49,13,'add_appointment','Can add appointment');
INSERT INTO "auth_permission" VALUES (50,13,'change_appointment','Can change appointment');
INSERT INTO "auth_permission" VALUES (51,13,'delete_appointment','Can delete appointment');
INSERT INTO "auth_permission" VALUES (52,13,'view_appointment','Can view appointment');
INSERT INTO "auth_permission" VALUES (53,14,'add_prescription','Can add prescription');
INSERT INTO "auth_permission" VALUES (54,14,'change_prescription','Can change prescription');
INSERT INTO "auth_permission" VALUES (55,14,'delete_prescription','Can delete prescription');
INSERT INTO "auth_permission" VALUES (56,14,'view_prescription','Can view prescription');
INSERT INTO "auth_permission" VALUES (57,15,'add_secretary','Can add secretary');
INSERT INTO "auth_permission" VALUES (58,15,'change_secretary','Can change secretary');
INSERT INTO "auth_permission" VALUES (59,15,'delete_secretary','Can delete secretary');
INSERT INTO "auth_permission" VALUES (60,15,'view_secretary','Can view secretary');
INSERT INTO "auth_permission" VALUES (61,16,'add_test_information','Can add test_ information');
INSERT INTO "auth_permission" VALUES (62,16,'change_test_information','Can change test_ information');
INSERT INTO "auth_permission" VALUES (63,16,'delete_test_information','Can delete test_ information');
INSERT INTO "auth_permission" VALUES (64,16,'view_test_information','Can view test_ information');
INSERT INTO "auth_permission" VALUES (65,17,'add_prescription_medicine','Can add prescription_medicine');
INSERT INTO "auth_permission" VALUES (66,17,'change_prescription_medicine','Can change prescription_medicine');
INSERT INTO "auth_permission" VALUES (67,17,'delete_prescription_medicine','Can delete prescription_medicine');
INSERT INTO "auth_permission" VALUES (68,17,'view_prescription_medicine','Can view prescription_medicine');
INSERT INTO "auth_permission" VALUES (69,18,'add_prescription_test','Can add prescription_test');
INSERT INTO "auth_permission" VALUES (70,18,'change_prescription_test','Can change prescription_test');
INSERT INTO "auth_permission" VALUES (71,18,'delete_prescription_test','Can delete prescription_test');
INSERT INTO "auth_permission" VALUES (72,18,'view_prescription_test','Can view prescription_test');
INSERT INTO "auth_permission" VALUES (73,19,'add_token','Can add Token');
INSERT INTO "auth_permission" VALUES (74,19,'change_token','Can change Token');
INSERT INTO "auth_permission" VALUES (75,19,'delete_token','Can delete Token');
INSERT INTO "auth_permission" VALUES (76,19,'view_token','Can view Token');
INSERT INTO "auth_permission" VALUES (77,20,'add_tokenproxy','Can add token');
INSERT INTO "auth_permission" VALUES (78,20,'change_tokenproxy','Can change token');
INSERT INTO "auth_permission" VALUES (79,20,'delete_tokenproxy','Can delete token');
INSERT INTO "auth_permission" VALUES (80,20,'view_tokenproxy','Can view token');
INSERT INTO "django_admin_log" VALUES (1,'2','dom.tessier@sgm.com',1,'[{"added": {}}]',6,1,'2024-03-16 05:57:02.238205');
INSERT INTO "django_admin_log" VALUES (2,'2','dom.tessier@sgm.com',2,'[{"changed": {"fields": ["Is doctor"]}}]',6,1,'2024-03-16 05:57:08.827207');
INSERT INTO "django_admin_log" VALUES (3,'1','SGM Lille',1,'[{"added": {}}]',8,1,'2024-03-16 06:01:22.330088');
INSERT INTO "django_admin_log" VALUES (4,'1','Neurologie - SGM Lille',1,'[{"added": {}}]',9,1,'2024-03-16 06:01:48.517566');
INSERT INTO "django_admin_log" VALUES (5,'2','Orthopédie - SGM Lille',1,'[{"added": {}}]',9,1,'2024-03-16 06:02:02.549561');
INSERT INTO "django_admin_log" VALUES (6,'2','Orthopédie - SGM Lille',2,'[]',9,1,'2024-03-16 06:02:14.068661');
INSERT INTO "django_admin_log" VALUES (7,'3','Dentaire - SGM Lille',1,'[{"added": {}}]',9,1,'2024-03-16 06:02:16.994667');
INSERT INTO "django_admin_log" VALUES (8,'4','Cardiologie - SGM Lille',1,'[{"added": {}}]',9,1,'2024-03-16 06:02:30.361385');
INSERT INTO "django_admin_log" VALUES (9,'5','Urologie - SGM Lille',1,'[{"added": {}}]',9,1,'2024-03-16 06:02:39.839199');
INSERT INTO "django_admin_log" VALUES (10,'1','dom.tessier@sgm.com',1,'[{"added": {}}]',11,1,'2024-03-16 06:03:36.180643');
INSERT INTO "django_admin_log" VALUES (11,'3','claude.grosjean@sgm.com',1,'[{"added": {}}]',6,1,'2024-03-16 06:07:34.626545');
INSERT INTO "django_admin_log" VALUES (12,'3','claude.grosjean@sgm.com',2,'[{"changed": {"fields": ["Is doctor"]}}]',6,1,'2024-03-16 06:07:41.680678');
INSERT INTO "django_admin_log" VALUES (13,'2','claude.grosjean@sgm.com',1,'[{"added": {}}]',11,1,'2024-03-16 06:08:17.235651');
INSERT INTO "django_admin_log" VALUES (14,'4','sebastien.vespasien@sgm.com',1,'[{"added": {}}]',6,1,'2024-03-16 06:10:09.480288');
INSERT INTO "django_admin_log" VALUES (15,'4','sebastien.vespasien@sgm.com',2,'[{"changed": {"fields": ["Is doctor"]}}]',6,1,'2024-03-16 06:10:13.839034');
INSERT INTO "django_admin_log" VALUES (16,'3','sebastien.vespasien@sgm.com',1,'[{"added": {}}]',11,1,'2024-03-16 06:11:00.827335');
INSERT INTO "django_admin_log" VALUES (17,'5','giselle.dujardin@sgm.com',1,'[{"added": {}}]',6,1,'2024-03-16 06:12:46.038648');
INSERT INTO "django_admin_log" VALUES (18,'5','giselle.dujardin@sgm.com',2,'[{"changed": {"fields": ["Is secretary"]}}]',6,1,'2024-03-16 06:12:50.851706');
INSERT INTO "django_admin_log" VALUES (19,'1','giselle.dujardin@sgm.com',1,'[{"added": {}}]',15,1,'2024-03-16 06:13:45.549572');
INSERT INTO "django_admin_log" VALUES (20,'6','jacqueline.moreno@sgm.com',1,'[{"added": {}}]',6,1,'2024-03-16 06:16:05.112353');
INSERT INTO "django_admin_log" VALUES (21,'6','jacqueline.moreno@sgm.com',2,'[{"changed": {"fields": ["Is secretary"]}}]',6,1,'2024-03-16 06:16:10.956849');
INSERT INTO "django_admin_log" VALUES (22,'2','jacqueline.moreno@sgm.com',1,'[{"added": {}}]',15,1,'2024-03-16 06:16:58.035710');
INSERT INTO "django_admin_log" VALUES (23,'7','paulette.vasseur@sgm.com',1,'[{"added": {}}]',6,1,'2024-03-16 06:19:08.846125');
INSERT INTO "django_admin_log" VALUES (24,'4','paulette.vasseur@sgm.com',1,'[{"added": {}}]',11,1,'2024-03-16 06:20:01.060572');
INSERT INTO "django_admin_log" VALUES (25,'8','michelle.delaunay@sgmc.com',1,'[{"added": {}}]',6,1,'2024-03-16 06:22:49.747015');
INSERT INTO "django_admin_log" VALUES (26,'5','michelle.delaunay@sgmc.com',1,'[{"added": {}}]',11,1,'2024-03-16 06:23:42.214091');
INSERT INTO "django_admin_log" VALUES (27,'1','Dominique.  Consulting Date: from 2024-03-16 to 2024-03-24',1,'[{"added": {}}]',12,1,'2024-03-16 06:29:08.806635');
INSERT INTO "django_admin_log" VALUES (28,'2','Dominique.  Consulting Date: from 2024-03-29 to 2024-04-03',1,'[{"added": {}}]',12,1,'2024-03-16 06:29:31.072518');
INSERT INTO "django_admin_log" VALUES (29,'3','Dominique.  Consulting Date: from 2024-04-15 to 2024-04-21',1,'[{"added": {}}]',12,1,'2024-03-16 06:29:52.426752');
INSERT INTO "django_admin_log" VALUES (30,'4','Claude.  Consulting Date: from 2024-03-20 to 2024-03-25',1,'[{"added": {}}]',12,1,'2024-03-16 06:30:10.345806');
INSERT INTO "django_admin_log" VALUES (31,'5','Claude.  Consulting Date: from 2024-03-28 to 2024-04-14',1,'[{"added": {}}]',12,1,'2024-03-16 06:30:31.891822');
INSERT INTO "django_admin_log" VALUES (32,'6','Sebastien.  Consulting Date: from 2024-03-17 to 2024-03-31',1,'[{"added": {}}]',12,1,'2024-03-16 06:30:58.229761');
INSERT INTO "django_admin_log" VALUES (33,'6','Sebastien.  Consulting Date: from 2024-03-17 to 2024-03-31',2,'[]',12,1,'2024-03-16 06:31:07.907690');
INSERT INTO "django_admin_log" VALUES (34,'7','Sebastien.  Consulting Date: from 2024-04-08 to 2024-04-17',1,'[{"added": {}}]',12,1,'2024-03-16 06:31:21.298506');
INSERT INTO "django_admin_log" VALUES (35,'7','Sebastien.  Consulting Date: from 2024-04-08 to 2024-04-17',2,'[]',12,1,'2024-03-16 06:31:22.352719');
INSERT INTO "django_admin_log" VALUES (36,'8','Paulette.  Consulting Date: from 2024-03-23 to 2024-03-31',1,'[{"added": {}}]',12,1,'2024-03-16 06:31:33.669442');
INSERT INTO "django_admin_log" VALUES (37,'8','Paulette.  Consulting Date: from 2024-03-23 to 2024-03-31',2,'[]',12,1,'2024-03-16 06:31:35.194805');
INSERT INTO "django_admin_log" VALUES (38,'9','Paulette.  Consulting Date: from 2024-04-15 to 2024-04-29',1,'[{"added": {}}]',12,1,'2024-03-16 06:31:51.669529');
INSERT INTO "django_admin_log" VALUES (39,'9','Michelle.  Consulting Date: from 2024-03-18 to 2024-03-23',2,'[{"changed": {"fields": ["Doctor", "Doc start date", "Doc end date"]}}]',12,1,'2024-03-16 06:32:21.513397');
INSERT INTO "django_admin_log" VALUES (40,'9','Michelle.  Consulting Date: from 2024-03-18 to 2024-03-23',2,'[]',12,1,'2024-03-16 06:32:23.853381');
INSERT INTO "django_admin_log" VALUES (41,'10','Michelle.  Consulting Date: from 2024-03-25 to 2024-03-30',1,'[{"added": {}}]',12,1,'2024-03-16 06:32:34.338528');
INSERT INTO "authtoken_token" VALUES ('7d06b25ac565ed0d528f3c3e2e25be7522b88d5f','2024-03-16 06:04:49.383205',2);
INSERT INTO "book_hospital" VALUES (1,'SGM Lille','125 Bl du Générale de Gaulle 59800 Lille','hospitals/H1_3QKe8Wz.jpg','Hôpital du groupe hospitalier SGM','lille@sgm.com','0123451234');
INSERT INTO "book_specialization" VALUES (1,'Neurologie',1);
INSERT INTO "book_specialization" VALUES (2,'Orthopédie',1);
INSERT INTO "book_specialization" VALUES (3,'Dentaire',1);
INSERT INTO "book_specialization" VALUES (4,'Cardiologie',1);
INSERT INTO "book_specialization" VALUES (5,'Urologie',1);
INSERT INTO "book_doctor" VALUES (1,'Dominique','Tessier','0123451231',1,1,2,'1981-09-26','94UD7J');
INSERT INTO "book_doctor" VALUES (2,'Claude','Grosjean','0123451232',1,2,3,'1970-09-21','IZ2ECM');
INSERT INTO "book_doctor" VALUES (3,'Sebastien','Vespasien','0123451233',1,3,4,'2001-01-05','3QU0MX');
INSERT INTO "book_doctor" VALUES (4,'Paulette','Vasseur','0123451234',1,4,7,'1995-03-13','XO12U0');
INSERT INTO "book_doctor" VALUES (5,'Michelle','Delaunay','0123451235',1,5,8,'1979-09-08','HOU1LF');
INSERT INTO "book_patient" VALUES (1,'Victor','Devos','0600000001','7 Avenue du Chatelier 59000 Lille','#PTGN3718',9,'1974-08-01');
INSERT INTO "book_doctortimeslots" VALUES (1,'2024-03-16','2024-03-24',1);
INSERT INTO "book_doctortimeslots" VALUES (2,'2024-03-29','2024-04-03',1);
INSERT INTO "book_doctortimeslots" VALUES (3,'2024-04-15','2024-04-21',1);
INSERT INTO "book_doctortimeslots" VALUES (4,'2024-03-20','2024-03-25',2);
INSERT INTO "book_doctortimeslots" VALUES (5,'2024-03-28','2024-04-14',2);
INSERT INTO "book_doctortimeslots" VALUES (6,'2024-03-17','2024-03-31',3);
INSERT INTO "book_doctortimeslots" VALUES (7,'2024-04-08','2024-04-17',3);
INSERT INTO "book_doctortimeslots" VALUES (8,'2024-03-23','2024-03-31',4);
INSERT INTO "book_doctortimeslots" VALUES (9,'2024-03-18','2024-03-23',5);
INSERT INTO "book_doctortimeslots" VALUES (10,'2024-03-25','2024-03-30',5);
INSERT INTO "book_appointment" VALUES (1,'2024-03-16','2024-03-24','','#PTZW5DTS',NULL,1,NULL,1);
INSERT INTO "book_user" VALUES (1,'pbkdf2_sha256$720000$ZgvQS9PJasofJPV8DPIcb4$m8LOdTQ5P9uPrebWbPVzIrqRUb9E1TCA+JSCZM1B2LY=','2024-03-16 06:28:38.500199',1,'','',1,1,'2024-03-16 05:51:16.191483','admin@sgm.com',1,0,0,0,0);
INSERT INTO "book_user" VALUES (2,'pbkdf2_sha256$720000$QDyTBpkvvgF8x5CdDRSOQr$mGVat8yW9ZuL4+F4FYV1jYe947CmhaGk0RWKiCfqS0w=',NULL,0,'','',0,1,'2024-03-16 05:57:02','dom.tessier@sgm.com',0,0,0,1,0);
INSERT INTO "book_user" VALUES (3,'pbkdf2_sha256$720000$d2ZQQy0Y79tQhN9nkHP9EQ$DBHL2vHR9EBfh6uIX3A+59FenGVYZXkfc5ZbGZ1hUgs=',NULL,0,'','',0,1,'2024-03-16 06:07:34','claude.grosjean@sgm.com',0,0,0,1,0);
INSERT INTO "book_user" VALUES (4,'pbkdf2_sha256$720000$0iIc0Gm034QZ6vAEYWWPOv$x29yfaLEBE5c4h6DugdIlsxsOYHq/uemNBGAVGI00pQ=',NULL,0,'','',0,1,'2024-03-16 06:10:09','sebastien.vespasien@sgm.com',0,0,0,1,0);
INSERT INTO "book_user" VALUES (5,'pbkdf2_sha256$720000$ok7La4BkW6EqObKdnSPgA0$vcLKsyCThgmF/CHsFzSxzl17Fz//YgyQPb/pgIz8uVY=',NULL,0,'','',0,1,'2024-03-16 06:12:45','giselle.dujardin@sgm.com',0,0,0,0,1);
INSERT INTO "book_user" VALUES (6,'pbkdf2_sha256$720000$d8KucFWj7Bxe0McL1B4Xub$0NlC7EREXmLSG5x54Z0IZMCLVeBF0l/s/P25eN/2nYA=',NULL,0,'','',0,1,'2024-03-16 06:16:04','jacqueline.moreno@sgm.com',0,0,0,0,1);
INSERT INTO "book_user" VALUES (7,'pbkdf2_sha256$720000$bk2Dep1rLQzsvYDM3Km374$3nSjH6evOuebID3uCzXh9n/7AeUN1xY7ZKuOUoLrKEo=',NULL,0,'','',0,1,'2024-03-16 06:19:08.624905','paulette.vasseur@sgm.com',0,0,0,0,0);
INSERT INTO "book_user" VALUES (8,'pbkdf2_sha256$720000$tYHAGrzcZCGXKCCYoeMbWe$Dzhe/qvRrN4AjN7kT/68uJ/NXbvNEI0DnzgZkA3Lmc4=',NULL,0,'','',0,1,'2024-03-16 06:22:49.518980','michelle.delaunay@sgmc.com',0,0,0,0,0);
INSERT INTO "book_user" VALUES (9,'pbkdf2_sha256$720000$5mGdnNiqTPxwXnnvg8Mpa0$i2Xymp4qkGlrkGLOe6nk+yA/ZPnYmCDBrrETLtsRV/g=','2024-03-16 06:33:49.966509',0,'Victor','Devos',0,1,'2024-03-16 06:26:20.597359','vic.devos@gmail.com',0,1,0,0,0);
INSERT INTO "book_secretary" VALUES (1,'Giselle','Dujardin','0123451200','914ML3',1,5,'2 Rue de la Guerche 59000 Lille','1988-07-28');
INSERT INTO "book_secretary" VALUES (2,'Jacqueline','Moreno','0123451200','2OUV59',1,6,'18 Rue du Moulin Guibreteau 59000 Lille','1996-11-18');
INSERT INTO "django_session" VALUES ('alwhuwvotl893bq8warnsssu4kas7192','.eJxVjDkOwjAUBe_iGlnxGpuSnjNEf7FxANlSnFSIu0OkFNC-mXkvMcG2lmnraZlmFmcRxel3Q6BHqjvgO9Rbk9Tquswod0UetMtr4_S8HO7fQYFevjUathmdsjo4DxGDsg5jzor9EFNwhMzBGE9IxAR2tDgoIjdq0HrIQbw_9jo4YQ:1rlNd2:GZhGdShvWZSfi3sVpWjP3_ws0G4f4WN3ybDNYSkhs-Q','2024-03-16 07:04:48.996622');
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "book_user_groups_user_id_group_id_215796e1_uniq" ON "book_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "book_user_groups_user_id_b7d49bd2" ON "book_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "book_user_groups_group_id_42a87701" ON "book_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "book_user_user_permissions_user_id_permission_id_c0874424_uniq" ON "book_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "book_user_user_permissions_user_id_0a2af966" ON "book_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "book_user_user_permissions_permission_id_7cb10e82" ON "book_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "book_specialization_hospital_id_c3791b15" ON "book_specialization" (
	"hospital_id"
);
CREATE INDEX IF NOT EXISTS "book_doctor_hospital_name_id_32df9148" ON "book_doctor" (
	"hospital_name_id"
);
CREATE INDEX IF NOT EXISTS "book_doctor_specialization_id_b24e2698" ON "book_doctor" (
	"specialization_id"
);
CREATE INDEX IF NOT EXISTS "book_doctortimeslots_doctor_id_a682e91b" ON "book_doctortimeslots" (
	"doctor_id"
);
CREATE INDEX IF NOT EXISTS "book_appointment_choise_speciality_id_8ebd2e1e" ON "book_appointment" (
	"choise_speciality_id"
);
CREATE INDEX IF NOT EXISTS "book_appointment_doctor_id_aecd7104" ON "book_appointment" (
	"doctor_id"
);
CREATE INDEX IF NOT EXISTS "book_appointment_doctor_time_slots_id_a69cb8a3" ON "book_appointment" (
	"doctor_time_slots_id"
);
CREATE INDEX IF NOT EXISTS "book_appointment_patient_id_609278de" ON "book_appointment" (
	"patient_id"
);
CREATE INDEX IF NOT EXISTS "book_prescription_doctor_id_ae74ac21" ON "book_prescription" (
	"doctor_id"
);
CREATE INDEX IF NOT EXISTS "book_prescription_patient_id_63cade43" ON "book_prescription" (
	"patient_id"
);
CREATE INDEX IF NOT EXISTS "book_prescription_medicine_prescription_id_fc8a2aa5" ON "book_prescription_medicine" (
	"prescription_id"
);
CREATE INDEX IF NOT EXISTS "book_prescription_test_prescription_id_75f0910a" ON "book_prescription_test" (
	"prescription_id"
);
CREATE INDEX IF NOT EXISTS "book_secretary_hospital_name_id_6b171627" ON "book_secretary" (
	"hospital_name_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
COMMIT;