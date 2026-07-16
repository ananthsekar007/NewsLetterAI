# NewsLetter AI

NewsLetter AI helps nonprofit leaders keep track of policy updates that may affect their work.

Instead of asking someone to manually search government websites every week, this project gathers recent federal policy notices, organizes them by nonprofit service area, and saves the results in easy-to-review files.

## Why This Exists

Nonprofit organizations are often affected by policy changes in healthcare, housing, education, food support, workforce programs, arts funding, and community services. These updates can be hard to follow because they are spread across government websites and written in formal language.

This project is meant to make that process easier. It helps answer questions like:

- What changed recently?
- Which policy areas are affected?
- Which nonprofit organizations might care about those updates?
- Where can someone read the original government notice?

## Who This Is For

This project is designed for people who support or work with nonprofits, including:

- nonprofit executives and staff
- policy and advocacy teams
- community partners
- newsletter writers
- researchers
- grant and compliance staff

You do not need to be a software engineer to understand the purpose of the project. The technical scripts simply do the collecting and sorting work in the background.

## What It Does

The project currently follows a three-part workflow:

1. Collects a list of community and nonprofit leaders
2. Groups their organizations into broad policy areas
3. Fetches recent federal policy updates related to those areas

The final result is a weekly policy update file that can be reviewed, summarized, or turned into a newsletter.

## Policy Areas Tracked

The project groups organizations and policy updates into these areas:

- Healthcare, Mental Health & Disability Services
- Child Welfare, Family Stability & Housing
- Education, Youth Development & Literacy
- Food Security & Basic Needs
- Community Advocacy, Equity & Workforce Development
- Arts, Culture & Historic Preservation

## Main Files

### `data/asu_community_council.json`

This file contains the collected list of community council members, their roles, their organizations, and organization websites.

Think of this as the starting contact and organization list.

### `data/classified_organizations.json`

This file sorts the organizations into policy areas.

For example, a health clinic may be grouped under healthcare, while a foster care organization may be grouped under child welfare and housing.

### `data/weekly_policy_updates.json`

This is the main weekly output.

It contains recent federal policy updates, grouped by policy area. Each update includes information such as:

- title
- publication date
- government agency
- summary
- link to the original notice
- PDF link, when available

This is the file most useful for creating a newsletter or briefing.

## How To Use It

If everything is already set up, the usual process is:

1. Refresh the community organization list
2. Classify the organizations by policy area
3. Fetch the latest federal policy updates
4. Review `data/weekly_policy_updates.json`
5. Turn the most relevant updates into a newsletter or report

The scripts that do this work are in the `scripts` folder.

## Running The Workflow

From the project folder, run these commands in order:

```bash
python scripts/scrape_np_list.py
python scripts/classify_np.py
python scripts/fetch_federal_policy.py
```

After the final command finishes, open:

```text
data/weekly_policy_updates.json
```

That file contains the latest collected policy updates.

## What The Output Means

Each policy update should be treated as a lead for review, not as legal advice.

The project helps find and organize government notices, but a person should still review the original source before making decisions. Some updates may be highly relevant, while others may only be loosely related to a nonprofit's work.

## Current Limitations

This project currently focuses on federal policy updates from the Federal Register.

It does not yet fully track:

- state-level Arizona policy updates
- city or county policy changes
- funding opportunities
- deadline reminders
- plain-language newsletter summaries
- automatic email delivery

Those would be natural next steps for the project.

## Plain-English Summary

NewsLetter AI is an early-stage tool for helping nonprofit communities stay informed. It gathers recent federal policy updates, organizes them by nonprofit issue area, and creates a weekly file that can be reviewed by a person before being shared more broadly.

The goal is not to replace human judgment. The goal is to save time, reduce missed updates, and make policy monitoring easier for people who serve the community.
