# Routines

Create these only from copy-critic-getting-started, each after its own yes, with your routine tool. Never say one exists or is on until listing your routines shows it.

## Weekly page review
- slug `weekly-page-review`, name "Weekly page review", description "Every Tuesday at 9 AM in your time zone, a cold read and score for each page in setup.md, with rewrites only where something slipped."
- Trigger: cron `0 9 * * 2` in the owner's time zone, flexible timing.
- Prompt:

This routine is turned on only after the owner's yes to this routine in a yes/no widget, and only when setup.md has a page and a time zone. If the owner pauses or turns it off, leave it that way.

Runs Tuesdays at 9:00 AM local. Read memory and setup.md first. For each URL in setup.md run copy-critic-first-read and copy-critic-clarity-score. Run copy-critic-rewrite only for pages whose lowest score is under 7 or got worse since last week. Message the owner once with a short table (page, what/who/next scores, change vs last week) and the rewrites. If every page is unchanged and scores 7 or above, stay quiet. Never edit the site or publish copy.

## After-deploy copy check
- slug `after-deploy-copy-check`, name "After-deploy copy check", description "After a production deploy, re-reads your pages at most once a day and flags copy that got less clear."
- Trigger from the setup.md deploy signal: GitHub `{"type": "github", "repo": "owner/name", "events": ["pr-merged"]}`, or `"events": ["ci-passed"]` with `"ciBranch"` when that branch runs real checks (a Vercel status alone is not CI). Origin `{"type": "origin", "repo": "owner/name", "events": ["pr-merged"]}`. Another host `{"type": "webhook"}`.
- Prompt:

This routine is turned on only after the owner picks a deploy signal in copy-critic-getting-started and says yes to this routine in a yes/no widget. If the owner pauses or turns it off, leave it that way. It is never a silent timer.

Trigger from the setup.md deploy signal:
- GitHub: a pull request merges into the site repo. If checks run on the default branch, use CI passing on that branch instead. A Vercel status alone is not CI.
- Origin: a pull request merges into the native Origin repo.
- Webhook: the owner's CI posts to this routine's URL after a production deploy.
- Event source or weekday timer: only if a dry run saves, or the owner asked for a timer, which you name as one.

When it fires, at most once a day: read memory and setup.md. Skip merges into other branches. Re-fetch each page in setup.md and compare text to the last review. If the deploy may not be live yet, check Vercel when connected or schedule one follow-up in 15 minutes. If nothing changed, stay quiet. If copy changed, run copy-critic-clarity-score; message the owner only when a score dropped or the primary CTA disappeared, quoting old vs new text with one fix. Never edit the site or open a pull request.
