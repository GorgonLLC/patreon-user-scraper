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
  COALESCE(data ->> '$.pageUser.data.attributes.created', data ->> '$.campaign.data.attributes.created') AS join_date,
  data ->> '$.userSuspensionReason' AS suspended_reason
FROM creators
WHERE data IS NOT NULL
ORDER BY creator_id
LIMIT 100;

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
| 30573 |                  |                |                               | marked_for_nuke  |
| 30574 |                  |                |                               | marked_for_nuke  |
| 30575 |                  |                |                               | marked_for_nuke  |
| 30576 |                  |                |                               | marked_for_nuke  |
| 30577 |                  |                |                               | marked_for_nuke  |
| 30578 |                  |                |                               | marked_for_nuke  |
| 30579 |                  |                |                               | marked_for_nuke  |
| 30580 |                  |                |                               | marked_for_nuke  |
| 30581 |                  |                |                               | marked_for_nuke  |
| 30582 |                  |                |                               | marked_for_nuke  |
| 30583 |                  |                |                               | marked_for_nuke  |
| 30584 |                  |                |                               | marked_for_nuke  |
| 30585 |                  |                |                               | marked_for_nuke  |
| 30586 |                  |                |                               | marked_for_nuke  |
| 30587 |                  |                |                               | marked_for_nuke  |
| 30588 |                  |                |                               | marked_for_nuke  |
| 30589 |                  |                |                               | marked_for_nuke  |
| 30590 | David Pechanec   |                | 2011-12-22T11:20:14.000+00:00 |                  |
| 30591 | Eli Davis        |                | 2011-12-22T11:20:11.000+00:00 |                  |
| 30592 |                  |                |                               | marked_for_nuke  |
| 30593 |                  |                |                               | marked_for_nuke  |
| 30594 |                  |                |                               | marked_for_nuke  |
| 30595 |                  |                |                               | marked_for_nuke  |
| 30596 |                  |                |                               | marked_for_nuke  |
| 30597 |                  |                |                               | marked_for_nuke  |
| 30598 |                  |                |                               | marked_for_nuke  |
| 30599 |                  |                |                               | marked_for_nuke  |
| 30600 |                  |                |                               | marked_for_nuke  |
| 30601 |                  |                |                               | marked_for_nuke  |
| 30602 |                  |                |                               | marked_for_nuke  |
| 30603 |                  |                |                               | marked_for_nuke  |
| 30604 |                  |                |                               | marked_for_nuke  |
| 30605 |                  |                |                               | marked_for_nuke  |
| 30606 |                  |                |                               | marked_for_nuke  |
| 30607 |                  |                |                               | marked_for_nuke  |
| 30608 |                  |                |                               | marked_for_nuke  |
| 30609 |                  |                |                               | marked_for_nuke  |
| 30610 |                  |                |                               | marked_for_nuke  |
| 30611 |                  |                |                               | marked_for_nuke  |
| 30612 |                  |                |                               | marked_for_nuke  |
| 30613 | Rachel Brown     |                | 2011-12-22T11:20:17.000+00:00 |                  |
| 30614 |                  |                |                               | marked_for_nuke  |
| 30615 |                  |                |                               | marked_for_nuke  |
| 30616 |                  |                |                               | marked_for_nuke  |
| 30617 |                  |                |                               | marked_for_nuke  |
| 30618 |                  |                |                               | marked_for_nuke  |
| 30619 |                  |                |                               | marked_for_nuke  |
| 30620 | Manny Calvar2    |                | 2013-05-04T14:20:52.000+00:00 |                  |
| 30621 | billy test       |                | 2013-05-06T06:11:34.000+00:00 |                  |
| 30622 | Lauren O'Connell | laurenoconnell |                               |                  |
| 30623 | Beatfreakz       | thebeatfreakz  | 2013-05-06T16:44:33.000+00:00 |                  |
| 30624 | Yanting Li       | yt             | 2013-05-07T00:28:43.000+00:00 |                  |
| 30625 | new happy        |                | 2013-05-07T01:18:45.000+00:00 |                  |
| 30626 | Matt Klein       |                | 2013-05-07T01:31:09.000+00:00 |                  |
| 30627 | Mark Campbell    |                |                               |                  |
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
