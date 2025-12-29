-- detect shared devices
SELECT
    device,
    COUNT(DISTINCT ffp_number) AS account_count
FROM enrolment
GROUP BY device
HAVING account_count > 10
-- identify devices used to enroll multiple accounts
ORDER BY account_count DESC;

-- redemption shortly after joining
SELECT
    t.ffp_number,
    e.enrolment_date,
    t.transaction_date AS redemption_time,
    TIMESTAMPDIFF(HOUR, e.enrolment_date, t.transaction_date) AS hours_gap
FROM transactions t
    JOIN enrolment e ON t.ffp_number = e.ffp_number
WHERE t.miles_amount < 0 -- redemptions
    AND t.transaction_date <= DATE_ADD(e.enrolment_date, INTERVAL
48 HOUR); -- redeeming within 48 hours of joining

-- retro claims on new accounts
SELECT
    c.ffp_number,
    e.enrolment_date,
    c.departure_date,
    DATEDIFF(e.enrolment_date, c.departure_date) AS days_retro
FROM claims c
    JOIN enrolment e ON c.ffp_number = e.ffp_number
WHERE e.enrolment_date >= DATE_SUB(NOW(), INTERVAL
7 DAY) -- newly joined ffps in the past 7 days
AND c.departure_date < DATE_SUB
(e.enrolment_date, INTERVAL 30 DAY); -- claiming flights from 1-4 months earlier

-- incorrect birth dates (hard coded in the python script)
SELECT
    ffp_number,
    first_name,
    birth_date
FROM members
WHERE birth_date IN ('1900-01-01', '1910-01-01', '1920-01-01', '1930-01-01'); -- specific dates used in generation