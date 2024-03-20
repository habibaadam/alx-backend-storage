-- a SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans

SELECT origin, SUM(fans) AS total
FROM metal_bands
GROUP BY origin
ORDER BY total DESC;
