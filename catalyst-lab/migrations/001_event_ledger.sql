BEGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TYPE catalyst_type AS ENUM ('earnings_guidance','government_contracts','drug_trials_approvals','ipos','uk_announcements','economic_releases');
CREATE TABLE source_documents (
 source_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), provider text NOT NULL,
 source_url text, source_identifier text, published_at timestamptz,
 ingested_at timestamptz NOT NULL DEFAULT now(), content_sha256 text NOT NULL,
 raw_object_uri text, licence_status text NOT NULL DEFAULT 'unverified',
 UNIQUE(provider,content_sha256)
);
CREATE TABLE securities (
 security_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), ticker text NOT NULL,
 company text NOT NULL, exchange text NOT NULL, country text, sector text,
 industry text, currency text, active_from date, active_to date,
 UNIQUE(ticker,exchange,active_from)
);
CREATE TABLE events (
 event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), event_type catalyst_type NOT NULL,
 event_subtype text NOT NULL, security_id uuid REFERENCES securities,
 event_timestamp timestamptz, announcement_timestamp timestamptz,
 market_session text CHECK(market_session IN ('before_open','regular','after_close','non_trading','unknown')),
 source_id uuid NOT NULL REFERENCES source_documents, attributes jsonb NOT NULL DEFAULT '{}',
 quality_flags jsonb NOT NULL DEFAULT '[]', created_at timestamptz NOT NULL DEFAULT now(),
 supersedes_event_id uuid REFERENCES events
);
CREATE TABLE market_bars (
 security_id uuid NOT NULL REFERENCES securities, bar_timestamp timestamptz NOT NULL,
 interval text NOT NULL, adjustment text NOT NULL, open numeric NOT NULL CHECK(open>0),
 high numeric NOT NULL, low numeric NOT NULL, close numeric NOT NULL CHECK(close>0),
 volume numeric CHECK(volume>=0), source_id uuid NOT NULL REFERENCES source_documents,
 PRIMARY KEY(security_id,bar_timestamp,interval,adjustment,source_id),
 CHECK(high>=low AND high>=open AND high>=close AND low<=open AND low<=close)
);
CREATE TABLE feature_snapshots (
 snapshot_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), event_id uuid NOT NULL REFERENCES events,
 prediction_cutoff timestamptz NOT NULL, dataset_version text NOT NULL,
 code_version text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE feature_values (
 snapshot_id uuid NOT NULL REFERENCES feature_snapshots, feature_name text NOT NULL,
 value jsonb, classification text NOT NULL CHECK(classification IN ('reported_fact','consensus','guidance','interpretation','assumption')),
 observed_at timestamptz, published_at timestamptz, ingested_at timestamptz NOT NULL,
 effective_at timestamptz, source_id uuid REFERENCES source_documents,
 available_at timestamptz NOT NULL, quality_flags jsonb NOT NULL DEFAULT '[]',
 PRIMARY KEY(snapshot_id,feature_name),
 CHECK(published_at IS NULL OR available_at>=published_at),
 CHECK(available_at>=ingested_at)
);
CREATE FUNCTION enforce_feature_cutoff() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.available_at > (SELECT prediction_cutoff FROM feature_snapshots WHERE snapshot_id=NEW.snapshot_id) THEN
  RAISE EXCEPTION 'Feature unavailable at prediction cutoff';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER feature_cutoff BEFORE INSERT ON feature_values FOR EACH ROW EXECUTE FUNCTION enforce_feature_cutoff();
CREATE TABLE model_registry (
 model_version text PRIMARY KEY, event_type catalyst_type NOT NULL,
 algorithm text NOT NULL, features jsonb NOT NULL, hyperparameters jsonb NOT NULL DEFAULT '{}',
 dataset_version text NOT NULL, code_version text NOT NULL, seed integer,
 training_start timestamptz, training_end timestamptz, validation_end timestamptz,
 holdout_start timestamptz, metrics jsonb NOT NULL DEFAULT '{}',
 artifact_uri text, artifact_sha256 text, created_at timestamptz NOT NULL DEFAULT now(),
 CHECK(training_end IS NULL OR training_start<=training_end),
 CHECK(validation_end IS NULL OR training_end<=validation_end),
 CHECK(holdout_start IS NULL OR validation_end<holdout_start)
);
CREATE TABLE predictions (
 prediction_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), snapshot_id uuid NOT NULL REFERENCES feature_snapshots,
 model_version text NOT NULL REFERENCES model_registry, predicted_at timestamptz NOT NULL,
 horizon text NOT NULL, output jsonb NOT NULL,
 evaluation_kind text NOT NULL CHECK(evaluation_kind IN ('live','historical_backtest')),
 created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(snapshot_id,model_version,horizon,evaluation_kind)
);
CREATE TABLE outcomes (
 outcome_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), event_id uuid NOT NULL REFERENCES events,
 horizon text NOT NULL, entry_timestamp timestamptz NOT NULL, exit_timestamp timestamptz NOT NULL,
 raw_return numeric, benchmark_return numeric, abnormal_return numeric,
 benchmark_security_id uuid REFERENCES securities, label_method text NOT NULL,
 observed_at timestamptz NOT NULL, dataset_version text NOT NULL,
 quality_flags jsonb NOT NULL DEFAULT '[]', supersedes_outcome_id uuid REFERENCES outcomes,
 CHECK(exit_timestamp>=entry_timestamp), CHECK(observed_at>=exit_timestamp)
);
CREATE TABLE model_promotions (
 promotion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), model_version text NOT NULL REFERENCES model_registry,
 previous_version text REFERENCES model_registry, decision text NOT NULL,
 evidence jsonb NOT NULL, approved_by text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE research_ledger (
 research_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), question text NOT NULL,
 dataset_version text NOT NULL, code_version text NOT NULL, method text NOT NULL,
 parameters jsonb NOT NULL DEFAULT '{}', result jsonb NOT NULL,
 limitations text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE FUNCTION seal_predicted_snapshot() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF EXISTS(SELECT 1 FROM predictions WHERE snapshot_id=NEW.snapshot_id) THEN
  RAISE EXCEPTION 'Snapshot already used by a prediction';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER sealed_features BEFORE INSERT ON feature_values FOR EACH ROW EXECUTE FUNCTION seal_predicted_snapshot();
CREATE FUNCTION enforce_prediction_time() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.predicted_at < (SELECT prediction_cutoff FROM feature_snapshots WHERE snapshot_id=NEW.snapshot_id) THEN
  RAISE EXCEPTION 'Prediction timestamp precedes feature cutoff';
 END IF;
 IF NEW.evaluation_kind='live' AND (NEW.predicted_at < now()-interval '5 minutes' OR NEW.predicted_at > now()+interval '5 minutes') THEN
  RAISE EXCEPTION 'Live predictions must use the current capture timestamp';
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER prediction_time BEFORE INSERT ON predictions FOR EACH ROW EXECUTE FUNCTION enforce_prediction_time();
CREATE FUNCTION deny_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'Append-only audit record; insert a superseding record'; END $$;
CREATE TRIGGER immutable_predictions BEFORE UPDATE OR DELETE ON predictions FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_snapshots BEFORE UPDATE OR DELETE ON feature_snapshots FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_features BEFORE UPDATE OR DELETE ON feature_values FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_outcomes BEFORE UPDATE OR DELETE ON outcomes FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_models BEFORE UPDATE OR DELETE ON model_registry FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_sources BEFORE UPDATE OR DELETE ON source_documents FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_events BEFORE UPDATE OR DELETE ON events FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_promotions BEFORE UPDATE OR DELETE ON model_promotions FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE TRIGGER immutable_research BEFORE UPDATE OR DELETE ON research_ledger FOR EACH ROW EXECUTE FUNCTION deny_mutation();
CREATE INDEX events_time_type ON events(event_timestamp,event_type);
CREATE INDEX features_available ON feature_values(available_at);
COMMIT;
