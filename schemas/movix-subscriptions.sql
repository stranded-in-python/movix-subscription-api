CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS subscriptions;

CREATE TYPE Currency As ENUM (
    'RUB'
);

CREATE TYPE SubscriptionStatus As ENUM (
    'active',
    'inactive',
    'pending',
    'blocked'
);

CREATE TABLE IF NOT EXISTS subscriptions.subscription(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255),
    is_deleted boolean
);

CREATE TABLE IF NOT EXISTS subscriptions.tariff(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    subscription_id uuid REFERENCES subscriptions.subscription(id),
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    duration bigint,
    amount decimal(14,2),
    currency Currency
);

CREATE TABLE IF NOT EXISTS subscriptions.subscription_account(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP,
    modified_at TIMESTAMP,
    subscription_id uuid REFERENCES subscriptions.subscription(id),
    user_id uuid NOT NULL,
    tariff_id uuid REFERENCES subscriptions.tariff(id),
    status SubscriptionStatus,
    expires_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscriptions.account_status(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id uuid REFERENCES subscriptions.account(id),
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    status SubscriptionStatus,
    responsible_for uuid
);
