-- Table: users
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY NOT NULL,
    username VARCHAR(32) DEFAULT NULL,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    subscription_end_date DATE DEFAULT DATE '1970-01-01',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table: vpn_configs
CREATE TABLE vpn_configs (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    config_name VARCHAR(32) NOT NULL,
    config_uuid VARCHAR(64) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table: bonus_configs_for_users
CREATE TABLE bonus_configs_for_users (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(user_id),
    bonus_config_count INTEGER NOT NULL DEFAULT 0
);
