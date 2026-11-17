-- 排除 thirdparty，找出部件数大于 8 的子系统
SELECT subsystem, COUNT(*) AS parts
  FROM components
 WHERE subsystem != 'thirdparty'
 GROUP BY subsystem
HAVING parts > 8
 ORDER BY parts DESC, subsystem
 LIMIT 20;
