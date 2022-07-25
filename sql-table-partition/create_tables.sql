BEGIN;

CREATE TABLE covid_data (
    day         date NOT NULL,
    country     varchar(70) NOT NULL,
    confirmed   integer NOT NULL,  -- int ok since all values < 2,147,483,647
    deaths      integer NOT NULL
);

CREATE TABLE covid_data_partitioned (
    day         date NOT NULL,
    country     varchar(70) NOT NULL,
    confirmed   integer NOT NULL,
    deaths      integer NOT NULL
)
PARTITION BY RANGE (day);

CREATE TABLE covid_data_2020q1 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2020-1-1') TO ('2020-4-1');
CREATE TABLE covid_data_2020q2 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2020-4-1') TO ('2020-7-1');
CREATE TABLE covid_data_2020q3 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2020-7-1') TO ('2020-10-1');
CREATE TABLE covid_data_2020q4 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2020-10-1') TO ('2021-1-1');
CREATE TABLE covid_data_2021q1 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2021-1-1') TO ('2021-4-1');
CREATE TABLE covid_data_2021q2 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2021-4-1') TO ('2021-7-1');
CREATE TABLE covid_data_2021q3 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2021-7-1') TO ('2021-10-1');
CREATE TABLE covid_data_2021q4 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2021-10-1') TO ('2022-1-1');
CREATE TABLE covid_data_2022q1 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2022-1-1') TO ('2022-4-1');
CREATE TABLE covid_data_2022q2 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2022-4-1') TO ('2022-7-1');
CREATE TABLE covid_data_2022q3 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2022-7-1') TO ('2022-10-1');
CREATE TABLE covid_data_2022q4 PARTITION OF covid_data_partitioned
    FOR VALUES FROM ('2022-10-1') TO ('2023-1-1');

COMMIT;
