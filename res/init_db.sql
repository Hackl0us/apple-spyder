CREATE TABLE IF NOT EXISTS apple_developer_rss
(
    id          TEXT PRIMARY KEY NOT NULL,
    update_time TEXT
);

INSERT INTO apple_developer_rss
VALUES ('RSS_FEED_UPDATE_TIME', NULL);

CREATE TABLE IF NOT EXISTS accessory_ota_update
(
    model          TEXT PRIMARY KEY NOT NULL,
    device_name    TEXT,
    update_time    TEXT
);

INSERT INTO accessory_ota_update
VALUES ('A2618','AirPods Pro 2', NULL);