CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    joined DATE,
    general_goal INTEGER,
    weekly_goal INTEGER,
    notifications_learn INTEGER,
    notifications_stats INTEGER

);

CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    privacy INTEGER,
    founder INTEGER REFERENCES users.user_id
);

CREATE TABLE packs (
    pack_id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users.user_id,
    privacy INTEGER

);

CREATE TABLE cards (
    card_id SERIAL PRIMARY KEY,
    pack_id INTEGER REFERENCES packs.pack_id,
    front TEXT NOT NULL,
    back TEXT,
    comment TEXT

);

CREATE TABLE user_groups (
    group_id INTEGER REFERENCES groups.group_id,
    user_id INTEGER REFERENCES users.user_id
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE user_packs (
    pack_id INTEGER REFERENCES packs.pack_id,
    user_id INTEGER REFERENCES users.user_id,
    status INTEGER NOT NULL,
    last_visited DATE,
    to_be_learned_until DATE,
    learned DATE
    PRIMARY KEY (pack_id, user_id)
);

CREATE TABLE user_cards (
    user_id INTEGER REFERENCES users.user_id,
    card_id INTEGER REFERENCES cards.card_id,
    times_reviewed INTEGER,
    correct_answers INTEGER,
    status INTEGER

    PRIMARY KEY (user_id, card_id)
);

CREATE TABLE group_packs (
    group_id INTEGER REFERENCES groups.group_id,
    pack_id INTEGER REFERENCES packs.pack_id,
    status INTEGER

    PRIMARY KEY (group_id, pack_id)
);

CREATE TABLE editing_rights (
    group_id INTEGER REFERENCES groups.group_id,
    user_id INTEGER REFERENCES users.user_id
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE access_rights (
    group_id INTEGER REFERENCES groups.group_id,
    user_id INTEGER REFERENCES users.user_id
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE group_invitations ( -- заявки от пользователей на вступление в группы
    group_id INTEGER REFERENCES groups.group_id,
    user_id INTEGER REFERENCES users.user_id
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE user_invitations ( -- приглашения пользователям
    group_id INTEGER REFERENCES groups.group_id,
    user_id INTEGER REFERENCES users.user_id
    PRIMARY KEY (group_id, user_id)
);