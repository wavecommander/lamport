CREATE TABLE personal_info_fragment (
    -- Primary key using identity column
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Foreign key to team_member table
    team_member_id BIGINT NOT NULL,
    
    -- Personal info type with check constraint
    personal_info_type TEXT NOT NULL CHECK (
        personal_info_type IN (
            'email',
            'phone_number',
            'address',
            'organization',
            'title',
            'image_src',
            'url',
            'other'
        )
    ),
    
    -- Personal info value
    personal_info_value TEXT NOT NULL,
    
    -- Visibility control
    public_visibility INTEGER,
    
    -- Timestamp tracking
    datetime_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT fk_team_member FOREIGN KEY (team_member_id)
        REFERENCES team_member(id)
        ON DELETE CASCADE
);