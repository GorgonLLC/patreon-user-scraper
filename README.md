# Patreon User Scraper

Scrapes Patreon users and stores the results in a SQLite database.

## Usage

```
$ scrapy crawl patreon -a exclude_ranges=[[9,79],[81,29400]]
```

To read the scraped data:

```
$ sqlite3 patreon.db
sqlite>.headers on
sqlite>.mode markdown
sqlite>
SELECT
  creator_id AS id,
  COALESCE(data ->> '$.pageUser.data.attributes.full_name', data ->> '$.campaign.data.attributes.name') AS name,
  COALESCE(data ->> '$.pageUser.data.attributes.vanity', data ->> '$.campaign.data.attributes.vanity') AS username,
  data ->> '$.campaign.data.attributes.patron_count' AS patron_count,
  data ->> '$.campaign.data.attributes.pledge_sum' AS pledge_sum
FROM creators
WHERE data IS NOT NULL AND patron_count > 0
ORDER BY patron_count DESC
LIMIT 20;

|  id   |            name            |     username     | patron_count | pledge_sum |
|-------|----------------------------|------------------|--------------|------------|
| 43579 | Kurzgesagt – In a Nutshell | Kurzgesagt       | 14772        |            |
| 36361 | Amanda Palmer              | amandapalmer     | 11344        |            |
| 51472 | Rob Has a Podcast          | RHAP             | 4576         |            |
| 47403 | Melody Lane                | Melodylane       | 4197         |            |
| 44481 | lovelyti                   | lovelyti         | 3991         |            |
| 39956 | Daily Tech News Show       | dtns             | 3840         |            |
| 31752 | Veritasium                 | veritasium       | 3514         |            |
| 36723 | Pretty Much It             | prettymuchit     | 3315         |            |
| 49401 | GamersNexus                | gamersnexus      | 3121         | 1141328    |
| 35605 | Robert Llewellyn           | FullyChargedShow | 3085         | 1375957    |
| 42913 | Zach Weinersmith           | ZachWeinersmith  | 3035         | 652331     |
| 54111 | Dave Barrack               | davebarrack      | 2902         | 861600     |
| 40381 | VaatiVidya                 | vaatividya       | 2529         |            |
| 30881 | Pomplamoose                | pomplamoose      | 2394         | 1278756    |
| 31368 | Adam Neely                 | adamneely        | 2152         |            |
| 36340 | VoicePlay                  | VoicePlay        | 1719         |            |
| 38672 | Ranged Touch               | rangedtouch      | 1663         | 908023     |
| 43849 | TerminalMontage            | terminalmontage  | 1661         |            |
| 43913 | David Pakman               | davidpakmanshow  | 1278         | 482958     |
| 48190 | Thunderf00t                | Thunderf00t      | 1277         |            |

sqlite>
SELECT
  creator_id AS id,
  COALESCE(data ->> '$.pageUser.data.attributes.full_name', data ->> '$.campaign.data.attributes.name') AS name,
  COALESCE(data ->> '$.pageUser.data.attributes.vanity', data ->> '$.campaign.data.attributes.vanity') AS username,
  COALESCE(data ->> '$.pageUser.data.attributes.created', data ->> '$.campaign.data.attributes.created') AS join_date,
  data ->> '$.userSuspensionReason' AS suspended_reason
FROM creators
WHERE data IS NOT NULL
ORDER BY creator_id
LIMIT 45;

|  id   |       name       |    username    |           join_date           | suspended_reason |
|-------|------------------|----------------|-------------------------------|------------------|
| 1     | Jack Conte       | jackconte      |                               |                  |
| 2     | Shishene Jing    | shishene       |                               |                  |
| 3     | Ruven Chu        | ruven          | 2011-09-10T00:00:00.000+00:00 |                  |
| 7     | Sandi Wu         |                | 2013-05-04T15:35:21.000+00:00 |                  |
| 8     | Mark Davis       |                | 2011-10-21T10:51:52.000+00:00 |                  |
| 80    | The Happy Talent | TheHappyTalent | 2011-11-15T03:53:06.000+00:00 |                  |
| 29418 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29480 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29495 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29560 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29562 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29633 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29748 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29851 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29906 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29919 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 29967 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30051 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30060 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30086 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30102 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30153 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30172 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30184 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30351 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30428 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30433 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30510 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30529 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30531 |                  |                | 2016-05-17T05:18:08.000+00:00 |                  |
| 30558 | new test         |                | 2013-04-24T11:48:37.000+00:00 |                  |
| 30559 | test me          |                | 2013-04-24T12:19:29.000+00:00 |                  |
| 30560 | first test       |                | 2013-04-24T12:34:01.000+00:00 |                  |
| 30561 | Nataly Dawn      | natalydawn     |                               |                  |
| 30562 | Gem              | geminieye      |                               |                  |
| 30563 |                  |                |                               |                  |
| 30564 | Ryan Lerman      | RyanLerman     | 2013-04-25T08:54:43.000+00:00 |                  |
| 30565 | Testers          |                | 2013-04-29T10:36:51.000+00:00 |                  |
| 30566 | Andrew McMurry   |                | 2013-04-29T21:04:16.000+00:00 |                  |
| 30567 | Joe Tester       |                | 2013-04-30T18:35:27.000+00:00 |                  |
| 30568 | Brenna Ehrlich   |                | 2013-04-30T19:46:54.000+00:00 |                  |
| 30569 | Sam Yam          | sam            |                               |                  |
| 30570 |                  |                |                               | marked_for_nuke  |
| 30571 |                  |                |                               | marked_for_nuke  |
| 30572 |                  |                |                               | marked_for_nuke  |
```

## Notes

The data is scraped from inline JavaScript at `/user?u=<user_id>` rather than through the JSON API endpoint `/api/user/<user_id>` due to an aggressive Cloudflare firewall blocking access.*

There are some variations in data between the endpoints. For instance, the `created` timestamp is not available for the "campaign" flavor of user at the endpoint we use. When looking at a suspended user, our endpoint will provide a `suspended_reason`, but the user's name will be `null`, while `/api/user/<user_id>` will show the user's name but not a suspension reason.

Here are some of the suspension reasons I've discovered:

```
sqlite>
SELECT DISTINCT(data ->> '$.userSuspensionReason') AS suspended_reason
FROM creators WHERE suspended_reason IS NOT NULL;

| suspended_reason  |
|-------------------|
| marked_for_nuke   |
| removed_gdpr      |
| removed_self_nuke |
| removed           |
```

\* The Cloudflare firewall can be bypassed with [puppeteer-extra-plugin-stealth](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth), but scraping will likely be slower due to driving a real browser.

## License

This project is licensed under the terms of the MIT license.
