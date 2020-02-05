SELECT * FROM USER;

SELECT
U.UserName
,L.UserId
,L.LoginTime
FROM LoginHistory L
INNER JOIN USER U ON U.UserID = L.UserID;