-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Look at all tables and schema of all in database (keep in a separate terminal for my reference)
-- .tables
-- .schema

-- Look at data from crime_scene_reports
SELECT *
FROM crime_scene_reports;

-- Look at data from crime_scene_reports that took place on 28 July 2023 and on Humphrey Street, find duck theft (10:15am)
SELECT *
FROM crime_scene_reports
WHERE street = 'Humphrey Street'
AND year = '2023'
AND month = '7'
AND day = '28';

-- Look at data from interviews, mostly out of curiosity
SELECT *
FROM interviews;

-- In the report of the duck theft, all three interviews mention the bakery, so search interviews to find ones with bakery
SELECT *
FROM interviews
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND transcript LIKE '%bakery%';
-- Info from interviews:
-- Ruth: Within 10 minutes of the theft, theif got into car in bakery parking lot and drove away. Is there footage of the parking lot between 10:05am and 10:25am?
-- Eugene: Recognized the thief, doesn't know name. Emma's bakery (yet not a witness?). Saw thief taking out money at the ATM (Leggett Street) in the morning before arriving at bakery
-- Raymond: Thief was leaving the bakery (before maybe driving out of parking lot, use this to narrow down time), called someone, talked less than a minute.
-- Thief planned on taking earliest flight out of fiftyville tomorrow (29 July 2023), and asked caller to purchase flgiht ticket (not tickets?)

-- Check bakery security logs for within 10 minutes of the theft
SELECT *
FROM bakery_security_logs
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND hour = '10'
AND minute > '05';
-- Possible license_plates (ids between 260 - 267 all possibilities, and saved in note outside this file for reference). 258 - 10:08 might be Eugene arriving at bakery?

-- Find Eugene's license plate number
SELECT *
FROM people
WHERE name = 'Eugene';

-- Then find when Eugene arrived at bakery to refine search for atm times
SELECT *
FROM bakery_security_logs
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND license_plate = '47592FJ';

-- Eugene might an unreliable witness or didn't drive to the bakery because there's no record of their license plate leaving or arriving on that day.
-- Eugene was at bakery 26 July 13:22 - 17:27 and 30 July 8:53 - 15:45
SELECT *
FROM bakery_security_logs
WHERE year = '2023'
AND month = '7'
AND license_plate = '47592FJ';

-- Thief could have been leaving anytime between 10:16am and 10:23am. Check phone records for this time period. Assuming duration is counted in seconds?
SELECT *
FROM phone_calls
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND duration <= '60';

-- Join above results with people to find the names of the callers and their information
SELECT *
FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.caller
WHERE year = '2023' AND month = '7'
AND day = '28'
AND duration <= '60';

-- Do above with receiver to get names of people who might've bought a flight ticket(s)
SELECT *
FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.receiver
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND duration <= '60';

-- Suspects to explore as thief: Sofia, Kelsey, Bruce, Katherine, Taylow, Diana, Carina, Kenny, Benista
-- Suspects to explore as accomplice: Jack, Larry, Robin, Luca, Melissa, James, Philip, Jacqueline, Doris, Anna

-- Join people with bakery security info to find names of people leaving bakery in order to find people who were leaving the bakery and made a phone call on the day of theft
SELECT *
FROM bakery_security_logs
JOIN people
ON people.license_plate = bakery_security_logs.license_plate
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND hour = '10'
AND minute > '05';

-- People who left the bakery and had a phone call of less than a minute on day of theft: Bruce, Sofia, Diana, Kelsey
-- I imagine people who left the bakery are not the people the thief is calling, so we can remove: Luca
-- Possible thieves: Bruce, Sofia, Diana, Kelsey
-- Possible accomplices: Jack, Larry, Robin, Melissa, James, Philip, Jacqueline, Doris, Anna

-- Check atm_transactions for morning of theft on Leggett street, join with bank accounts, join with people on account number:
SELECT *
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND atm_location = 'Leggett Street';

-- People who withdrew money and are suspects: Bruce (left 10:18, called Robin), Diana (10:23, called Philip)
-- Check flights for the day after theft (29 July 2023) order by earliest:
SELECT *
FROM flights
WHERE year = '2023'
AND month = '7'
AND day = '29'
ORDER BY hour ASC
LIMIT 1;

-- Earliest flight id is 36 (dep: 8, arr: 4), check passengers on that flight, join with people via passport_number
-- Check just passengers first out of curisoity:
SELECT *
FROM passengers
WHERE flight_id = '36';

SELECT *
FROM passengers
JOIN people
ON people.passport_number = passengers.passport_number
WHERE flight_id = '36';

-- Find flight destination destination: LaGuardia Airport, New York City, LGA.
SELECT *
FROM airports
WHERE id = '4';

-- Diana not on the flight, so not the thief. If I can trust Eugene, then the thief would be Bruce, with Robin as accomplice. If I don't trust Eugene, the thief could still be Kelsey.
-- Check entries to the bakery to see if Kelsey or Bruce were at the bakery while the theft took place, and of course... both were.
SELECT * FROM bakery_security_logs
JOIN people
ON people.license_plate = bakery_security_logs.license_plate
WHERE year = '2023'
AND month = '7'
AND day = '28'
AND hour >= '8'
AND hour <= '10';

-- I don't think there's a way except for Eugene's report to rule out Kelsey v. Bruce, so I'll have to say Bruce/Robin/New York City

