CREATE TABLE form_submission (
    -- Primary key using identity column
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Foreign key to team_member table for submitter
    submitter BIGINT NOT NULL,
    
    -- Status field for tracking submission state
    status INTEGER,
    
    -- Foreign key to team_member table for reviewer (nullable)
    reviewer BIGINT,
    
    -- Timestamp tracking
    datetime_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_submitter FOREIGN KEY (submitter)
        REFERENCES team_member(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reviewer FOREIGN KEY (reviewer)
        REFERENCES team_member(id)
        ON DELETE SET NULL
);