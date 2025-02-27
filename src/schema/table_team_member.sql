CREATE TABLE team_member (
    -- Identity column for primary key
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- Name-related fields
    given_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    full_name TEXT NOT NULL,
    preferred_name TEXT,
    
    -- System fields
    preferred_system_username TEXT UNIQUE,
    preferred_pronouns TEXT,
    
    -- Visibility control
    public_visibility INTEGER,
    
    -- Timestamp tracking
    datetime_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);