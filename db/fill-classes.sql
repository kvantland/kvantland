ALTER TABLE Kvantland.Variant
ADD COLUMN classes text default 'all',
ADD COLUMN variant_points int;

ALTER TABLE Kvantland.Score
ADD COLUMN classes text default 'all';
