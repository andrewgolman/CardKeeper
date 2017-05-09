-- TODO: UNIFY CAPITALIZATION IN ENUMS
CREATE TYPE GEN_GOAL_TYPE AS ENUM ('Science', 'Speech', 'Belletristic');
CREATE TYPE NOTIFICATION_TYPE AS ENUM ('Twice a day', 'Daily', 'Weekly', 'Never');
CREATE TYPE PRIVACY_TYPE AS ENUM ('private', 'protected',  'public');
CREATE TYPE CARD_STATUS_TYPE AS ENUM ('Active', 'Reserved', 'Not ready', 'Deprecated', 'Learned');
CREATE TYPE RIGHTS_TYPE AS ENUM ('admin', 'user');
CREATE TYPE INVITATION_TYPE AS ENUM ('from a group', 'from a user');
CREATE TYPE CARD_TYPE AS ENUM ('Short', 'Construction', 'Sentence');

CREATE TABLE users (
    user_id 			        INTEGER 		PRIMARY KEY,
    name 				          VARCHAR(30) 	NOT NULL UNIQUE,
    joined 			          DATE			NOT NULL,
    general_goal          GEN_GOAL_TYPE,
    weekly_goal 	        INTEGER 		NOT NULL,
    notifications_learn 	NOTIFICATION_TYPE,
    notifications_stats 	NOTIFICATION_TYPE
);

CREATE TABLE groups (
    group_id 	  SERIAL 		PRIMARY KEY,
    name 		    VARCHAR(50) 	NOT NULL UNIQUE,
    privacy 	  PRIVACY_TYPE 	NOT NULL,
    founder 	  INTEGER 		REFERENCES users (user_id)
);

CREATE TABLE packs (
    pack_id 	SERIAL 	PRIMARY KEY,
    name      VARCHAR(30) NOT NULL UNIQUE,
    owner_id 	INTEGER 	REFERENCES users (user_id),
    privacy 	PRIVACY_TYPE
);

CREATE TABLE cards (
    card_id 	SERIAL 	PRIMARY KEY,
    pack_id 	INTEGER 	REFERENCES packs (pack_id),
    front 		TEXT 		NOT NULL,
    back 		  TEXT,
    comment     TEXT,
    type      CARD_TYPE
);

CREATE TABLE user_groups (
    group_id 	INTEGER 	REFERENCES groups (group_id),
    user_id 	INTEGER 	REFERENCES users (user_id),
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE user_packs (
    pack_id 		  INTEGER 			REFERENCES packs (pack_id),
    user_id 		  INTEGER 			REFERENCES users (user_id),
    status 		    CARD_STATUS_TYPE 	NOT NULL,
    last_visited 	DATE,
    to_be_learned_until DATE,
    learned 		  DATE,
    PRIMARY KEY (pack_id, user_id)
);

CREATE TABLE user_cards (
    user_id 		      INTEGER 		REFERENCES users (user_id),
    card_id 		      INTEGER 		REFERENCES cards (card_id),
    times_reviewed 	  INTEGER 		NOT NULL,
    correct_answers 	INTEGER 		NOT NULL CHECK (correct_answers <= times_reviewed),
    status 		CARD_STATUS_TYPE NOT NULL,
    PRIMARY KEY (user_id, card_id)
);

CREATE TABLE group_packs (
    group_id 		INTEGER 			REFERENCES groups (group_id),
    pack_id 		INTEGER 			REFERENCES packs (pack_id),
    status 		CARD_STATUS_TYPE 	NOT NULL,
    PRIMARY KEY (group_id, pack_id)
);

CREATE TABLE rights ( -- editing (all packs) and access (private packs)
    group_id 	INTEGER 		REFERENCES groups (group_id),
    user_id	INTEGER 		REFERENCES users (user_id),
    rights 	RIGHTS_TYPE 	NOT NULL,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE access_rights (
    group_id 	INTEGER 	REFERENCES groups (group_id),
    user_id 	INTEGER 	REFERENCES users (user_id),
    PRIMARY KEY (group_id, user_id)
);
