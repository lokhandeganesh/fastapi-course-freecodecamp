-- Enable citext once per DB
CREATE EXTENSION IF NOT EXISTS citext;

CREATE SCHEMA IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.user_account (
  id            BIGSERIAL PRIMARY KEY,
  email         CITEXT UNIQUE NOT NULL,
  password_h    TEXT NOT NULL,                     -- argon2/bcrypt hash
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Optional: refresh tokens if you don’t want Redis
CREATE TABLE IF NOT EXISTS auth.refresh_token (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT NOT NULL REFERENCES auth.user_account(id) ON DELETE CASCADE,
  token_h      TEXT NOT NULL,                      -- store a hash of the refresh token
  expires_at   TIMESTAMPTZ NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  revoked      BOOLEAN NOT NULL DEFAULT FALSE
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_user_created_at ON auth.user_account(created_at);
CREATE INDEX IF NOT EXISTS idx_refresh_user_expires ON auth.refresh_token(user_id, expires_at);